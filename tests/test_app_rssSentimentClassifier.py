import requests
import time
import json

BASE_URL = "http://127.0.0.1:5003"  # Note the port is changed to 5001 for sentiment classifier

# Define your custom classes here, if you want to filter by specific classes for sentiment analysis
# CLASSES = ["News", "Entertainment", "Sports", "Economy", "Technology", "Finance", "Politics"]  # Replace with your desired classes

CLASSES = None # Clssifies every entry


def trigger_sentiment_classification(classes):
    response = requests.get(f"{BASE_URL}/classify_sentiment", params={"classes": json.dumps(classes)})
    try:
        data = response.json()
        if response.status_code == 200:
            print(data["message"])
        else:
            print(f"Error triggering sentiment classification: {data['message']}")  # Changed 'error' to 'message' to match the expected server response key
    except ValueError:  # JSON decoding failed
        print(f"Unexpected server response: {response.text}")

def poll_status():
    while True:
        response = requests.get(f"{BASE_URL}/status")
        try:
            data = response.json()
            print(f"Status: {data['status']}, Number of entries classified: {data['num_classified']}")

            # Print start_time and current_runtime
            if data['start_time']:
                formatted_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['start_time']))
                print(f"Start Time: {formatted_start_time}")
            if data['current_runtime']:
                print(f"Current Runtime: {data['current_runtime']:.2f} seconds")

            if data['status'] == 'idle':
                break
        except ValueError:  # JSON decoding failed
            print(f"Unexpected server response: {response.text}")
            break
        time.sleep(1)

if __name__ == '__main__':
    trigger_sentiment_classification(CLASSES)
    poll_status()
