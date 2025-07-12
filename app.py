from flask import Flask, jsonify
from flask_cors import CORS
import json, os
from scraper import scrape_myntra  # your existing scraper function

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.getcwd(), "myntra_products.json")

@app.route("/products")
def products():
    with open(DATA_FILE, encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.route("/refresh")
def refresh():
    # Run the scraper and overwrite the JSON
    data = scrape_myntra(category="shoes", limit=20)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return jsonify({"status": "ok", "count": len(data)})


@app.route("/")
def home():
    return "Welcome to Myntra Scraper API!  Try /products or /refresh."


if __name__ == "__main__":
    app.run(debug=True)
