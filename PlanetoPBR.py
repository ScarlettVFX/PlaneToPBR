bl_info = {
    "name": "planetopbr",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os
from bpy_extras.io_utils import ImportHelper

class OBJECT_OT_import_plane_from_image(bpy.types.Operator, ImportHelper):
    """Operator to import a plane with a PBR material using an image as reference."""
    bl_idname = "object.import_plane_from_image"
    bl_label = "Import Plane from Image"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        """Execute the operator and import the plane from the diffuse image."""
        textures = load_pbr_textures(self.directory)
        import_plane_from_image(textures)
        return {'FINISHED'}

    def invoke(self, context, event):
        """Invoke the directory selection dialog."""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    """Add the operator to the 'Add Mesh' menu."""
    self.layout.operator(OBJECT_OT_import_plane_from_image.bl_idname)

def register():
    """Register the add-on classes and menu functions."""
    bpy.utils.register_class(OBJECT_OT_import_plane_from_image)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    """Unregister the add-on classes and menu functions."""
    bpy.utils.unregister_class(OBJECT_OT_import_plane_from_image)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

def load_pbr_textures(texture_folder):
    """Load PBR textures from a specified folder."""
    textures = {
        "diffuse": None,
        "roughness": None,
        "mask": None,
        "normal": None,
        "normal_extra": None,
        "depth": None,
    }

    for filename in os.listdir(texture_folder):
        filepath = os.path.join(texture_folder, filename)
        filename_lower = filename.lower()

        if "diffuse" in filename_lower:
            textures["diffuse"] = filepath
        elif "roughness" in filename_lower:
            textures["roughness"] = filepath
        elif "mask" in filename_lower:
            textures["mask"] = filepath
        elif "normal" in filename_lower:
            textures["normal"] = filepath
        elif "depth" in filename_lower:
            textures["depth"] = filepath

    print("Loaded textures:", textures)
    return textures

def import_plane_from_image(textures):
    """Import a plane and apply the diffuse image as a texture."""
    if not textures["diffuse"]:
        print("No diffuse image found!")
        return

    img = bpy.data.images.load(textures["diffuse"])
    aspect_ratio = img.size[0] / img.size[1]
    width = 2.0
    height = width / aspect_ratio

    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))
    plane = bpy.context.active_object
    plane.scale = (width / 2, height / 2, 1)
    plane.name = "PBR_Plane"

    bpy.ops.object.shade_smooth()
    apply_pbr_textures(plane, textures)
    plane.data.materials.append(bpy.data.materials.get("PBR_Material"))

    add_modifiers(plane, textures)

def apply_pbr_textures(plane, textures):
    """Apply the loaded PBR textures to the material of the plane."""
    mat = bpy.data.materials.new(name="PBR_Material")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    nodes.clear()

    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (1200, 0)

    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.location = (900, 0)
    links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    mapping = nodes.new(type='ShaderNodeMapping')
    mapping.location = (-600, 0)
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])

    if textures["diffuse"]:
        diffuse_node = nodes.new(type='ShaderNodeTexImage')
        diffuse_node.image = bpy.data.images.load(textures["diffuse"])
        diffuse_node.location = (-400, 300)
        links.new(mapping.outputs['Vector'], diffuse_node.inputs['Vector'])
        links.new(diffuse_node.outputs['Color'], bsdf.inputs['Base Color'])

    if textures["roughness"] and textures["mask"]:
        roughness_node = nodes.new(type='ShaderNodeTexImage')
        roughness_node.image = bpy.data.images.load(textures["roughness"])
        roughness_node.image.colorspace_settings.name = 'Non-Color'
        roughness_node.location = (-400, 100)

        mask_node = nodes.new(type='ShaderNodeTexImage')
        mask_node.image = bpy.data.images.load(textures["mask"])
        mask_node.image.colorspace_settings.name = 'Non-Color'
        mask_node.location = (-400, -100)

        mix_roughness_node = nodes.new(type='ShaderNodeMixRGB')
        mix_roughness_node.location = (100, 100)
        links.new(mapping.outputs['Vector'], roughness_node.inputs['Vector'])
        links.new(mapping.outputs['Vector'], mask_node.inputs['Vector'])
        links.new(roughness_node.outputs['Color'], mix_roughness_node.inputs['Color1'])

        mix_roughness_node.inputs['Color2'].default_value = (0.082, 0.082, 0.082, 1)  # Hex #151515
        links.new(mask_node.outputs['Color'], mix_roughness_node.inputs['Fac'])

        links.new(mix_roughness_node.outputs['Color'], bsdf.inputs['Roughness'])

    if textures["normal"]:
        normal_node = nodes.new(type='ShaderNodeTexImage')
        normal_node.image = bpy.data.images.load(textures["normal"])
        normal_node.image.colorspace_settings.name = 'Non-Color'
        normal_node.location = (-400, -300)

        normal_map_node = nodes.new(type='ShaderNodeNormalMap')
        normal_map_node.location = (400, -300)

        links.new(mapping.outputs['Vector'], normal_node.inputs['Vector'])
        links.new(normal_node.outputs['Color'], normal_map_node.inputs['Color'])

        mix_normal_node = nodes.new(type='ShaderNodeMixRGB')
        mix_normal_node.location = (600, -300)
        mix_normal_node.blend_type = 'MIX'
        mix_normal_node.inputs['Fac'].default_value = 0.5

        links.new(normal_map_node.outputs['Normal'], mix_normal_node.inputs['Color1'])
        links.new(normal_map_node.outputs['Normal'], mix_normal_node.inputs['Color2'])

        links.new(mix_normal_node.outputs['Color'], bsdf.inputs['Normal'])

def add_modifiers(plane, textures):
    """Add subdivision and displacement modifiers to the plane."""
    bpy.ops.object.modifier_add(type='SUBSURF')
    sub1 = plane.modifiers["Subdivision"]
    sub1.subdivision_type = 'SIMPLE'
    sub1.levels = 6
    sub1.render_levels = 6

    bpy.ops.object.modifier_add(type='SUBSURF')
    sub2 = plane.modifiers["Subdivision.001"]
    sub2.subdivision_type = 'SIMPLE'
    sub2.levels = 1
    sub2.render_levels = 1

    bpy.ops.object.modifier_add(type='DISPLACE')
    disp = plane.modifiers["Displace"]

    if textures["depth"]:
        displacement_texture = bpy.data.textures.new(name="DisplacementTexture", type='IMAGE')
        displacement_texture.image = bpy.data.images.load(textures["depth"])
        displacement_texture.image.colorspace_settings.name = 'Non-Color'
        disp.texture = displacement_texture

    disp.texture_coords = 'UV'
    disp.strength = 1.0
    disp.mid_level = 0.5
