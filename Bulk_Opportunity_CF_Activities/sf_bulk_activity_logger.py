import requests
import json

url = "https://activityeditor.qlabs.sfdc.sh/v1/push_bulk_activities"
token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZW5jMl8vaWUzdkpIRkxTZDR0STRxY1hOK1pRPT1cbiIsImV4cCI6MTc4NDY4MTk3M30.QlFgI9Aqb2HGWRASyFnX_QbFc_ycgFJ1uC_vBx5vWA8"
# Load the payload from the file
with open('cleaned_events.json', 'r') as file:
    payload = json.load(file)

headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://activityeditor.qlabs.sfdc.sh",
    "Referer": "https://activityeditor.qlabs.sfdc.sh/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Storage-Access": "active",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"'
}

response = requests.post(url, headers=headers, data=json.dumps(payload))

print(response.status_code)
print(response.text)
