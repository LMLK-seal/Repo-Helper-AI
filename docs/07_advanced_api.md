# Advanced API Usage

This project supports several advanced parameters for fine-tuning its behavior.

## The `process` Endpoint
The primary endpoint is `/process`. It accepts a JSON payload.

### Parameters:
-   `source_path` (string, required): The path to the folder to process.
-   `output_path` (string, required): The path where results will be saved.
-   `force_jpeg` (boolean, optional, default: false): If true, all output images will be converted to JPEG format, regardless of their original format.
-   `quality` (integer, optional, default: 90): A number from 1 to 100 representing the JPEG compression quality if `force_jpeg` is true.