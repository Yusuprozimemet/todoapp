# todoapp

## Development — Step 1: FastAPI + Uvicorn

Follow these steps from the repository root (`E:\todoapp`) to create a virtual environment, install dependencies, and run the development server using PowerShell on Windows.

1) Create a virtual environment

```powershell
python -m venv venv
```

2) Activate the venv (PowerShell)

```powershell
# If your execution policy blocks scripts, temporarily allow them for this session:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Then activate the venv
.\venv\Scripts\Activate.ps1
```

3) Install dependencies

```powershell
pip install fastapi uvicorn
```

4) (Optional) Save exact pinned dependencies

```powershell
pip freeze > requirements.txt
```

5) Run the development server (from repo root)

```powershell
uvicorn app.main:app --reload
```

6) Verify endpoints in your browser or with curl:

- http://127.0.0.1:8000/  → {"message":"Welcome to the Task Manager API!"}
- http://127.0.0.1:8000/tasks  → {"tasks":[]}
- Swagger UI: http://127.0.0.1:8000/docs

Notes:
- The `requirements.txt` file in the repo currently lists `fastapi` and `uvicorn` as baseline entries; running `pip freeze > requirements.txt` will overwrite it with exact installed versions.
- The linter in your editor may report unresolved imports until you activate the virtual environment and install the packages.

If you'd like, I can also add a short `README` badge or a small `run.ps1` convenience script to automate activation + server start.
# todoapp