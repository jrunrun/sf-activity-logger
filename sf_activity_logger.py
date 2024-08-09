import requests
from datetime import datetime, timedelta

url = 'https://activityeditor.qlabs.sfdc.sh/v1/upsert_62_event'
headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZW5jMl8vaWUzdkpIRkxTZDR0STRxY1hOK1pRPT1cbiIsImV4cCI6MTcyMjAxNTA4MX0.2n-jm3E_CNnEVzSfJ7jQC9lVysLnMdoxzuYW2STQfQY',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://activityeditor.qlabs.sfdc.sh',
    'Pragma': 'no-cache',
    'Referer': 'https://activityeditor.qlabs.sfdc.sh/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
}

template = {
    "form_data": {
        "StartDateTime": "2024-07-23T09:00:00-05:00",
        "Subject": "cdapp",
        "EndDateTime": "2024-07-23T13:30:00-05:00",
        "SE_Task_Type__c": "Asset Creation",
        "Description": "",
        "Remote__c": False,
        "Meeting_Type__c": "",
        "Duration__c": "0.5",
        "WhoId": "",
        "RecordTypeId": "01230000001GgBYAA0"
    },
    "isNew": True
}


# Create a new dictionary to store the new data
updated_data = template.copy()

# Parse the original StartDateTime
StartDateTime_str = updated_data['form_data']['StartDateTime']
StartDateTime_dt = datetime.fromisoformat(StartDateTime_str)

# Add 1 hour
EndDateTime_dt = StartDateTime_dt + timedelta(hours=1)

# Update the new_data dictionary
updated_data['form_data']['EndDateTime'] = EndDateTime_dt.isoformat()


# Send the updated data to the API
response = requests.post(url, headers=headers, json=updated_data)

print(response.status_code)
print(response.json())

