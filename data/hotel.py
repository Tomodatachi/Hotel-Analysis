#CHÚ Ý TRƯỚC KHI ĐỌC:
#1) Nếu cần, thay đổi địa chỉ của 2 file Driver và Browser trong phần CONFIG
#2) Có một biến counter quyết định số hotel mình lấy, biến này mặc định là 30,
#	(tương ứng với gần 1500 khách sạn), nếu cần lấy thêm thì đổi.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time, csv

# --- CONFIG ---

# Thay đổi vị trí Driver và Browser
# Tôi dùng Firefox, nếu dùng Chrome thì đổi

GECKO_PATH = r"D:/coding/python/selenium/geckodriver.exe"
FIREFOX_BINARY = r"C:/Program Files/Mozilla Firefox/firefox.exe"
OUTPUT_CSV = "hotels_hochiminh.csv"
URL = "https://www.booking.com/searchresults.html?dest_id=-3730078&dest_type=city&checkin=2025-09-27&checkout=2025-09-28&nflt=ht_id%3D204"
# -------------

options = Options()
options.binary_location = FIREFOX_BINARY
service = Service(GECKO_PATH)
driver = webdriver.Firefox(service=service, options=options)
driver.get(URL)
time.sleep(3)

results = []
counter = 0
seen_links = set()

def auto_scroll():
    """Scroll down until page height stops increasing."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_card_data(card):
    try:
        name = card.find_element(By.CSS_SELECTOR, "div[data-testid='title']").text.strip()
    except: name = "N/A"

    try:
        price = card.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price']").text.strip()
    except:
        try:
            price = card.find_element(By.CSS_SELECTOR, "span[class*='price']").text.strip()
        except:
            price = "N/A"

    try:
        room_size = ", ".join([
            b.text.strip()
            for b in card.find_elements(By.XPATH, ".//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'bed')]")
            if b.text.strip()
        ]) or "N/A"
    except: room_size = "N/A"

    if "Show on map" in room_size:
        room_size = ", ".join([p for p in room_size.split(",") if "Show on map" not in p]) or "N/A"

    try:
        score = card.find_element(By.CSS_SELECTOR, "div[data-testid='review-score']").text.strip()
    except:
        try:
            score = card.find_element(By.CSS_SELECTOR, "div[data-testid='review-score'] span").text.strip()
        except:
            score = "N/A"

    try:
        link = card.find_element(By.CSS_SELECTOR, "a[data-testid='title-link']").get_attribute("href")
    except: link = "N/A"

    try:
        address = card.find_element(By.CSS_SELECTOR, "span[data-testid='address']").text.strip()
    except: address = "N/A"

    return [name, price, room_size, score, link, address]

def scrape_current_page():
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid*='property-card']")
    new_count = 0
    for c in cards:
        data = extract_card_data(c)
        if data[4] not in seen_links:  # link is at index 4
            seen_links.add(data[4])
            results.append(data)
            new_count += 1
    print(f"Captured {new_count} new hotels (total: {len(results)})")

# Keep clicking + scrolling until no button
while True:
    auto_scroll()
    scrape_current_page()
    try:
        load_btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Load more results')]]")
        driver.execute_script("arguments[0].scrollIntoView(true);", load_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", load_btn)
        print("Clicked 'Load more results'...")
        time.sleep(3)
        
        counter += 1
        if counter >= 30:	#đổi nếu cần
            break
    except:
        print("No more 'Load more results' button found.")
        break

driver.quit()

# Save results
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Hotel Name", "Price (1 night)", "Room/Bed Size", "Score", "Link", "Address"])
    writer.writerows(results)

print(f"Done — saved {len(results)} hotels to '{OUTPUT_CSV}'")
