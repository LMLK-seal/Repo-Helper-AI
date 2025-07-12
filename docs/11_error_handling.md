# Error Handling and Logs

If the bot stops working or behaves unexpectedly, there are two primary places to look for errors.

## 1. The `uvicorn` Server Terminal
This is your first stop. The live terminal running the FastAPI application will print any critical tracebacks or errors that occur while the application is running. Look for red text or messages starting with `ERROR`.

## 2. The `bot.log` File
For issues happening within a background task, the application writes detailed logs to a file named `bot.log` in the root project directory. This file contains a timestamped record of every major step the bot takes and will contain the full traceback for any fatal errors that occur during issue processing.