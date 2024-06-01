# gateway

## Requirements

1. Python version: Ensure you are using a Python version that supports `tensorflow==2.15.0`. Specifically, any version of Python below 3.12 is compatible.
2. TensorFlow: `tensorflow==2.15.0`
3. TensorFlow Hub: `tensorflow-hub==0.16.1`
4. Firebase service account key in `.json` form
5. Database (CloudSQL/MySQL) credentials -> environment variable
6. Groq API key -> environment variable

> [!WARNING]
> Do not use `tensorflow==2.16.0` as it cannot load the model properly. Also, uninstall any conflicting dependencies that may interfere with `tensorflow==2.15.0` (e.g., `tf-keras` if it is installed).

## Run

1. `python -m venv .venv`
2. `.venv\Scripts\activate.bat`
3. `pip install -r requirements.txt`
4. Create environment variable files:

   `.env` :<br>

   ```
   ENVIRONMENT=DEVELOPMENT
   ```

   `.env.dev` :<br>

   ```
   SECRET_KEY=bangkit

   DB_HOST=<db_host>
   DB_PORT=<db_port>
   DB_USER=<db_user>
   DB_PASSWORD=<db_password>
   DB_NAME=<db_name>

   GROQ_API_KEY=<groq_api_key>
   ```

5. with cmd

   ```pwsh
   uvicorn src.main:app --reload --proxy-headers --host 0.0.0.0 --port 8000 
   ```

   or with Git Bash

   ```bash
   ./start.sh
   ```
