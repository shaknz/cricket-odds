from flask import Flask
import requests
import pymongo
import datetime

# MongoDB connection
MONGO_URI = "mongodb+srv://sdvlala:lRbxyXffXlCqLaAB@cricket-odds.87j7p.mongodb.net/?retryWrites=true&w=majority&appName=cricket-odds&tls=true"
DB_NAME = "cricket_odds"
COLLECTION_NAME = "odds_data"

## Service URL for remote trigger is here: https://cricket-odds-839974042016.us-central1.run.app

# Connect to MongoDB
try:
    client = pymongo.MongoClient(MONGO_URI)
    print("Connected to MongoDB successfully!")
except pymongo.errors.ConnectionError as e:
    print(f"Connection failed: {e}")
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# API key and endpoint
API_KEY = '0cf11ef1f0647bddaab1c1dc859e5474'
URL = 'https://api.the-odds-api.com/v4/sports/cricket_test_match/odds/'
PARAMS = {
    'apiKey': API_KEY,
    'regions': 'uk,au',
    'markets': 'h2h',
    'oddsFormat': 'decimal'
}

# Flask app
app = Flask(__name__)

@app.route('/')
def run_job():
    try:
        # Fetch data
        response = requests.get(URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        # Store in MongoDB
        for event in data:
            for bookmaker in event['bookmakers']:
                for market in bookmaker['markets']:
                    for outcome in market['outcomes']:
                        record = {
                            'game_id': event['id'],
                            'commence_time': event['commence_time'],
                            'in_play': event.get('in_play', False),
                            'bookmaker': bookmaker['title'],
                            'last_update': bookmaker.get('last_update', ''),
                            'home_team': event['home_team'],
                            'away_team': event['away_team'],
                            'market': market['key'],
                            'outcome_name': outcome['name'],
                            'outcome_price': outcome['price'],
                            'outcome_point': outcome.get('point', None),
                            'fetched_at': datetime.datetime.utcnow()
                        }
                        collection.insert_one(record)

        return "Data successfully fetched and stored in MongoDB!", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)