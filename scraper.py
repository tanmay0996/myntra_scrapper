from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json, os, time
import random

def scrape_myntra(category="shoes", limit=20):
    print(f"🚀 Starting scraper for category: {category}, limit: {limit}")
    
    options = Options()
    
    # Essential options for cloud deployment
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-ipc-flooding-protection")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    
    # Memory optimization
    options.add_argument("--memory-pressure-off")
    options.add_argument("--max_old_space_size=4096")
    
    # Anti-detection measures
    options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Set binary location (for cloud deployment)
    options.binary_location = '/usr/bin/google-chrome'
    
    driver = None
    try:
        print("🔧 Initializing Chrome driver with webdriver-manager...")
        
        # Use webdriver-manager to automatically handle version matching
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute script to hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Chrome driver initialized successfully")
        
    except Exception as e:
        print(f"❌ webdriver-manager failed: {e}")
        
        # Fallback to manual ChromeDriver
        try:
            print("🔄 Trying manual ChromeDriver...")
            service = Service('/usr/local/bin/chromedriver')
            driver = webdriver.Chrome(service=service, options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Manual ChromeDriver initialized successfully")
        except Exception as e2:
            print(f"❌ Manual ChromeDriver also failed: {e2}")
            return []

    url = f"https://www.myntra.com/{category}"
    print(f"🔗 Visiting: {url}")
    
    try:
        driver.get(url)
        print("📄 Page loaded, waiting for content...")
        
        # Check if page loaded properly
        page_title = driver.title
        print(f"📋 Page title: {page_title}")
        
        # Random delay to appear more human-like
        time.sleep(random.uniform(3, 5))
        
        # Wait for products to load with longer timeout
        print("⏳ Waiting for products to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-base"))
        )
        print("✅ Products loaded successfully")
        
        # Scroll to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Error loading page: {e}")
        
        # Try to get page source for debugging
        try:
            page_source_length = len(driver.page_source)
            print(f"📄 Page source length: {page_source_length}")
            
            # Check if we're blocked
            if "blocked" in driver.page_source.lower() or "captcha" in driver.page_source.lower():
                print("🚫 Detected blocking/captcha")
            
        except Exception as debug_e:
            print(f"❌ Debug info failed: {debug_e}")
        
        driver.quit()
        return []

    items = []
    
    try:
        products = driver.find_elements(By.CLASS_NAME, "product-base")
        print(f"🔍 Found {len(products)} products")
        
        if len(products) == 0:
            print("❌ No products found")
            driver.quit()
            return []
            
        products = products[:limit]
        print(f"🎯 Processing {len(products)} products")

        for i, prod in enumerate(products):
            try:
                print(f"📦 Processing product {i+1}/{len(products)}")
                
                # Add small delay between products
                if i > 0 and i % 5 == 0:
                    time.sleep(1)
                
                link = prod.find_element(By.TAG_NAME, "a").get_attribute("href")
                brand = prod.find_element(By.CLASS_NAME, "product-brand").text
                name = prod.find_element(By.CLASS_NAME, "product-product").text
                
                try:
                    price = prod.find_element(By.CLASS_NAME, "product-discountedPrice").text
                except:
                    try:
                        price = prod.find_element(By.CLASS_NAME, "product-price").text
                    except:
                        price = "Price not available"

                try:
                    image = prod.find_element(By.TAG_NAME, "img").get_attribute("src")
                except:
                    image = ""

                items.append({
                    "brand": brand,
                    "name": name,
                    "price": price,
                    "link": link,
                    "image": image
                })
                print(f"✅ Product {i+1} added: {brand} - {name}")
                
            except Exception as e:
                print(f"❌ Error processing product {i+1}: {e}")
                continue

    except Exception as e:
        print(f"❌ Error during scraping: {e}")
    
    finally:
        print(f"🏁 Scraping completed. Found {len(items)} valid products")
        driver.quit()

    return items