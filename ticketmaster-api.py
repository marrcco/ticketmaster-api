from playwright.sync_api import sync_playwright
import json
import pandas as pd


page_url = "https://www.ticketmaster.com/minnesota-wild-vs-san-jose-sharks-saint-paul-minnesota-11-11-2025/event/060062F1D5BB5334"
match_id = page_url.split("/")[-1]


# playwright chromium starting
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Store requests we care about
    tracked_requests = {}
    collected_responses = []  # <- list to hold JSON responses

    # Listen to all requests
    def handle_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            print(request.url)
            if f"/api/ismds/event/{match_id}/facets" in request.url: # Catching facets XHR from TM network

                tracked_requests[request.url] = request # tracking fetched requests, GET
                print(f"Request found: {request.url}")
                if request.post_data:
                    print("POST data:", request.post_data)

    # Listen to responses
    def handle_response(response):
        request = response.request
        if request.resource_type in ["xhr", "fetch"]: # only accept xhr and fetch networks
            if request.url in tracked_requests:
                try:
                    body = response.text() # saving response from xhr and fetch
                    try:
                        body_json = json.loads(body) # loading fetch / xhr to JSON
                        collected_responses.append(body_json)  # saving JSON to a list
                        print("✅ Captured JSON response")

                    except json.JSONDecodeError:
                        print("Response Text (not JSON):", body)
                except Exception as e:
                    print("Failed to get response body:", e)

    page.on("request", handle_request) # listening to get
    page.on("response", handle_response)

    page.goto(page_url)
    page.wait_for_timeout(10000)  # max wait time for waiting for fetch and xhr

    # saving json to file
    if collected_responses:
        with open(f"json-data/{match_id}.json", "w", encoding="utf-8") as f:
            json.dump(collected_responses, f, indent=2, ensure_ascii=False)
        print("💾 Saved responses to responses.json")
    else:
        print("⚠️ No JSON responses captured")

    browser.close() # closing chromium


# loading saved json file
with open(f"json-data/{match_id}.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Find the first item that has ["_embedded"]["offer"]
all_tickets_data = [] # list to keep all tickets data from  JSON

json_data = None # initial value of JSON is None, until it's found in list of JSONs


# trying to find JSON that contains tickets data
for item in data:
    if isinstance(item, dict) and "_embedded" in item and "offer" in item["_embedded"]: # it is stored in _embedded > offer
        json_data = item["_embedded"]["offer"] # JSON found
        break

if json_data is not None: # If JSON data is Found
    print("Found tickets data in JSON.")

    for x in json_data:
        try:
            name = x["name"]
        except:
            name = None
        try:
            rank = x["rank"]
        except:
            rank = None
        try:
            offer_type = x["offerType"]
        except:
            offer_type = None
        try:
            ticket_type_id = x["ticketTypeId"]
        except:
            ticket_type_id = None
        try:
            desc = x["description"]
        except:
            desc = None
        try:
            list_price = x["listPrice"]
        except:
            list_price = None
        try:
            total_price = x["totalPrice"]
        except:
            total_price = None
        try:
            sellable_quantities = x["sellableQuantities"][-1]
        except:
            sellable_quantities = None
        try:
            currency = x["currency"]
        except:
            currency = None
        curr_data = {"name": name,
                     "rank": rank,
                     "currency" : currency,
                     "offer_type": offer_type,
                     "ticket_type_id": ticket_type_id,
                     "description": desc,
                     "list_price": list_price,
                     "total_price": total_price,
                     "selleable_quantities": sellable_quantities}
        all_tickets_data.append(curr_data)

    tickets_df = pd.DataFrame(all_tickets_data)
    tickets_df.to_csv(f"raw-data/{match_id}.csv",index=False)
else:
    print("No offer found")



