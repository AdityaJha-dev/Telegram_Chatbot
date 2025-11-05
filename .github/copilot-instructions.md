## Purpose
This repository is a small Telegram bot that uses aiogram + OpenAI. These instructions help AI coding agents contribute quickly by describing the project's structure, run/debug steps, and notable quirks discovered in the code.

## Big picture
- Main runtime: `main.py` — an aiogram-based Telegram bot that forwards user messages to OpenAI (chat model) and stores per-user conversation history in-memory (`user_history` dict).
- Research/example: `research/echo_bot.py` — an alternate/older example (aiogram v2-style) kept for reference.
- Test/debug helper: `test.py` — prints the certifi CA bundle path; useful for diagnosing SSL/cert issues when calling OpenAI.

Key flows
- Incoming Telegram -> aiogram handler in `main.py` -> append messages to `user_history[user_id]` -> call OpenAI via `openai.chat.completions.create` -> reply and append assistant message to `user_history`.

## Run / developer workflow (PowerShell)
1. Create virtual env and install deps:
   python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
2. Export env vars in PowerShell (example):
   $env:OPENAI_API_KEY = "<your_key>"
   $env:TELEGRAM_BOT_TOKEN = "<your_telegram_token>"
3. Run the bot:
   python main.py
4. Quick cert test (if TLS issues):
   python test.py
5. Research/example bot (older style):
   python research/echo_bot.py

### Windows / PowerShell notes

If PowerShell refuses to run `Activate.ps1` with an execution policy error, use one of the safe workarounds below.

- Enable script execution for the current user (minimal scope):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate as normal:

```powershell
\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

- Avoid activating the venv (no policy change): run the venv's Python directly:

```powershell
python -m venv .venv
\.venv\Scripts\python.exe -m pip install -r requirements.txt
\.venv\Scripts\python.exe main.py
```

- Use the Command Prompt activation (cmd) to bypass PowerShell policy:

```powershell
cmd /c ".venv\\Scripts\\activate.bat & python -m pip install -r requirements.txt & exit"
```

Notes:
- `RemoteSigned` allows locally created scripts to run but blocks unsigned scripts downloaded from the Internet unless unblocked. Use the minimum scope you need (`CurrentUser` recommended).
- When you see pip warnings like "script xyz.exe is installed in ... which is not on PATH", it's informational — call the scripts through the venv's `Scripts` directory or add that directory to your PATH if you want them globally available.

## Notable project-specific conventions & quirks
- Env var name inconsistency: `main.py` expects `OPENAI_API_KEY` while `research/echo_bot.py` uses `OpenAI_API_KEY`. Prefer `OPENAI_API_KEY` (upper snake case) and unify both files if you modify env handling.
- Two styles of aiogram are present: `main.py` uses aiogram v3-style handlers (decorators like `@dp.message(...)`), while `research/echo_bot.py` uses older v2-style (`@dp.message_handler`, `executor.start_polling`). Prefer v3-style code in `main.py` for new changes.
- In-memory conversation history: `user_history` is a dict keyed by Telegram user id. It's ephemeral (no persistence) — changing storage requires touching `main.py` where `user_history` is declared and used.
- System prompt is in `main.py` as `SYSTEM_PROMPT` and encodes a strong assistant persona and reply rules (max two sentences, tone, emojis). Changes to assistant behaviour should be done here and tested thoroughly.
- Model selection: `model_name = "gpt-3.5-turbo"` is defined in `main.py`. To switch models, update this variable and ensure the OpenAI client version supports the model and call shape.

## Important files to inspect for any change
- `main.py` — core logic, handlers, system prompt, model name, and in-memory history structure.
- `research/echo_bot.py` — reference echo implementation and an alternate environment-variable name usage.
- `requirements.txt` — pinned dependencies (aiogram==3.10.0, openai==1.35.13, python-dotenv==1.0.1). Use this exact file for reproducible installs.
- `test.py` — use when debugging TLS/cert issues; prints certifi CA path.

## Editing guidance / examples
- To change assistant persona or reply constraints: edit `SYSTEM_PROMPT` in `main.py`. Example: shorten sentences or remove emojis, then test by sending messages in Telegram.
- To make history persistent: replace `user_history` with a storage adapter (file/db). Update every handler that reads/appends to `user_history[user_id]`.
- To change env var names: update `load_dotenv()` usage and calls to `os.getenv(...)` in both `main.py` and `research/echo_bot.py` to the same key.

## Tests, linting, CI notes
- There is no test runner or CI config in this repo. `test.py` is a manual helper, not automated tests. When adding tests, follow the project's minimal style (single-file small scripts).

## Safety & behavior
- `SYSTEM_PROMPT` contains a deliberately provocative persona. When modifying assistant instructions, ensure changes align with policy and the target deployment audience.

If anything here is unclear or you want more detail (CI, deployment, persistent storage examples), tell me which area to expand and I'll update the file.
