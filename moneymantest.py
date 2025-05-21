import time
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def createDriver():
    options = Options()
    driver = webdriver.Firefox(options=options)
    return driver

def loadCookies(driver):
    try:
        with open("cookies.json", "r") as f:
            cookies = json.load(f)

        driver.get("https://open.spotify.com/")
        time.sleep(3)  # Give time for the site to load

        for cookie in cookies:
            cookie["domain"] = ".spotify.com"
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(f"Could not add cookie: {cookie['name']}, Error: {e}")

        print("Cookies loaded successfully!")
        driver.refresh()
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error loading cookies: {e}")

def playMusic(account):
    driver = createDriver()
    loadCookies(driver)

    # Open the song page
    driver.get(account["song_url"])
    time.sleep(5)

    try:
        #Accept cookie popup if present
        try:
            accept_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            accept_button.click()
            print("✅ Accepted cookies.")
            time.sleep(2)
        except Exception:
            print("✅ No cookie popup.")

        #Ensure we are logged in
        if "login" in driver.current_url:
            print("❌ Not logged in. Check cookies or login manually.")
            driver.quit()
            return

        #Wait for the play button to be clickable
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Play']"))
        )

        #Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView();", play_button)
        time.sleep(1)

        try:
            play_button.click()
        except Exception:
            print("⚠️ Normal click failed, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", play_button)

        print(f"✅ Playing song for account: {account['username']}")

        #Wait and check if playback starts
        time.sleep(5)

        #Check if playback is happening
        try:
            playing_icon = driver.find_element(By.XPATH, "//button[@aria-label='Pause']")
            print("🎵 Song is playing successfully!")
        except Exception:
            print("❌ Song did not start playing.")

    except Exception as e:
        print(f"❌ Error playing song for {account['username']}: {e}")

    time.sleep(5)
    driver.quit()

# Run function
playMusic({"username": "Chillout32", "song_url": "https://open.spotify.com/track/1AHf5FSofKcUw8tyKkccKF"})
