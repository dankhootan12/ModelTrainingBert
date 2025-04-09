from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set up WebDriver
driver = webdriver.Chrome()

# CSV file for saving data
csv_file = "labeled_malaysian_news.csv"
try:
    existing_data = pd.read_csv(csv_file)
    print(f"Loaded {len(existing_data)} existing articles.")
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=["title", "link", "label"])
    print("No existing data found. Starting fresh.")

# Initialize articles list
articles = []


# Scrape "More Sport" section
def scrape_more_sport():
    print("\nScraping 'More Sport' section...")
    driver.get("https://www.thestar.com.my/sport")
    try:
        for i in range(2):  # Click "Load More" twice
            print(f"Fetching articles from 'More Sport' (Load More {i + 1})...")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            section = soup.find("div", class_="more-news")
            if not section:
                print("No 'More Sport' section found.")
                break

            # Extract articles
            links = section.find_all("a", attrs={"data-list-type": "More Stories"})
            for link in links:
                title = link.get("data-content-title", "").strip()
                href = link.get("href", "").strip()
                full_link = f"https://www.thestar.com.my{href}" if href.startswith("/") else href
                articles.append({"title": title, "link": full_link, "label": "Sports"})

            print(f"{len(links)} articles fetched from 'More Sport'.")

            # Try clicking "Load More"
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "loadMorestories"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
                load_more_button.click()
                time.sleep(3)
            except TimeoutException:
                print("No more 'Load More' button found.")
                break
    except Exception as e:
        print(f"An error occurred in 'More Sport': {e}")


# Scrape subcategories
def scrape_subcategory(subcategory_url):
    print(f"\nScraping subcategory: {subcategory_url}...")
    driver.get(subcategory_url)
    page = 1
    while page <= 11:  # Limit to 11 pages
        try:
            print(f"Fetching articles from Page {page}...")
            soup = BeautifulSoup(driver.page_source, "html.parser")
            links = soup.find_all("a", attrs={"data-list-type": "Paged Stories"})
            if not links:
                print("No more articles found.")
                break

            for link in links:
                title = link.get("data-content-title", "").strip()
                href = link.get("href", "").strip()
                full_link = f"https://www.thestar.com.my{href}" if href.startswith("/") else href
                articles.append({"title": title, "link": full_link, "label": "Sports"})

            print(f"{len(links)} articles fetched from Page {page}.")

            # Click "Load More"
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "loadMorestories"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
                load_more_button.click()
                time.sleep(3)
            except TimeoutException:
                print("No more 'Load More' button found.")
                break
            page += 1
        except Exception as e:
            print(f"An error occurred in subcategory: {e}")
            break


# Execute scraping
try:
    scrape_more_sport()
    subcategories = [
        "https://www.thestar.com.my/sport/athletics",
        "https://www.thestar.com.my/sport/football",
        "https://www.thestar.com.my/sport/motorsport",
        "https://www.thestar.com.my/sport/other-sport",
    ]

    for url in subcategories:
        scrape_subcategory(url)

finally:
    driver.quit()

# Combine new articles with existing data and save
new_data = pd.DataFrame(articles)
combined_data = pd.concat([existing_data, new_data]).drop_duplicates(subset=["title", "link"], keep="first")
combined_data.to_csv(csv_file, index=False)
print(f"\nData saved to {csv_file} with {len(combined_data)} unique articles.")
