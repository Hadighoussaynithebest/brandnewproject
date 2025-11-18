r"""
Simple contact receiver (Flask)

Usage (local testing):
1. Create a virtual environment:
    python -m venv venv

2. Install Flask (two safe options):

    Option A — install without activating the venv (recommended; avoids PowerShell execution-policy issues):
      .\venv\Scripts\python -m pip install --upgrade pip
      .\venv\Scripts\python -m pip install flask

    Option B — activate the venv in PowerShell (may require a temporary bypass):
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
      .\venv\Scripts\Activate.ps1
      pip install flask

3. Run the server (using the venv python so activation is not required):
    .\venv\Scripts\python contact_server.py

4. Point your contact form `action` to: http://localhost:5000/contact

This server saves each submission to `messages/` as a timestamped JSON file.
Do NOT expose this without proper security for production.
"""
from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)
BASE = os.path.abspath(os.path.dirname(__file__))
MSG_DIR = os.path.join(BASE, 'messages')
os.makedirs(MSG_DIR, exist_ok=True)


def save_message(data: dict) -> str:
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    fname = f'msg_{ts}.json'
    path = os.path.join(MSG_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


@app.route('/contact', methods=['POST'])
def contact():
    # Accept form-encoded or JSON
    if request.is_json:
        payload = request.get_json()
    else:
        payload = {k: request.form.get(k) for k in request.form.keys()}

    # basic validation
    name = payload.get('name') or payload.get('Name') or ''
    email = payload.get('email') or payload.get('Email') or ''
    message = payload.get('message') or payload.get('Message') or ''

    record = {
        'received_at_utc': datetime.utcnow().isoformat() + 'Z',
        'name': name,
        'email': email,
        'message': message,
        'raw': payload
    }

    path = save_message(record)
    app.logger.info('Saved contact message to %s', path)

    # Respond with JSON for fetch() clients
    return jsonify({'status': 'ok', 'saved': os.path.basename(path)}), 201


@app.route('/_messages', methods=['GET'])
def list_messages():
    """Dev-only: return saved messages. Protected by CONTACT_ADMIN_TOKEN env var if set.

    Access with header 'X-Admin-Token' or query param 'token'.
    """
    admin_token = os.environ.get('CONTACT_ADMIN_TOKEN')
    provided = request.headers.get('X-Admin-Token') or request.args.get('token')
    if admin_token:
        if not provided or provided != admin_token:
            return jsonify({'error': 'unauthorized'}), 401
    else:
        return jsonify({'error': 'admin-token-not-configured', 'note': 'Set CONTACT_ADMIN_TOKEN for dev access'}), 403

    files = sorted([f for f in os.listdir(MSG_DIR) if f.endswith('.json')])
    entries = []
    for fname in files:
        path = os.path.join(MSG_DIR, fname)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            data = {'_error': 'failed to read', 'file': fname}
        entries.append({'file': fname, 'data': data})
    return jsonify({'count': len(entries), 'messages': entries})

if __name__ == '__main__':
    # Development server only. Use a real WSGI server for production.
    app.run(host='127.0.0.1', port=5000, debug=True)
