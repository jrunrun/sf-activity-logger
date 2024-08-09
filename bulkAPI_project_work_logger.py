import requests
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
import json


def create_activity(date_str):
    events = []
    current_total = 0
    event_start_date_time_offset_list = [0,2,4,6]
    
    total_hours=4
    task_type="Asset Creation"
    start_time="08:00:00-05:00"
    subject_list=['cdapp', 'exp cloud', 'api stuff', 'sf stuff', 'project work', 'product/research']
    event_duration_list=[1.5, 2, 3]

    month, day, year = map(int, date_str.split('-'))
    start_date_time_str = f"{year}-{month:02d}-{day:02d}T{start_time}"

    current_total = 0
    while current_total < total_hours:
        print(event_start_date_time_offset_list)
        offset = random.choice(event_start_date_time_offset_list)
        offset_index = event_start_date_time_offset_list.index(offset)
        event_start_date_time_offset_list.pop(offset_index)

        event_duration = random.choice(event_duration_list)
        event_subject = random.choice(subject_list)
        event_task_type = task_type
        event_start_date_time = datetime.fromisoformat(start_date_time_str) + timedelta(hours=offset)
        event_end_date_time = event_start_date_time + timedelta(hours=event_duration)

        # event_start_date_time_str = event_start_date_time.strftime('%Y-%m-%dT%H:%M:%S')
        # event_end_date_time_str = event_end_date_time.strftime('%Y-%m-%dT%H:%M:%S')

        event_start_date_time_str = event_start_date_time.isoformat()
        event_end_date_time_str = event_end_date_time.isoformat()

        event_duration_decimal = Decimal(event_duration).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        event_duration_decimal_str = str(event_duration_decimal)

        if current_total + event_duration > total_hours:
            event_duration = total_hours - current_total

        events.append({
            "start_date_time": event_start_date_time_str,
            "end_date_time": event_end_date_time_str,
            "duration_str": event_duration_decimal_str,
            "subject": event_subject,
            "task_type": event_task_type
        })
        current_total += event_duration

    print(f"Total duration: {current_total} hours")
    print(f"Events: {json.dumps(events, indent=4)}")

    return events


# Log the events in Salesforce
def log_activity_in_salesforce(event_list, token):
    bulk_url = 'https://activityeditor.qlabs.sfdc.sh/v1/push_bulk_activities'
    
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



def log_project_work_for_dates(dates_list, token):
    events = []
    for date_str in dates_list:
        e = create_activity(date_str)
        events.extend(e)
    print(f"Events for week: {json.dumps(events, indent=4)}")
    log_activity_in_salesforce(events, token)


dates_list = ['7-29-2024', '7-22-2024']
token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZW5jMl8vaWUzdkpIRkxTZDR0STRxY1hOK1pRPT1cbiIsImV4cCI6MTcyMzE1NjkyOH0.n-BpAN8wV4XrPv6ZhfV4d2x7RkAu-GdILIptdAmyHVM'
log_project_work_for_dates(dates_list, token)