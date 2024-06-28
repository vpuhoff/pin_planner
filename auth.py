import os

import requests
import yaml
from flask import Flask, redirect, request

from utils import update_tokens


def get_deviantart_authorization_url(client_id, redirect_uri):
    url = 'https://www.deviantart.com/oauth2/authorize'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    return requests.Request('GET', url, params=params).prepare().url

def get_deviantart_access_token(client_id, client_secret, redirect_uri, auth_code, file_path):
    url = 'https://www.deviantart.com/oauth2/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    update_tokens({'deviantart': tokens}, file_path)
    return tokens

def refresh_deviantart_access_token(client_id, client_secret, refresh_token, file_path):
    url = 'https://www.deviantart.com/oauth2/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    update_tokens({'deviantart': tokens}, file_path)
    return tokens

def get_pinterest_authorization_url(client_id, redirect_uri):
    url = 'https://www.pinterest.com/oauth'
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': 'read_public,write_public'
    }
    return requests.Request('GET', url, params=params).prepare().url

def get_pinterest_access_token(client_id, client_secret, redirect_uri, auth_code, file_path):
    url = 'https://api.pinterest.com/v1/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'redirect_uri': redirect_uri
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    update_tokens({'pinterest': tokens}, file_path)
    return tokens

def refresh_pinterest_access_token(client_id, client_secret, refresh_token, file_path):
    url = 'https://api.pinterest.com/v1/oauth/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    update_tokens({'pinterest': tokens}, file_path)
    return tokens
