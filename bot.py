import time
import os
from curl_cffi import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
OLX_URL = "YOUR_OLX_URL_HERE"
OTODOM_URL = "YOUR_OTODOM_URL_HERE"
SEEN_LISTINGS_FILE = "seen_listings.txt"

def send_telegram_message(message):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(api_url, data={"chat_id": CHAT_ID, "text": message})

def get_seen_listings():
    if not os.path.exists(SEEN_LISTINGS_FILE):
        return set()
    with open(SEEN_LISTINGS_FILE, "r", encoding="utf-8") as file:
        return set(file.read().splitlines())

def save_new_listing(link):
    with open(SEEN_LISTINGS_FILE, "a", encoding="utf-8") as file:
        file.write(link + "\n")

def scrape_olx_listings():
    seen_listings = get_seen_listings()
    response = requests.get(OLX_URL, impersonate="chrome")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", {"data-cy": "l-card"})
        
        for card in cards:
            link_elem = card.find("a")
            if not link_elem:
                continue
                
            link = link_elem["href"]
            if link.startswith("/"): 
                link = "https://www.olx.pl" + link
                
            if link not in seen_listings:
                title_elem = card.find("h6")
                title = title_elem.text.strip() if title_elem else "No Title"
                price_elem = card.find("p", {"data-testid": "ad-price"})
                price = price_elem.text.strip() if price_elem else "No Price"
                
                message = f"🚨 NEW OLX LISTING!\n\n🏠 {title}\n💰 {price}\n🔗 {link}"
                send_telegram_message(message)
                save_new_listing(link)
                print(f"New OLX listing sent: {title}")
    else:
        print(f"OLX Connection error: {response.status_code}")

def scrape_otodom_listings():
    seen_listings = get_seen_listings()
    response = requests.get(OTODOM_URL, impersonate="chrome")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("li", {"data-cy": "listing-item"})
        
        for card in cards:
            link_elem = card.find("a")
            if not link_elem: 
                continue
                
            link = link_elem["href"]
            if link.startswith("/"): 
                link = "https://www.otodom.pl" + link
                
            if link not in seen_listings:
                title_elem = card.find("p", {"data-cy": "listing-item-title"})
                title = title_elem.text.strip() if title_elem else "Otodom Listing"
                
                price_elem = card.find("span", string=lambda s: s and "zł" in s)
                price = price_elem.text.strip() if price_elem else "Price not parsed"
                
                message = f"🚨 NEW OTODOM LISTING!\n\n🏠 {title}\n💰 {price}\n🔗 {link}"
                send_telegram_message(message)
                save_new_listing(link)
                print(f"New Otodom listing sent: {title}")
    else:
        print(f"Otodom Connection error: {response.status_code}")

print("🤖 Bot active! Scanning OLX and Otodom... Press CTRL+C in terminal to stop.")
while True:
    scrape_olx_listings()
    scrape_otodom_listings()
    print("Waiting (10 minutes)...")
    time.sleep(600)