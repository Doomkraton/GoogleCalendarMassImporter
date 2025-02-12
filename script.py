import argparse
import glob
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from datetime import datetime, timedelta

# Set up the argument parser
parser = argparse.ArgumentParser(description='Google Calendar Mass Importer')
parser.add_argument('email', type=str, help='Email address for Google Calendar')
args = parser.parse_args()

# Get email from arguments
email = args.email

# Find client_secret file using wildcard
client_secret_files = glob.glob('./.credentials/client_secret*.json')
if not client_secret_files:
    raise FileNotFoundError('No client_secret*.json file found')
client_secret_filename = client_secret_files[0]

calendar = GoogleCalendar(email, credentials_path=client_secret_filename)  # Create a GoogleCalendar object

print("Importing events from ./event_list.txt. To add event to calendar write \"y\", to skip write \"n\".")

# Function to parse date and time
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d / %m / %Y %H:%M')
    except ValueError:
        return datetime.strptime(date_str, '%d / %m / %Y').date()

# Open the file containing the events
with open('./event_list.txt', 'r') as f:
    for line in f:
        # Assuming each line in the file is in the format: summary; start_date; [end_date]
        event_data = line.strip().split('; ')
        if len(event_data) < 2:
            print(f"Skipping invalid line: {line}")
            continue
        
        summary = event_data[0]
        start_date_str = event_data[1]
        end_date_str = event_data[2] if len(event_data) > 2 else None

        # Parse dates
        start_date = parse_date(start_date_str)
        if end_date_str:
            end_date = parse_date(end_date_str)
        else:
            if isinstance(start_date, datetime):
                end_date = start_date + timedelta(hours=1)
            else:
                end_date = None

        event = Event(
            summary=summary,
            start=start_date,
            end=end_date
        )  # Create a new event object
        
        print(f"Event: {event.summary}, Start: {event.start}, End: {event.end}")
        answer = input("Add event to calendar? (y/n): ")
        if answer == 'y':
            calendar.add_event(event)  # Add the event to the calendar
            print("Event added to calendar")
        else:
            print("Event skipped")