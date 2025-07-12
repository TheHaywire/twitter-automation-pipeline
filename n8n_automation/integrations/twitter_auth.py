import os
import requests
import urllib.parse
import webbrowser
import base64
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Tuple
import pkce

CLIENT_ID = os.getenv('X_CLIENT_ID')
CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')
REDIRECT_URI = os.getenv('X_REDIRECT_URI')
SCOPES = 'tweet.read tweet.write users.read offline.access'
AUTH_URL = 'https://twitter.com/i/oauth2/authorize'
TOKEN_URL = 'https://api.twitter.com/2/oauth2/token'
TOKEN_PATH = 'logs/twitter_tokens.json'

def save_tokens(tokens: dict):
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tokens, f)

def load_tokens() -> Optional[dict]:
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as f:
            return json.load(f)
    return None

def oauth2_pkce_flow() -> dict:
    code_verifier = pkce.generate_code_verifier()
    code_challenge = pkce.get_code_challenge(code_verifier)
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'state': 'state',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    auth_url = AUTH_URL + '?' + urllib.parse.urlencode(params)
    print('Open this URL in your browser to authorize:')
    print(auth_url)
    webbrowser.open(auth_url)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            qs = urllib.parse.parse_qs(parsed.query)
            self.server.auth_code = qs.get('code', [None])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>You may close this window.</h1>')
    httpd = HTTPServer(('127.0.0.1', 8080), Handler)
    print('Waiting for redirect and auth code on http://127.0.0.1:8080/callback ...')
    while not hasattr(httpd, 'auth_code'):
        httpd.handle_request()
    code = httpd.auth_code
    print('Received code:', code)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier,
    }
    basic_auth = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    headers['Authorization'] = f'Basic {basic_auth}'
    resp = requests.post(TOKEN_URL, headers=headers, data=data)
    tokens = resp.json()
    if 'access_token' not in tokens:
        raise RuntimeError('Failed to obtain access token.')
    save_tokens(tokens)
    return tokens

def refresh_access_token(refresh_token: str) -> Optional[dict]:
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': CLIENT_ID,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    basic_auth = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    headers['Authorization'] = f'Basic {basic_auth}'
    resp = requests.post(TOKEN_URL, headers=headers, data=data)
    tokens = resp.json()
    if 'access_token' in tokens:
        save_tokens(tokens)
        return tokens
    return None

def get_valid_access_token() -> Tuple[str, Optional[str]]:
    tokens = load_tokens()
    if not tokens:
        tokens = oauth2_pkce_flow()
    return tokens['access_token'], tokens.get('refresh_token')
