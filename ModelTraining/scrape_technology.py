from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set up WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
driver.get("https://www.thestar.com.my/tag/technology")

# Load existing data
csv_file = "labeled_malaysian_news.csv"
try:
    existing_data = pd.read_csv(csv_file)
    all_articles = existing_data.to_dict("records")  # Convert existing data to list of dicts
    print(f"Loaded {len(existing_data)} existing articles.")
except FileNotFoundError:
    all_articles = []
    print("No existing data found. Creating a new dataset.")

# Initialize variables for pagination
page_count = 1
max_pages = 11  # Set the maximum number of pages to scrape

# Loop through pagination
while page_count <= max_pages:
    print(f"Fetching articles from Page {page_count}...")
    try:
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract articles
        articles = soup.find_all("a", attrs={"data-list-type": "Paged Stories"})
        if not articles:
            print("No articles found on this page. Stopping.")
            break

        # Add articles to the dataset
        for article in articles:
            title = article.text.strip()  # Extract the text inside the <a> tag
            link = article.get("href", "").strip()  # Safely get 'href' or default to an empty string
            if not link:
                continue  # Skip articles without valid links
            full_link = f"https://www.thestar.com.my{link}" if link.startswith("/") else link
            all_articles.append({"title": title, "link": full_link, "label": "Technology"})

        print(f"{len(articles)} articles fetched from Page {page_count}.")

        # Find and click the "Load More" button
        try:
            load_more_button = driver.find_element(By.ID, "loadMorestories")
            driver.execute_script("arguments[0].click();", load_more_button)  # Use JavaScript to click
            time.sleep(5)  # Wait for the next articles to load
            page_count += 1
        except Exception as e:
            print(f"No more articles to load or error: {e}")
            break

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the browser
driver.quit()

# Save all articles to a CSV file
try:
    df = pd.DataFrame(all_articles)
    df.drop_duplicates(subset=["title"], inplace=True)  # Remove duplicate titles
    df.to_csv(csv_file, index=False)
    print(f"Data saved to {csv_file} with {len(df)} unique articles.")
except PermissionError:
    print(f"Permission denied: Unable to write to {csv_file}. Ensure the file is closed.")
