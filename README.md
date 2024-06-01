# gateway

## Requirements
1. Python Version: Ensure you are using a Python version that supports tensorflow==2.15.0. Specifically, any version of Python below 3.12 is compatible.
2. TensorFlow: tensorflow==2.15.0
3. TensorFlow Hub: tensorflow-hub==0.16.1

**Important Note**: Do not use tensorflow==2.16.0 as it cannot load the model properly. Also, uninstall any conflicting dependencies that may interfere with tensorflow==2.15.0 (e.g., tf-keras if it is installed).

## Run

1. `python -m venv .venv`
2. `.venv\Scripts\activate.bat`
3. `pip install -r requirements.txt`
4. With Git Bash
   ```
   ./start.sh
   ```
