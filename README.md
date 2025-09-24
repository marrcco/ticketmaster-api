# 🎟️ Ticketmaster Scraper with Playwright & Python

This project uses [Playwright](https://playwright.dev/python/) to capture **Ticketmaster event API responses** (XHR/Fetch), extract **ticket offers**, and save them to structured JSON and CSV files for further analysis.  

---

## 📌 Features
- ✅ Automatically launches Chromium with Playwright.  
- ✅ Tracks **XHR/Fetch network requests**.  
- ✅ Captures the **facets API call** that contains ticketing data.  
- ✅ Saves all raw JSON responses to `json-data/`.  
- ✅ Extracts ticket offers (`_embedded > offer`) into a clean **CSV dataset** in `raw-data/`.  
- ✅ Collects key fields such as:
  - Ticket name  
  - Rank  
  - Offer type  
  - Ticket type ID  
  - Description  
  - List price & total price  
  - Sellable quantities  
  - Currency  

---

## ⚙️ Requirements
- Python **3.9+**
- [Playwright](https://playwright.dev/python/)
- [Pandas](https://pandas.pydata.org/)
- [JSON](https://docs.python.org/3/library/json.html) (built-in)

Install dependencies:

```bash
pip install playwright pandas
playwright install chromium
```
## 🚀 Usage
Clone this repo:

```bash
git clone https://github.com/your-username/ticketmaster-scraper.git
cd ticketmaster-scraper
```
Run the script with a Ticketmaster event URL:

```bash
Example inside the script:

python
page_url = "https://www.ticketmaster.com/minnesota-wild-vs-san-jose-sharks-saint-paul-minnesota-11-11-2025/event/060062F1D5BB5334"
The scraper will:

Save captured JSON response(s) to:

pgsql
json-data/{match_id}.json
Save structured ticket data to:

raw-data/{match_id}.csv
📂 Output Example
JSON (json-data/060062F1D5BB5334.json)
json
[
  {
    "_embedded": {
      "offer": [
        {
          "name": "Section 102",
          "rank": 1,
          "offerType": "standard",
          "ticketTypeId": "12345",
          "description": "Lower Bowl",
          "listPrice": 150.00,
          "totalPrice": 165.00,
          "sellableQuantities": [1, 2, 4],
          "currency": "USD"
        }
      ]
    }
  }
]
CSV (raw-data/060062F1D5BB5334.csv)
name	rank	currency	offer_type	ticket_type_id	description	list_price	total_price	selleable_quantities
Section 102	1	USD	standard	12345	Lower Bowl	150.0	165.0	4
```

## 🛠️ Customization
Change the page_url variable in scraper.py to any Ticketmaster event URL.

Adjust the wait_for_timeout if events load slower.

Extend the data extraction block to include more fields if needed.

## ⚠️ Disclaimer
This project is for educational and personal use only.
Scraping Ticketmaster may violate their Terms of Service — use responsibly.
