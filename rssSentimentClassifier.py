import sqlite3
from transformers import pipeline
import yaml

CONFIG_PATH = "./config_rssSentimentClassifier.yaml"

# Load config from config.yaml
with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

MODEL = config['semantic_model']

sentiment_analysis = pipeline("sentiment-analysis", model=MODEL)

def classify_sentiments_in_db(db_path, classes_list=None, increment_func=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'rss_entries_%';")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Check and add 'Sentiment' column if it doesn't exist
        if 'Sentiment' not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN Sentiment TEXT;")
        
        if classes_list:
            cursor.execute(f"SELECT rowid, Title FROM {table} WHERE (Class IN ({', '.join(['?' for _ in classes_list])})) AND (Sentiment IS NULL OR Sentiment = '');", classes_list)
        else:
            cursor.execute(f"SELECT rowid, Title FROM {table} WHERE Sentiment IS NULL OR Sentiment = '';")
        
        titles = cursor.fetchall()

        for rowid, title in titles:
            try:
                sentiment = analyze_sentiment(title)
            except Exception as e:
                print(f"Error during classification of title '{title}': {e}")
                sentiment = 'Unknown'
            
            cursor.execute(f"UPDATE {table} SET Sentiment = ? WHERE rowid = ?", (sentiment, rowid))

            if increment_func:
                increment_func()
        
        conn.commit()
    conn.close()

def analyze_sentiment(title):
    if not title or not isinstance(title, str):
        return 'Unknown'
    return str(sentiment_analysis(title)[0]["label"])
