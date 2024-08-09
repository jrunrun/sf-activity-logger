import requests
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_DOWN
import json


def create_activity(date_str):
    events = []
    current_total = 0
    event_start_date_time_offset_list = [0,2,4,6]
    
    total_hours=3
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
def log_activity_in_salesforce(event_list):
    url = 'https://activityeditor.qlabs.sfdc.sh/v1/upsert_62_event'
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

    updated_data = template.copy()
    for event in event_list:
        updated_data["form_data"]["StartDateTime"] = event["start_date_time"]
        updated_data["form_data"]["EndDateTime"] = event["end_date_time"]
        updated_data["form_data"]["Duration__c"] = event["duration_str"]
        updated_data["form_data"]["Subject"] = event["subject"]
        updated_data["form_data"]["SE_Task_Type__c"] = event["task_type"]
        print(f"Event: {json.dumps(updated_data, indent=4)}")
        # Send the updated data to the API
        response = requests.post(url, headers=headers, json=updated_data)

        print(response.status_code)
        print(response.json())


# Example bulk payload is dict with key "events" and value is list of dicts
# {
#     "events": [
#         {
#             "StartDateTime": "2024-08-08T14:00:00-05:00",
#             "Subject": "Tune in to Laulima ’24 ",
#             "EndDateTime": "2024-08-08T17:00:00-05:00",
#             "SE_Task_Type__c": "Personal Development",
#             "Description": "<b><a href=\"http://sfdc.co/fy25laulima\" target=\"_blank\">Tune in to Laulima</a>, August 6-8</b><br><b><br></b>Get ready for our mid-year company moment! We ask that everyone tune in and participate so we can all learn, get aligned, and be inspired as we drive a strong finish in H2.<br><br><br>Join <a target=\"_blank\" href=\"https://salesforce-internal.slack.com/archives/C0317LHUZS4\"><u>#event-cko-laulima</u></a> for more details and to join the conversation.<br>All three days will be livestreamed to employees, where you’ll have the chance to hear directly from Marc and senior leaders about ...<ul><li><i>The</i> Dreamforce keynote </li><li>Must-know product innovations — with an AI and Data-first lens, we’ll cover both current sellable products and our future vision</li><li>Marc’s CEO priorities and the latest refresh of our FY25 Corporate V2MOM </li><li>Plus, demos, customer stories, and more!</li></ul><b>Livestream Instructions:</b><br>For the best results:<br><ol><li>Log into Okta from an up-to-date, <a href=\"https://support.video.ibm.com/hc/en-us/articles/360000403129-Supported-Browsers-for-IBM-Watson-Media\" target=\"_blank\"><u><u><u><u>supported browser</u></u></u></u></a> (Chrome or Firefox recommended)</li><li>Then launch the<a href=\"http://sfdc.co/fy25laulima\" target=\"_blank\"><u><u> FY25 Laulima</u></u></a> IBM page</li><li>You can also access the <u><u><a href=\"http://sfdc.co/fy25laulima-asl\" target=\"_blank\"><u><u>American Sign Language</u></u></a></u></u> IBM channel<br></li><li>Press the play button</li></ol><b>If you run into any issues with the livestream, try the following:</b><br><ol><li>Reload the page and press play</li><li>Restart your computer and follow step 1 above</li><li>Check out the <a href=\"https://concierge.it.salesforce.com/articles/en_US/Supportforce_Article/IBM-Watson-Streaming-Video\" target=\"_blank\"><u><u><u><u>Streaming Video article on Concierge</u></u></u></u></a></li></ol><b>To access the live text transcript:</b><br><ol><li>Head to <a href=\"https://www.streamtext.net/player?event=Laulima-24\" target=\"_blank\"><u><u><u>our Streamtext URL</u> </u></u></a>(Japanese link <a href=\"https://www.streamtext.net/player?event=Laulima-24-Japanese\" target=\"_blank\"><u><u>here</u></u></a>)</li><li>Click \"Sign in with Google\" and select your Salesforce email address</li><li>Click \"Continue to event using your Google Account\"</li></ol>",
#             "Remote__c": false,
#             "Meeting_Type__c": "",
#             "Duration__c": "3.00",
#             "WhoId": "",
#             "RecordTypeId": "01230000001GgBYAA0",
#             "id": "3vd2o39efei844vk56j2a4ksas",
#             "Location": "Streaming details below",
#             "selectedRecord": {}
#         },
#         {
#             "StartDateTime": "2024-08-07T14:00:00.000-05:00",
#             "Subject": "Tune in to Laulima ’24 ",
#             "EndDateTime": "2024-08-07T17:00:00-05:00",
#             "SE_Task_Type__c": "Personal Development",
#             "Description": "<b><a href=\"http://sfdc.co/fy25laulima\" target=\"_blank\">Tune in to Laulima</a>, August 6-8</b><br><b><br></b>Get ready for our mid-year company moment! We ask that everyone tune in and participate so we can all learn, get aligned, and be inspired as we drive a strong finish in H2.<br><br>Join <a target=\"_blank\" href=\"https://salesforce-internal.slack.com/archives/C0317LHUZS4\">#event-cko-laulima</a> for more details and to join the conversation.<br><br>All three days will be livestreamed to employees, where you’ll have the chance to hear directly from Marc and senior leaders about ...<ul><li><i>The</i> Dreamforce keynote </li><li>Must-know product innovations — with an AI and Data-first lens, we’ll cover both current sellable products and our future vision</li><li>Marc’s CEO priorities and the latest refresh of our FY25 Corporate V2MOM </li><li>Plus, demos, customer stories, and more! </li></ul><b>Livestream Instructions:</b><br>For the best results:<br><ol><li>Log into Okta from an up-to-date, <a href=\"https://support.video.ibm.com/hc/en-us/articles/360000403129-Supported-Browsers-for-IBM-Watson-Media\" target=\"_blank\"><u><u><u>supported browser</u></u></u></a> (Chrome or Firefox recommended)</li><li>Then launch the<a href=\"http://sfdc.co/fy25laulima\" target=\"_blank\"><u> FY25 Laulima</u></a> IBM page</li><li>You can also access the <u><u><a href=\"http://sfdc.co/fy25laulima-asl\" target=\"_blank\"><u>American Sign Language</u></a></u></u> IBM channel<br></li><li>Press the play button</li></ol><b>If you run into any issues with the livestream, try the following:</b><br><ol><li>Reload the page and press play</li><li>Restart your computer and follow step 1 above</li><li>Check out the <a href=\"https://concierge.it.salesforce.com/articles/en_US/Supportforce_Article/IBM-Watson-Streaming-Video\" target=\"_blank\"><u><u><u>Streaming Video article on Concierge</u></u></u></a></li></ol><b>To access the live text transcript:</b><br><ol><li>Head to <a href=\"https://www.streamtext.net/player?event=Laulima-24\" target=\"_blank\"><u><u>our Streamtext URL</u> </u></a>(Japanese link <a href=\"https://www.streamtext.net/player?event=Laulima-24-Japanese\" target=\"_blank\"><u>here</u></a>)</li><li>Click \"Sign in with Google\" and select your Salesforce email address</li><li>Click \"Continue to event using your Google Account\"</li></ol>",
#             "Remote__c": false,
#             "Meeting_Type__c": "",
#             "Duration__c": "3.00",
#             "WhoId": "",
#             "RecordTypeId": "01230000001GgBYAA0",
#             "id": "01ef9ovhki0g4nusel0kl3c0gl",
#             "Location": "Streaming details below",
#             "selectedRecord": {}
#         }
#     ]
# }





# dates_list = ['5-1-2024', '5-2-2024', '5-3-2024', '5-6-2024', '5-7-2024', '5-8-2024', '5-9-2024', '5-10-2024', '5-13-2024', '5-14-2024', '5-15-2024', '5-16-2024', '5-17-2024', '5-20-2024', '5-21-2024', '5-22-2024', '5-23-2024', '5-24-2024', '5-27-2024', '5-28-2024', '5-29-2024', '5-30-2024', '5-31-2024']
dates_list = ['5-28-2024', '5-29-2024', '5-30-2024', '5-31-2024']

def log_project_work_for_dates(dates_list):
    events = []
    for date_str in dates_list:
        e = create_activity(date_str)
        events.extend(e)
    print(f"Events for week: {json.dumps(events, indent=4)}")
    log_activity_in_salesforce(events)

log_project_work_for_dates(dates_list)