# Image to WebP Converter

A simple GUI application to convert images to WebP format.

## Features

- Convert multiple images to WebP
- Adjustable quality settings (1-100%)
- Lossless compression option
- Choose output folder or save alongside originals
- Option to keep or delete original files

## Requirements

- Python 3.x
- Pillow (`pip install Pillow`)

## Building EXE

To build a standalone executable, run:
```bash
build.bat
```

The EXE file will be created in the `dist` folder.

## Usage

Run the application:
```bash
python webp_converter.py
```

1. Click "Select Images" to choose image files
2. (Optional) Select output folder
3. Adjust quality if needed
4. Click "Convert to WebP"

## Supported Formats

Input: JPG, JPEG, PNG, BMP, GIF, TIFF  
Output: WebP

