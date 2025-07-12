from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json, os

def scrape_myntra(category="shoes", limit=20):
    options = Options()
    
    # Enable headless mode for production deployment
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Additional options for better stability on cloud platforms
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")  # Faster loading
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--window-size=1920,1080")
    
    # Set user agent to avoid detection
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Use system Chrome instead of ChromeDriverManager
    try:
        # Try to use system chromedriver (installed via Docker)
        service = Service('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)
    except:
        # Fallback: Use Chrome binary directly
        options.binary_location = '/usr/bin/google-chrome'
        driver = webdriver.Chrome(options=options)

    url = f"https://www.myntra.com/{category}"
    print(f"🔗 Visiting: {url}")
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
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

    # Save to file
    with open("myntra_products.json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    driver.quit()
    return items