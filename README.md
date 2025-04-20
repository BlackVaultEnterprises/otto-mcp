# OTTO MCP Agent

A lightweight Model Context Protocol (MCP) agent designed to run inside GitHub Codespaces, providing terminal and filesystem access through a secure HTTPS endpoint.

## Features

- Terminal command execution
- File system operations (read/write/list)
- Automatic HTTPS tunneling via ngrok
- CORS enabled for cross-origin requests
- Health check endpoint

## Setup in Codespaces

1. Open this repository in GitHub Codespaces
2. Set your ngrok auth token (optional but recommended):
   ```bash
   export NGROK_AUTH_TOKEN='your_token_here'
   ```
3. Start the server:
   ```bash
   python otto_server.py
   ```
4. The server will output its public URL to both the console and `otto_url.txt`

## API Endpoints

- `POST /execute` - Execute terminal commands
- `POST /fs/read` - Read file contents
- `POST /fs/write` - Write to files
- `POST /fs/list` - List directory contents
- `GET /health` - Health check

## Adding to Cursor Toolbox

Once the server is running and you have the public URL, you can add it to Cursor's Toolbox using:

```python
mcp_toolbox_add_server({
    "qualifiedName": "otto-mcp-agent",
    "endpoint": "your_public_url_here"
})
```

## Security Notes

- The server exposes filesystem and terminal access - use appropriate security measures
- Consider implementing authentication for production use
- Be cautious with exposed endpoints and implement proper access controls