import requests
import yaml
import os
from flask import Flask, request, redirect


# Файл для хранения токенов
tokens_file = 'tokens.yaml'
