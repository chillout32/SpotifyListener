import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def createDriver():
    options = Options()
    driver = webdriver.Firefox(options=options)
    return driver

# Step 1: Open Spotify and log in manually
driver = createDriver()
driver.get("https://open.spotify.com/")

input("Log in manually and then press Enter...")  # Wait for manual login

# Step 2: Save cookies
cookies = driver.get_cookies()
with open("cookies.json", "w") as f:
    json.dump(cookies, f)

print("Cookies saved successfully!")
driver.quit()
