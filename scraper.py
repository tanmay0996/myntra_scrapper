from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json, os

def scrape_myntra(category="shoes", limit=20):
    options = Options()
    options.add_argument("--headless")  # Enable for production if needed
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.myntra.com/{category}"
    print(f"🔗 Visiting: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-base"))
        )
    except Exception as e:
        print("❌ Timeout waiting for products to load:", e)
        driver.quit()
        return []

    items = []
    products = driver.find_elements(By.CLASS_NAME, "product-base")[:limit]
    print(f"🔍 Found {len(products)} products")

    for prod in products:
        try:
            link = prod.find_element(By.TAG_NAME, "a").get_attribute("href")
            brand = prod.find_element(By.CLASS_NAME, "product-brand").text
            name = prod.find_element(By.CLASS_NAME, "product-product").text
            try:
                price = prod.find_element(By.CLASS_NAME, "product-discountedPrice").text
            except:
                price = prod.find_element(By.CLASS_NAME, "product-price").text

            image = prod.find_element(By.TAG_NAME, "img").get_attribute("src")

            items.append({
                "brand": brand,
                "name": name,
                "price": price,
                "link": link,
                "image": image
            })
        except Exception as e:
            print("⚠️ Skipping a product due to error:", e)
            continue

    with open("myntra_products.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    driver.quit()
    return items

# Flask app
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.getcwd(), "myntra_products.json")

@app.route("/products")
def products():
    if not os.path.exists(DATA_FILE):
        return jsonify([])
    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

@app.route("/refresh")
def refresh():
    data = scrape_myntra(category="shoes", limit=20)
    return jsonify({"message": "Scraped", "items": len(data)})

if __name__ == "__main__":
    app.run(debug=True)
