import requests
import yaml
import os
from flask import Flask, request, redirect

from shared import tokens_file
from auth import get_deviantart_access_token, get_deviantart_authorization_url, get_pinterest_access_token, get_pinterest_authorization_url, refresh_deviantart_access_token, refresh_pinterest_access_token
from utils import load_tokens

# Flask приложение для обработки callback
app = Flask(__name__)

@app.route('/deviantart/callback')
def deviantart_callback():
    auth_code = request.args.get('code')
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    redirect_uri = request.args.get('redirect_uri')
    tokens = get_deviantart_access_token(
        client_id, 
        client_secret, 
        redirect_uri, 
        auth_code, 
        tokens_file
    )
    return redirect('/')

@app.route('/pinterest/callback')
def pinterest_callback():
    auth_code = request.args.get('code')
    client_id = request.args.get('client_id')
    client_secret = request.args.get('client_secret')
    redirect_uri = request.args.get('redirect_uri')
    tokens = get_pinterest_access_token(
        client_id, 
        client_secret, 
        redirect_uri, 
        auth_code, 
        tokens_file
    )
    return redirect('/')

@app.route('/')
def index():
    return "Authorization complete. You can close this window."

def run_flask_app():
    app.run(port=5000)

def authorize_if_needed(deviantart_config, pinterest_config):
    tokens = load_tokens(tokens_file)

    if 'deviantart' not in tokens:
        print("Open the following URL to authorize DeviantArt:")
        print(get_deviantart_authorization_url(deviantart_config['client_id'], deviantart_config['redirect_uri']))
    elif 'pinterest' not in tokens:
        print("Open the following URL to authorize Pinterest:")
        print(get_pinterest_authorization_url(pinterest_config['client_id'], pinterest_config['redirect_uri']))
    else:
        deviantart_tokens = tokens.get('deviantart', {})
        if 'expires_in' in deviantart_tokens and deviantart_tokens['expires_in'] <= 0:
            refresh_deviantart_access_token(
                deviantart_config['client_id'], 
                deviantart_config['client_secret'], 
                deviantart_tokens['refresh_token'], 
                tokens_file
            )
        
        pinterest_tokens = tokens.get('pinterest', {})
        if 'expires_in' in pinterest_tokens and pinterest_tokens['expires_in'] <= 0:
            refresh_pinterest_access_token(
                pinterest_config['client_id'], 
                pinterest_config['client_secret'], 
                pinterest_tokens['refresh_token'], 
                tokens_file
            )


def main(deviantart_config, pinterest_config):
    authorize_if_needed(deviantart_config, pinterest_config)
    
    # Здесь вставьте логику для работы с изображениями, как описано ранее
    # Сохранение изображений в PocketBase и публикация их на Pinterest

if __name__ == "__main__":
    deviantart_config = {
        'client_id': os.environ.get("DEVIANTART_CLIENT_ID"),
        'client_secret': os.environ.get("DEVIANTART_CLIENT_SECRET"),
        'redirect_uri': 'http://localhost:5000/deviantart/callback'
    }

    pinterest_config = {
        'client_id': os.environ.get("PINTEREST_CLIENT_ID"),
        'client_secret': os.environ.get("PINTEREST_CLIENT_SECRET"),
        'redirect_uri': 'http://localhost:5000/pinterest/callback'
    }

    import threading
    threading.Thread(target=run_flask_app).start()
    main(deviantart_config, pinterest_config)
