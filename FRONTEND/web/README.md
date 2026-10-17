# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and Oxlint's TypeScript related rules in your project.

## Niza chat

The authenticated web app stores onboarding answers through the backend API and streams bot replies over WebSocket. Start the backend on port 8000 and the Niza bot on port 8001; see [BOTS/README.md](../../BOTS/README.md) for bot and Ollama setup.

Set `VITE_API_URL` to the backend base URL and `VITE_BOT_WS_URL` to the bot WebSocket URL when using non-default addresses. For HTTPS deployments, the WebSocket URL must use `wss://`.
