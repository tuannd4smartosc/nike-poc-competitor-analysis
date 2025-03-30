from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import uuid

class SeleniumScraper:
    def crawl_and_snapshot(self, link):
        # Set up headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without GUI
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        # Set up WebDriver (make sure you have chromedriver installed)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        # Open the target webpage
        url = link  # Replace with your target URL
        driver.get(url)

        # Wait for page to load
        time.sleep(2)  # Adjust as needed

        # Find the first h1 element
        h1_element = driver.find_element(By.TAG_NAME, "h1")

        # Scroll to the h1 element
        driver.execute_script("arguments[0].scrollIntoView();", h1_element)

        # Give time for smooth scrolling
        time.sleep(1)

        # Take a screenshot
        driver.save_screenshot(f"snapshot-{uuid.uuid4().hex}.png")
        print("Screenshot saved as snapshot.png")

        # Close the driver
        driver.quit()
