import os 
import datetime 
from google.oauth2 import service_account 
from googleapiclient.discovery import build
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
dotenv_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path)
credentials_path = os.path.join(root_dir, 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/calendar'] 
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID') 
SERVICE_ACCOUNT_FILE = credentials_path 

def get_calender_service():
    """Google Calendar API connection """
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"file nhi mil rahi: {SERVICE_ACCOUNT_FILE}") 
        return None
    try:
        cred=service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,scopes=SCOPES
        )
        service=build('calendar','v3',credentials=cred)
        return service
    except Exception as e:
        print(f"error",{e})
        return None

def check_availability(date_str,time_str):# "2025-12-25","17:00" 
    """
    Check available specific time slot is empty or not?
    Format: date_str='2025-12-25', time_str='17:00'
    Returns: (True/False, Message)
    """

    service=get_calender_service()
    if not service:
        return False, "calender connection error"
    try:
        start_dt=datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt=start_dt+datetime.timedelta(hours=1) 
        start_iso=start_dt.isoformat()+ '+05:00' # only asian country
        end_iso = end_dt.isoformat() + '+05:00' 
        print(f"🔍 Checking Calendar for: {date_str} at {time_str} (PKT)...")
        events_result=service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_iso,
            timeMax=end_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events=events_result.get('items',[]) 
        if not events:
                return True, f"✅ yes, {date_str} and {time_str} slot is empty"
        else:
                return False, f"❌ Sorry, {time_str} slot not empty."
    except Exception as e:
        return False, f"Error checking availability: {e}"
            

def book_appointment(name, phone,date_str,time_str):
    """
    Books a new appointment.
    Use this ONLY when user confirms "Yes book it".
    """
    is_available, message = check_availability(date_str, time_str)
    if not is_available:
        return f"🚫 Booking Failed: slot  not available."
        
    service=get_calender_service()
    if not service:
        return "system Error"


    try:
        start_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + datetime.timedelta(hours=1)
        event_body = {
            'summary': f'Appointment: {name}',
            'description': f'Patient Phone: {phone}',
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'Asia/Karachi',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'Asia/Karachi',
            },
        }
        event=service.events().insert(calendarId=CALENDAR_ID,body=event_body).execute()
        return f"booking confirmed your id is : {event.get('id')}"
    except Exception as e:
        return f"Booking error: {e}"
    
if __name__=="__main__":
    print("calender bot testing..............")
    today=datetime.datetime.now().strftime("%Y-%m-%d")
    print(today)
    print("\n--- Attempt 1: Booking for Basit (5:00 pM) ---")
    book1=book_appointment("basit","032425697202",today,"17:00")
    print(book1)
    print("\n--- Attempt 2: Booking for Ali (5:00 pM) ---")
    book2=book_appointment("Ali","030000000",today,"17:00")
    print(book2)