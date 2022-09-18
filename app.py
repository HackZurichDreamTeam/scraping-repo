from flask import Flask,jsonify
import json
import pandas as pd
import urllib.request, json 


app = Flask(__name__)

@app.route("/")
def index():
    return "Nothing here. "

@app.route('/scrapeweather', methods=['GET'])
def scrape_weather():
    #scrape weather call
    weather_data_path ='https://raw.githubusercontent.com/HackZurichDreamTeam/scraping-repo/main/scraped_weather.csv'
    got_df = pd.read_csv(weather_data_path)
    result = got_df.to_json(orient='records')
    parsed = jsonify(result)
    return parsed

@app.route('/scrapepirates', methods=['GET'])
def scrape_pirates():
    #scrape pirates call
    weather_data_path ='https://raw.githubusercontent.com/HackZurichDreamTeam/scraping-repo/main/scraped_pirates.csv'
    got_df = pd.read_csv(weather_data_path)
    result = got_df.to_json(orient='records')
    parsed = jsonify(result)
    return parsed


@app.route('/warnings', methods=['GET'])
def get_warnings():
    #get warnings
    warnings_data_path = 'https://raw.githubusercontent.com/HackZurichDreamTeam/data_science/main/data_for_backend/warnings.json'
    with urllib.request.urlopen(warnings_data_path) as url:
        parsed = jsonify(json.load(url))

    return parsed


@app.route('/shipment', methods=['GET'])
def get_shipment():
    #get shipment info
    shipment_data_path = 'https://raw.githubusercontent.com/HackZurichDreamTeam/data_science/main/data_for_backend/shipments.json'
    with urllib.request.urlopen(shipment_data_path) as url:
        parsed = jsonify(json.load(url))

    return parsed


if __name__ == "__main__":
    app.run()
