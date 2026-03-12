import os
import json
import time
import threading
from flask import Flask, jsonify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
config = {}
CONFIG_PATH = '/etc/config/config.json'

class ConfigReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == CONFIG_PATH:
            print("Config file changed, reloading...")
            load_config()

def load_config():
    global config
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        print(f"Config reloaded: {config}")
    except Exception as e:
        print(f"Error loading config: {e}")

@app.route('/config')
def get_config():
    return jsonify(config)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    load_config()
    
    event_handler = ConfigReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/etc/config', recursive=False)
    observer.start()
    
    app.run(host='0.0.0.0', port=8080)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()