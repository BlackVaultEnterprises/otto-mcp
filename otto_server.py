import os
import subprocess
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        return jsonify({
            'stdout': stdout,
            'stderr': stderr,
            'exit_code': process.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fs/read', methods=['POST'])
def read_file():
    data = request.json
    path = data.get('path')
    if not path:
        return jsonify({'error': 'No path provided'}), 400
    
    try:
        with open(path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fs/write', methods=['POST'])
def write_file():
    data = request.json
    path = data.get('path')
    content = data.get('content')
    if not path or content is None:
        return jsonify({'error': 'Path and content are required'}), 400
    
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fs/list', methods=['POST'])
def list_directory():
    data = request.json
    path = data.get('path', '.')
    
    try:
        items = os.listdir(path)
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

def setup_ngrok():
    try:
        # Get the auth token from environment variable
        auth_token = os.getenv('NGROK_AUTH_TOKEN')
        if auth_token:
            ngrok.set_auth_token(auth_token)
        
        # Start ngrok
        public_url = ngrok.connect(5000).public_url
        print(f'OTTO MCP Server is available at: {public_url}')
        return public_url
    except Exception as e:
        print(f'Failed to start ngrok: {e}')
        return None

if __name__ == '__main__':
    # Setup ngrok if auth token is available
    public_url = setup_ngrok()
    
    # Write the public URL to a file for reference
    if public_url:
        with open('otto_url.txt', 'w') as f:
            f.write(public_url)
    
    app.run(host='0.0.0.0', port=5000)