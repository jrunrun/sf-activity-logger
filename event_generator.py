import requests
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN


def create_activity(override="default", total_hours=7, task_type="Asset Creation", year=2024, month=7, day=22, start_time="09:00:00-05:00", subject_list=['product/research', 'cdapp', 'exp cloud', 'api stuff'], event_subject_override="", event_task_type_override="", event_duration_override=8, event_start_time_override=""):
    events = []
    current_total = 0
    event_start_date_time_offset_list = [0,1,2,3,4,5,6,7]
    start_date_time_str = f"{year}-{month:02d}-{day:02d}T{start_time}"


    def handle_time_block():
        nonlocal current_total
        event_duration = event_duration_override
        event_duration_decimal = Decimal(event_duration).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        event_duration_decimal_str = str(event_duration_decimal)

        event_start_date_time = datetime.fromisoformat(start_date_time_str)
        event_end_date_time = event_start_date_time + timedelta(hours=event_duration)

        event_start_date_time_str = event_start_date_time.isoformat()
        event_end_date_time_str = event_end_date_time.isoformat()

        events.append({
            "start_date_time": event_start_date_time_str,
            "end_date_time": event_end_date_time_str,
            "duration_str": event_duration_decimal_str,
            "duration": event_duration,
            "subject": event_subject_override,
            "task_type": event_task_type_override
        })
        current_total += event_duration

    def handle_reoccurring_events():
        nonlocal current_total
        for date_str in dates_list:
            month, day = map(int, date_str.split('-'))
            # event_start_date_time = datetime.fromisoformat(start_date_time_str) + timedelta(hours=offset)
            event_start_date_time = datetime(year, month, day, int(start_time.split(":")[0]), int(start_time.split(":")[1]))
            event_end_date_time = event_start_date_time + timedelta(hours=event_duration_override)

            event_start_date_time_str = event_start_date_time.isoformat()
            event_end_date_time_str = event_end_date_time.isoformat()

            event_duration_decimal = Decimal(event_duration_override).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            event_duration_decimal_str = str(event_duration_decimal)

            events.append({
                "start_date_time": event_start_date_time_str,
                "end_date_time": event_end_date_time_str,
                "duration_str": event_duration_decimal_str,
                "duration": event_duration_override,
                "subject": event_subject_override,
                "task_type": event_task_type_override
            })
            current_total += event_duration_override

    def handle_default():
        nonlocal current_total
        while current_total < total_hours:
            offset = random.choice(event_start_date_time_offset_list)
            event_start_date_time_offset_list.remove(offset)

            event_duration = 1
            event_subject = random.choice(subject_list)
            event_task_type = task_type
            event_start_date_time = datetime.fromisoformat(start_date_time_str) + timedelta(hours=offset)
            event_end_date_time = event_start_date_time + timedelta(hours=event_duration)

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
                "duration": event_duration,
                "subject": event_subject,
                "task_type": event_task_type
            })
            current_total += event_duration



    # Map override values to functions
    case_functions = {
        "default": handle_default,
        "time_block": handle_time_block,
        "reoccurring_events": handle_reoccurring_events,
    }

    # Call the appropriate function based on the override value
    case_functions.get(override, handle_default)()

    return events






# Generate events for each date in dates_list
# Generate events for each date in dates_list
def log_activity_in_salesforce(url, headers, dates_list, override="default", total_hours=5, subject_list=['product/research', 'cdapp', 'exp cloud', 'api stuff'], event_subject_override="PTO", event_task_type_override="Wellness", event_duration_override=8):
    template = {
        "form_data": {
            "StartDateTime": "",
            "Subject": "",
            "EndDateTime": "",
            "SE_Task_Type__c": "",
            "Description": "",
            "Remote__c": False,
            "Meeting_Type__c": "",
            "Duration__c": "",
            "WhoId": "",
            "RecordTypeId": "01230000001GgBYAA0"
        },
        "isNew": True
    }

    for date_str in dates_list:
        month, day = map(int, date_str.split('-'))
        events = create_activity(override="reoccurring_events", total_hours=total_hours, month=month, day=day, subject_list=subject_list, event_subject_override=event_subject_override, event_task_type_override=event_task_type_override, event_duration_override=event_duration_override)
        print(f"Generated events for {date_str}: {events}")
        print(f"Total duration for {date_str}: {sum(event['duration'] for event in events)} hours")

        # Create a new dictionary to store the new data
        updated_data = template.copy()

        for event in events:
            updated_data["form_data"]["StartDateTime"] = event["start_date_time"]
            updated_data["form_data"]["EndDateTime"] = event["end_date_time"]
            updated_data["form_data"]["Duration__c"] = event["duration_str"]
            updated_data["form_data"]["Subject"] = event["subject"]
            updated_data["form_data"]["SE_Task_Type__c"] = event["task_type"]
            print(updated_data)
            # Send the updated data to the API
            response = requests.post(url, headers=headers, json=updated_data)

            print(response.status_code)
            print(response.json())

url = 'https://activityeditor.qlabs.sfdc.sh/v1/upsert_62_event'
token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiZW5jMl8vaWUzdkpIRkxTZDR0STRxY1hOK1pRPT1cbiIsImV4cCI6MTcyMjEwNjk3NH0.nzHJN-5rI-U9TyumXFeXM0dT8Uvi1lSGAgJ0Vv6iOmk'
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


reoccurring_events = {"subject": "Alex/Justin", "task_type": "V2MOM Initiatives", "duration": 0.5}
dates_list = ['5-6', '5-13', '6-3', '6-17', '6-24', '7-8', '7-15', '7-22']

# ['5-6', '5-13', '6-3', '6-10', '6-17', '6-24','7-8', '7-15', '7-22']

log_activity_in_salesforce(url, headers, dates_list, override="handle_reoccurring_events", total_hours=5, subject_list=['product/research', 'cdapp', 'exp cloud', 'api stuff'], event_subject_override="Alex/Justin", event_task_type_override="V2MOM Initiatives", event_duration_override=0.5)
   

