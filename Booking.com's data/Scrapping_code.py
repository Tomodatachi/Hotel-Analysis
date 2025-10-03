from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

def scrape_booking_url(url, output_csv):
    driver = webdriver.Edge()
    driver.get(url)
    time.sleep(5)

    last_count = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        try:
            load_more = driver.find_element(By.XPATH, "//button[span[contains(text(),'Load more results')]]")
            driver.execute_script("arguments[0].click();", load_more)
            print("🔄 Clicked 'Load more results'")
            time.sleep(5)
        except NoSuchElementException:
            print("⚠️ Found no button 'Load more results', continue with checking the number of stays...")

        hotels = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'property-card')]")
        print(f"🔍 The current number of scrapped stays is approximately {int(len(hotels)/2)}")
        if len(hotels) == last_count:
            print("✅ All stays are loaded, no more new result.") 
            break
        last_count = len(hotels)

    hotels = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'property-card')]")
    print(f"🔍 The total number of stays is: {int(len(hotels)/2)}")

    unique_hotels = {}

    with open(output_csv, "w", newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = [
            "Stay","Price (2 adults/night)","Check_in","Check_out","Score","Stars","Address","Reviews","Overall","Link"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, hotel in enumerate(hotels, 1):
            try:
                name_elems = hotel.find_elements(By.XPATH, ".//div[@data-testid='title']")
                if not name_elems:
                    print(f"{i}. Skipped: Not a stay (perhaps ads or special cards).")
                    continue
                name = name_elems[0].text

                link_elems = hotel.find_elements(By.XPATH, ".//a")
                link = link_elems[0].get_attribute("href") if link_elems else "N/A"
                try:
                    rating = hotel.find_element(By.XPATH, ".//div[@data-testid='review-score']/div[1]").text
                except:
                    rating = "N/A"
                try:
                    location = hotel.find_element(By.XPATH, ".//span[@data-testid='address']").text
                except:
                    location = "N/A"
                try:
                    num_reviews = hotel.find_element(By.XPATH, ".//*[contains(text(),'reviews')]").text
                except:
                    num_reviews = "N/A"
                try:
                    price = hotel.find_element(By.XPATH, ".//*[contains(text(),'VND')]").text
                except:
                    price = "N/A"
                try:
                    overall_elems = hotel.find_elements(By.XPATH, ".//div[contains(@class, 'f63b14ab7a') and contains(@class, 'f546354b44') and contains(@class, 'becbee2f63')]")
                    overall = overall_elems[0].text if overall_elems else "N/A"
                except:
                    overall = "N/A"
                stars = len(hotel.find_elements(By.XPATH, ".//div[contains(@class, 'e03979cfad')]"))

                date_span_elems = hotel.find_elements(By.XPATH, ".//span[contains(@class, 'f323fd7e96')]")
                check_in, check_out = "N/A", "N/A"
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                for span in date_span_elems:
                    date_text = span.text
                    # Accept only if it contains a month abbreviation and " - "
                    if any(month in date_text for month in months) and " - " in date_text:
                        check_in, check_out = date_text.split(" - ", 1)
                        break

                if name not in unique_hotels:
                    unique_hotels[name] = (price,check_in,check_out,rating,stars,location,num_reviews,overall,link)
                    writer.writerow({
                        "Stay": name,
                        "Price (2 adults/night)": price,
                        "Check_in": check_in,
                        "Check_out": check_out,
                        "Score": rating,
                        "Stars": stars,
                        "Address": location,
                        "Reviews": num_reviews,
                        "Overall": overall,
                        "Link": link
                    })
                    print(f"{len(unique_hotels)}. {name} | ⭐ {rating} | {stars} |📍 {location} | 📝 {num_reviews}| 💰 {price} | 🏅 {overall} | 🛎️  {check_in} - {check_out}")
            except Exception as e:
                print(f"{i}. Error: {e}")

    driver.quit()
    print(f"✅ Saved into {output_csv}")

url = input("Booking.com's URL: ")
destination = input("Destination: ")
scrape_booking_url(url, f'booking_{destination}.csv')

# HCMC: https://www.booking.com/searchresults.html?ss=Ho+Chi+Minh+City&ssne=Ho+Chi+Minh+City&ssne_untouched=Ho+Chi+Minh+City&efdco=1&label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3730078&dest_type=city&ltfd=1%3A1%3A10-2025_11-2025_12-2025%3A1%3A1&group_adults=2&no_rooms=1&group_children=0
# Hanoi: https://www.booking.com/searchresults.html?label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&checkin=2025-10-06&checkout=2025-10-07&dest_id=-3714993&dest_type=city&group_adults=2&req_adults=2&no_rooms=1&group_children=0&req_children=0
# Danang: https://www.booking.com/searchresults.html?ss=Danang%2C+Vietnam&ssne=Hanoi&ssne_untouched=Hanoi&label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3712125&dest_type=city&checkin=2025-10-06&checkout=2025-10-07&group_adults=2&no_rooms=1&group_children=0
# Hai Phong: https://www.booking.com/searchresults.html?ss=Hai+Phong%2C+Hai+Phong+Municipality%2C+Vietnam&ssne=Danang&ssne_untouched=Danang&label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3714825&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=ce3f2c2bc1f80202&ac_meta=GhBjZTNmMmMyYmMxZjgwMjAyIAAoATICZW46A0hhaUAASgBQAA%3D%3D&checkin=2025-10-06&checkout=2025-10-07&group_adults=2&no_rooms=1&group_children=0
# Can Tho: https://www.booking.com/searchresults.html?ss=Can+Tho%2C+Can+Tho+Municipality%2C+Vietnam&ssne=Hai+Phong&ssne_untouched=Hai+Phong&label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3709910&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=c7fb2c38740201fc&ac_meta=GhBjN2ZiMmMzODc0MDIwMWZjIAAoATICZW46BGNhbiBAAEoAUAA%3D&checkin=2025-10-06&checkout=2025-10-07&group_adults=2&no_rooms=1&group_children=0
# Hue: https://www.booking.com/searchresults.html?ss=Hue%2C+Thua+Thien+-+Hue%2C+Vietnam&ssne=Can+Tho&ssne_untouched=Can+Tho&label=gen173nr-10CAEoggI46AdIM1gEaPQBiAEBmAEzuAEXyAEM2AED6AEB-AEBiAIBqAIBuAK78OPGBsACAdICJDg2NTdiNzM2LTFhYTYtNDAzNC1hZmUyLWRiYzA1ZDFiZDJlN9gCAeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=searchresults&dest_id=-3715887&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=d2b92c41d7d10168&ac_meta=GhBkMmI5MmM0MWQ3ZDEwMTY4IAAoATICZW46A2h1ZUAASgBQAA%3D%3D&checkin=2025-10-06&checkout=2025-10-07&group_adults=2&no_rooms=1&group_children=0
