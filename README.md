# 🏠 Wrocław Real-Time Rental Bot

An automated Python web scraper designed to track real-time rental listings on OLX and Otodom in Poland. Built to assist international students in finding affordable accommodation in highly competitive markets like Wrocław.

## 🚀 Features
- **Bypasses Anti-Bot Systems:** Uses `curl_cffi` to mimic real Google Chrome TLS fingerprints, successfully bypassing Cloudflare/Datadome 403 blocks on major real estate platforms.
- **Multi-Platform Scraping:** Extracts data simultaneously from OLX and Otodom using `BeautifulSoup4`.
- **Instant Telegram Alerts:** Sends real-time notifications directly to a mobile device via the Telegram Bot API the moment a new listing is published.
- **Memory & Deduplication:** Maintains a local database (`seen_listings.txt`) to ensure only brand new listings trigger alerts.
- **24/7 Cloud Deployment:** Designed to run continuously on PythonAnywhere via `nohup` for uninterrupted tracking.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Libraries:** `curl_cffi`, `BeautifulSoup4`, `os`, `time`
- **Deployment:** PythonAnywhere (Linux/Bash)

## ⚙️ How to Run Locally
1. Clone this repository.
2. Install dependencies: `pip install curl_cffi beautifulsoup4`
3. Replace `YOUR_TELEGRAM_TOKEN_HERE`, `YOUR_CHAT_ID_HERE`, and the target URLs with your actual data.
4. Run the script: `python bot.py`

*Note: For security reasons, the actual API tokens and Chat IDs have been omitted from this public repository.*
