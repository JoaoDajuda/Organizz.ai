# Niza bot

The bot validates each WebSocket bearer token against the authenticated onboarding endpoint in the backend. It does not connect directly to the database or store chat history.

Install the bot dependencies and download the configured Ollama model:

```sh
pip install -r requirements.txt
ollama pull llama3.2
```

Run the backend from `BACKEND` on port 8000, then run the bot from `BOTS`:

```sh
uvicorn main:app --reload --port 8001
```

If the backend uses another address, set `BACKEND_API_URL` before starting the bot. For example, `http://localhost:8000`.

The web app defaults to `http://localhost:8000` for its REST API and `ws://localhost:8001/robo/ws` for the bot. Override these with `VITE_API_URL` and `VITE_BOT_WS_URL` in the web app environment. Use `wss://` for deployments served over HTTPS.