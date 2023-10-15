import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from flask import Flask, jsonify, request
from rssSentimentClassifier import classify_sentiments_in_db
import threading
import yaml
import json
import time

app = Flask(__name__)

CONFIG_PATH = "./config_rssSentimentClassifier.yaml"

# Load config from config.yaml
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

DATABASE_PATH = config['database']['sqlite_path']

# Status variables
status = "idle"
num_classified = 0
start_time = None
num_classified_lock = threading.Lock()

def increment_classified_count():
    global num_classified
    with num_classified_lock:
        num_classified += 1

def run_sentiment_classification(classes_list=None):
    global status, num_classified, start_time
    start_time = time.time()
    try:
        classify_sentiments_in_db(DATABASE_PATH, classes_list, increment_func=increment_classified_count)
    except Exception as e:
        print(f"Error during classification: {e}")
    finally:
        status = "idle"

@app.route('/classify_sentiment', methods=['GET'])
def classify_sentiments():
    global status

    if status == "running":
        return jsonify({"message": "Sentiment Classification is already in progress!"}), 409

    status = "running"
    
    # Get classes from query parameters, or use None as default
    classes_list = request.args.get('classes', None, type=json.loads)
    
    # Start the classification in a separate thread
    threading.Thread(target=run_sentiment_classification, args=(classes_list,)).start()

    return jsonify({"message": "Sentiment Classification started successfully!"}), 200

@app.route('/status', methods=['GET'])
def get_status():
    current_runtime = None
    if status == "running" and start_time:
        current_runtime = time.time() - start_time

    return jsonify({
        "status": status,
        "num_classified": num_classified,
        "start_time": start_time,
        "current_runtime": current_runtime
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)  # Port changed to avoid conflict if running alongside the other service
