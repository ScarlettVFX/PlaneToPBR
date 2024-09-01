# PlanetoPBR: One-Click PBR Texture Importer for Blender

## Overview

**PlanetoPBR** is a Blender script designed to streamline the process of importing image planes and applying PBR textures. With this tool, you can effortlessly apply PBR textures (Diffuse, Normal, Roughness, Depth, and Mask) to your models in just a few clicks. This script is ideal for anyone looking to enhance their 3D models quickly without the need for complex manual texture mapping.

## Requirements

- **Blender** (version 3.0 or later recommended)
- Internet access for using the AI tools linked in the guide

## Installation

1. Download the `PlanetoPBR.py` script.
2. Open Blender and navigate to `Edit` > `Preferences`.
3. In the Preferences window, click on the `Add-ons` tab and select `Install...`.
4. Navigate to the location where you downloaded the `PlanetoPBR.py` file, select it, and click `Install Add-on`.
5. Ensure the add-on is enabled by checking the box next to its name.

## Usage

### Step 1: Prepare Your Images
- **Base Image Generation**: Use [FLUX](https://huggingface.co/spaces/black-forest-labs/FLUX.1-dev) to generate an image of a building facade. You can customize your prompt or use the following example:

  > "A weathered two-story urban building in a gritty, neglected neighborhood, centered in the frame, front-facing, fully visible from top to bottom. The historic brick exterior shows signs of heavy decay—chipped paint, crumbling masonry, and rusted metalwork. The storefront has large windows covered in posters and graffiti. Faded signage above, with flickering neon lights, hints at former vibrancy. The second-floor windows feature mismatched air conditioning units, with some panes boarded up or covered by haphazard curtains. The roofline shows rusted gutters, chipped cornices, and water damage. The building's sides reveal graffiti and fire escape ladders with peeling paint. The sidewalk is cracked with weeds, littered with debris. Lighting is soft, diffused daylight, evoking a sense of urban decay with a muted color palette."

- Crop your images to focus on the facade or the area you want to texture.

### Step 2: Generate Texture Maps
- **Window Mask**: Use [Grounded Segment Anything](https://huggingface.co/spaces/yizhangliu/Grounded-Segment-Anything) to generate a black-and-white window mask. This AI tool allows you to segment and detect objects with custom prompts.
- **Depth Map**: Generate a depth map using the [Marigold tool](https://huggingface.co/spaces/prs-eth/marigold) on Hugging Face. Adjust the ensemble size to 20 for maximum detail.
- **Normal Map**: Create a normal map using [Smart Normal](https://www.smart-page.net/smartnormal/). This free online tool converts your images into detailed normal maps.
- **Roughness Map**: Generate a roughness map using [Photo-Kako](https://www.photo-kako.com/en/hpf/). Adjust depth settings to around 3 for optimal results.

### Step 3: Organize Your Files
- Place all generated texture maps in a folder named “Textures.”
- Name the files with appropriate labels: `normal`, `depth`, `mask`, `diffuse`, `roughness`.

### Step 4: Import Image Plane in Blender
1. With the add-on enabled, go to the 3D Viewport in Blender.
2. Press `Shift+A` to add a new object and select `Image` > `Import Plane from Image`.
3. Navigate to your “Textures” folder and select all the texture files.
4. The script will automatically apply the textures to your model.

### Step 5: Adjust Modifiers
- Use the Modifiers Editor to fine-tune subdivisions and displacement scale as needed.

## License

This script is open-source and available under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and modify it as you see fit.

## Acknowledgments

This script wouldn't be possible without the excellent free tools provided by the following creators:

- **Black Forest Labs** for the [FLUX.1-dev tool](https://huggingface.co/spaces/black-forest-labs/FLUX.1-dev) on Hugging Face
- **Yizhong Liu** for [Grounded Segment Anything](https://huggingface.co/spaces/yizhangliu/Grounded-Segment-Anything) on Hugging Face
- **Smart-Page.net** for the [Smart Normal](https://www.smart-page.net/smartnormal/) tool
- **Photo-Kako** for their [Photo-Kako](https://www.photo-kako.com/en/hpf/) tool
- **Pieter-Jan Hoedt (prs-eth)** for [Marigold](https://huggingface.co/spaces/prs-eth/marigold) on Hugging Face
