# LangGraph AI Chatbot

Lightweight Streamlit frontend + LangGraph backend for conversational AI using Google GenAI (Gemini) models.

This repository contains a small demo chatbot that uses LangGraph to define a conversation graph and a Streamlit UI to interact with it. It is intended as a starting point for experimenting with multi-threaded chat sessions and integrating Google Generative AI through the `langchain_google_genai` connector.

## Contents

- `chatbot_backed.py` — backend graph definition (StateGraph) and node that calls the Google Generative AI model.
- `chatbot_frontend.py` — simple Streamlit frontend (smaller/demo).
- `chatbot_frontend_full.py` — fuller Streamlit frontend with multi-chat/thread handling and session-state management.
- `requirements.txt` — project dependency list (used to install modules).
- `assingment.ipynb` — notebook (placeholder in the workspace).
- `test.py` — small test / development helper (if present).

## Features

- Multi-thread chat support (conversations are identified by `thread_id`).
- Streamed assistant responses (uses the backend `chatbot.stream` API in the frontend).
- Simple in-memory checkpointing via `InMemorySaver` in the backend for short-lived sessions.

## Requirements

This project assumes Python 3.10+ (or compatible) and the packages listed in `requirements.txt`. The core libraries used include:

- streamlit
- langgraph
- langchain_core
- python-dotenv
- langchain_google_genai
- langchain_community

Install dependencies (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

If you prefer CMD instead of PowerShell use:

```cmd
.venv\Scripts\activate.bat
```

## Environment variables

The backend uses `dotenv` to load environment variables. Create a `.env` file in the project root with any keys required by your model provider. Example (you may need different names depending on your provider/connector):

```
GOOGLE_API_KEY=your_api_key_here
LANGCHAIN_API_KEY=...
```

Be careful not to commit secrets to source control. Add `.env` to `.gitignore`.

## Run the app (Streamlit)

From the project root (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
streamlit run .\chatbot_frontend_full.py
```

Or to run the simpler frontend:

```powershell
streamlit run .\chatbot_frontend.py
```

Open the browser link Streamlit prints (usually http://localhost:8501).

## How it works (brief)

- `chatbot_backed.py` defines a `StateGraph` with a single node `chat_node` that accepts messages and calls `ChatGoogleGenerativeAI` (Gemini). The compiled graph is exposed as `chatbot`.
- `chatbot_frontend_full.py` manages multiple conversation threads in `st.session_state['chat_threads']`, keeps per-thread message history in `message_history`, and uses `chatbot.stream`/`chatbot.invoke` to get responses.

## Troubleshooting

- If Streamlit raises a missing session state key error (e.g., `chat_threads`), make sure `chatbot_frontend_full.py` initializes session keys before accessing them. The repository contains an updated frontend that initializes `chat_threads`, `thread_id`, and `message_history` safely.
- If model/API errors occur, check that your API key is set and that the `langchain_google_genai` connector supports the configured model name.
- For issues starting Streamlit on Windows PowerShell, ensure you activate the virtual environment with `Activate.ps1` or use the correct activation script for your shell.

## Development notes & next steps

- Consider persisting conversations to disk or a database instead of `InMemorySaver` for longer-term storage.
- Add unit tests for the backend `chat_node` and a small integration test for the frontend to validate the message flow.
- Add input sanitization and rate limiting if you expose this service publicly.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Add tests where appropriate
4. Submit a pull request with a clear description of changes

## License

This project has no license file in the repository. If you want to make it open source, consider adding a `LICENSE` (for example MIT or Apache 2.0). Example: add an `MIT` file at the project root.

---

If you'd like, I can also:
- Add a short `README` badge and a `LICENSE` file.
- Create a small `run_local.ps1` script that sets up the venv and runs Streamlit (PowerShell-friendly).

Tell me which extras you want and I'll add them.