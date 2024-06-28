import yaml
import os

def save_tokens(tokens, file_path):
    with open(file_path, 'w') as f:
        yaml.dump(tokens, f)

def load_tokens(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    return {}

def update_tokens(new_tokens, file_path):
    tokens = load_tokens(file_path)
    tokens.update(new_tokens)
    save_tokens(tokens, file_path)
