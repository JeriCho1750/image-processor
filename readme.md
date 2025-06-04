# Image Processor - Batch Resize & Convert to WebP

A user-friendly GUI application for batch image processing with resizing and WebP conversion capabilities.

![Screenshot from 2025-06-04 11-21-10.png](../../Screenshot%20from%202025-06-04%2011-21-10.png)

## Features

- **Batch Processing**: Process multiple images at once
- **Two Processing Modes**:
  - Resize and convert to WebP with customizable dimensions
  - Convert to WebP only (preserve original dimensions)
- **Flexible Input**: Select individual files or entire folders
- **Smart Resizing Options**:
  - Maintain aspect ratio
  - Center crop to exact dimensions
  - Custom width and height settings
- **WebP Quality Control**: Adjustable quality settings (1-100)
- **File Naming**: Optional suffix addition to processed files
- **Real-time Preview**: See how your images will look before processing
- **Progress Tracking**: Visual progress bar and current file indicator
- **Error Handling**: Detailed error reporting for failed conversions

## Requirements

- Python 3.7 or higher
- Pillow (PIL) library
- tkinter (usually included with Python)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/image-processor.git
cd image-processor
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python image_processor.py
```

## Usage

### Basic Usage

1. **Select Images**: Click "Select Files" to choose individual images or "Select Folder" to process all images in a directory
2. **Choose Processing Mode**:
   - **Resize and convert**: Resize images to specific dimensions and convert to WebP
   - **Convert only**: Convert to WebP while preserving original dimensions
3. **Set Parameters** (for resize mode):
   - Width and Height: Target dimensions
   - Maintain aspect ratio: Preserve original proportions
   - Center crop: Crop to exact dimensions from center
4. **Adjust WebP Quality**: Use the slider to set compression quality (1-100)
5. **Configure Output**:
   - Select output folder
   - Choose whether to add suffix to filenames
6. **Process**: Click "Process All" to start batch processing

### Preview Feature

Use the "Preview" button to see how your images will look with current settings before processing the entire batch.

### Supported Formats

**Input formats**: JPEG, PNG, BMP, TIFF, GIF, WebP
**Output format**: WebP

## Command Line Usage

The application can also be run from command line:

```bash
python image_processor.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0
- Initial release
- Batch image processing
- WebP conversion
- Resize functionality
- GUI interface
- Preview feature
- Progress tracking

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/yourusername/image-processor/issues) on GitHub.

## Acknowledgments

- Built with Python and tkinter
- Image processing powered by Pillow (PIL)
- WebP format support for modern web optimization