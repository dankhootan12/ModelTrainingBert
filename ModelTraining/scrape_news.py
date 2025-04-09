from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from bs4 import BeautifulSoup

# Set up WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
driver.get("https://www.thestar.com.my/news/latest")

# Initialize a list to store all articles
all_articles = []

# Loop through pagination
while True:
    print("Fetching articles from the current page...")
    try:
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract articles
        articles = soup.find_all("a", attrs={"data-list-type": "Paged Stories"})
        if not articles:
            print("No articles found on this page. Stopping.")
            break

        for article in articles:
            title = article.text.strip()  # Extract the text inside the <a> tag
            link = article["href"].strip()  # Extract the href attribute
            full_link = f"https://www.thestar.com.my{link}" if link.startswith("/") else link
            all_articles.append({"title": title, "link": full_link})

        print(f"{len(articles)} articles fetched from the current page.")

        # Find the "Next" button and navigate
        next_button = soup.find("a", attrs={
            "data-content-title": f"Page {len(all_articles) // 38 + 2}"})  # Adjust based on page increment
        if not next_button:
            print("No more pages to navigate. Stopping.")
            break

        # Click the next button
        next_href = next_button["href"]
        driver.get(next_href)
        time.sleep(3)  # Wait for the next page to load

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the browser
driver.quit()

# Save all articles to a CSV file
if all_articles:
    df = pd.DataFrame(all_articles)

    # Drop duplicates
    df.drop_duplicates(subset=["title"], inplace=True)

    # Save the dataset
    df.to_csv("latest_malaysian_news.csv", index=False)
    print(f"Data saved to latest_malaysian_news.csv with {len(df)} unique articles.")
else:
    print("No articles were saved.")o3
