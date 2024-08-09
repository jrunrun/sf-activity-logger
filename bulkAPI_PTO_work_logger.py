import requests
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
import json

# Create an event for the date
def create_activity(date_str):

    total_hours=5
    task_type="V2MOM Initiatives"
    event_subject="Release Planning 254"
    start_time="12:00:00-05:00"
  
    month, day, year = map(int, date_str.split('-'))
    start_date_time_str = f"{year}-{month:02d}-{day:02d}T{start_time}"
    event_task_type = task_type
    event_start_date_time = datetime.fromisoformat(start_date_time_str)
    event_end_date_time = event_start_date_time + timedelta(hours=total_hours)
    event_start_date_time_str = event_start_date_time.isoformat()
    event_end_date_time_str = event_end_date_time.isoformat()
    event_duration_decimal = Decimal(total_hours).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
    event_duration_decimal_str = str(event_duration_decimal)

    event = {
        "start_date_time": event_start_date_time_str,
        "end_date_time": event_end_date_time_str,
        "duration_str": event_duration_decimal_str,
        "subject": event_subject,
        "task_type": event_task_type
    }  

    print(f"Event: {json.dumps(event, indent=4)}")

    return event



# Log the events in Salesforce
def log_activity_in_salesforce(event_list):
    bulk_url = 'https://activityeditor.qlabs.sfdc.sh/v1/push_bulk_activities'
    token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZW5jMl8vaWUzdkpIRkxTZDR0STRxY1hOK1pRPT1cbiIsImV4cCI6MTcyMzE1NjkyOH0.n-BpAN8wV4XrPv6ZhfV4d2x7RkAu-GdILIptdAmyHVM'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': token,
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

    template_bulk = {
        "StartDateTime": "",
        "Subject": "",
        "EndDateTime": "",
        "SE_Task_Type__c": "",
        "Description": "",
        "Remote__c": False,
        "Meeting_Type__c": "",
        "Duration__c": "",
        "WhoId": "",
        "RecordTypeId": "01230000001GgBYAA0",
        "id": "",
        "Location": "",
        "selectedRecord": {}
    }

    bulk_data = []
    for event in event_list:
        updated_data = template_bulk.copy()
        updated_data["StartDateTime"] = event["start_date_time"]
        updated_data["EndDateTime"] = event["end_date_time"]
        updated_data["Duration__c"] = event["duration_str"]
        updated_data["Subject"] = event["subject"]
        updated_data["SE_Task_Type__c"] = event["task_type"]
        bulk_data.append(updated_data)

    print(f"Bulk data: {json.dumps(bulk_data, indent=4)}")    
    
    # Send the updated data to the API
    response = requests.post(bulk_url, headers=headers, json={"events": bulk_data})
    print(response.status_code)
    print(response.json())




dates_list = ['7-29-2024', '7-22-2024']

def log_project_work_for_dates(dates_list):
    events = []
    for date_str in dates_list:
        e = create_activity(date_str)
        events.append(e)
    print(f"Events for week: {json.dumps(events, indent=4)}")
    log_activity_in_salesforce(events)

log_project_work_for_dates(dates_list)