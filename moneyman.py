import time
import subprocess
import multiprocessing
from selenium import webdriver
from undetected_chromedriver import Chrome, ChromeOptions


# List of accounts to be used
accounts = [ 
    {"username": "username1", "token": "token1", "song_url": "Spotify URL 1"},
    {"username": "username2", "token": "token2", "song_url": "Spotify URL 2"},
    {"username": "username3", "token": "token3", "song_url": "Spotify URL 3"},
    {"username": "username4", "token": "token4", "song_url": "Spotify URL 4"},
    {"username": "username5", "token": "token5", "song_url": "Spotify URL 5"},
]

vpn_servers = [
    'United States',
    'United Kingdom',
    'Canada',
    'Germany',
    'France',
    'Netherlands',
    'Sweden'
]

# Function to connect to a VPN server
def connectVpn(server):
    print(f"Connecting to {server} VPN server")
    subprocess.run(["nordvpn", "connect", server], check=True)

# Function to create a driver with VPN
def createDriverVpn(server):
    connect_vpn(server)
    options = ChromeOptions()
    driver = Chrome(options=options)
    return driver

# Function to play music with an account
def playMusic(account, server):
    driver = createDriverVpn(server)
    
    # Authenticates the account and plays the song
    driver.get(account["song_url"])

    time.sleep(5)

    try:
        play_button = driver.find_element_by_xpath("//button[@aria-label='Play']")
        play_button.click()
    except Exception as e:
        print(f"Error playing song for {account['username']}: {e}")
    
    time.sleep(34)

    driver.quit()


def runBot(account, server):
    while True:
        playMusic(account, server)

def main():
    processes = []
    for i, account in enumerate(accounts):
        server = vpn_servers[i % len(vpn_servers)]
        process = multiprocessing.Process(target=runBot, args=(account, server))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

if __main__ == "__main__":
    main()