# ExplainerAPI
The API that provides LLM generated violation summaries for xDECAF.

## Installing and Running
The following command makes the API accessible on port 8080 to anyone.
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```
If you only want to test locally use `--host 127.0.0.1` instead.

## Configuration
The `.env` configuration file has to be created in the projects root folder, on the same level the main.py. This project has an example for the contents of `.env` under `docs/env.example`, which you can copy and adjust to your needs.
```bash
cp docs/env.example .env
nano .env
```

# Usage
The API provides the following endpoints:
| Endpoint | Variables | Description | Protection |
| :--- | :--- | :--- | :--- |
| /health | `none` | shows current API status including used model | `none` |
| /explain | `violation` | sends violation prompt to llm and returns explaination | `api key` `rate limiting` |

For further information look at the examples in `docs/health.txt` and `docs/explain.txt`.

## Security
To secure this API from misuse the following mechanisms are implemented:
* **api keys** for authentication
* per api key **rate limiting**
