========================================================================
             AI APPOINTMENT BOOKING BOT - SETUP GUIDE
========================================================================

Thank you for choosing the AI Appointment Bot. This intelligent system manages 
patient inquiries via a Knowledge Base (RAG) and books real-time appointments 
directly into your Google Calendar.

Please follow the steps below to set up and run the bot on your system.

------------------------------------------------------------------------
1. PREREQUISITES
------------------------------------------------------------------------
- Python 3.10 or higher installed on your system.
- A Google Cloud Service Account (credentials.json).
- An OpenAI API Key.

------------------------------------------------------------------------
2. INSTALLATION
------------------------------------------------------------------------
1. Unzip the project folder.
2. Open your terminal (Command Prompt/PowerShell).
3. Navigate to the project folder:
   cd ai_appointment_bot

4. (Optional but Recommended) Create a Virtual Environment:
   python -m venv venv
   
   - To activate on Windows: venv\Scripts\activate
   - To activate on Mac/Linux: source venv/bin/activate

5. Install required libraries:
   pip install -r requirements.txt

------------------------------------------------------------------------
3. CONFIGURATION (IMPORTANT)
------------------------------------------------------------------------
You need to set up your keys and credentials for the bot to work.

A. GOOGLE CREDENTIALS:
   - Place your Google Service Account file named 'credentials.json' 
     inside the main project folder.

B. ENVIRONMENT VARIABLES:
   - Create a new file named '.env' in the main folder.
   - Copy and paste the text below into the file and fill in your details:

   # --- .env File Content Start ---
   
   # 1. Your OpenAI API Key (Required for the Brain)
   OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx"

   # 2. Google Calendar Settings
   # Put your actual Gmail address here (e.g., doctor@gmail.com)
   GOOGLE_CALENDAR_ID="your_email@gmail.com"

   # 3. Timezone Settings
   # Select your region (e.g., Asia/Karachi, Asia/Dubai, America/New_York)
   TIMEZONE="Asia/Karachi"

   # --- .env File Content End ---

------------------------------------------------------------------------
4. GOOGLE CALENDAR PERMISSIONS
------------------------------------------------------------------------
For the bot to write appointments to your calendar, you must share it:

1. Open your 'credentials.json' file and copy the "client_email" address 
   (e.g., ai-bot@project-id.iam.gserviceaccount.com).
2. Go to Google Calendar (calendar.google.com).
3. Go to Settings > Share with specific people.
4. Click "Add people" and paste the Service Account email.
5. **CRITICAL:** Set permissions to "Make changes to events".

------------------------------------------------------------------------
5. HOW TO RUN THE SERVER
------------------------------------------------------------------------
1. Open your terminal in the project folder.
2. Run the following command:
   python api.py

3. If successful, you will see:
   "Uvicorn running on http://127.0.0.1:8000"

------------------------------------------------------------------------
6. HOW TO TEST (CHAT WIDGET)
------------------------------------------------------------------------
1. Ensure the server (api.py) is running in the background.
2. Locate the file named 'test.html' in the folder.
3. Double-click to open it in your browser (Chrome/Edge).
4. Click the Chat Icon at the bottom right to start booking!

------------------------------------------------------------------------
7. CUSTOMIZATION (DATA)
------------------------------------------------------------------------
To update the bot's knowledge (Fees, Timings, Address):
1. Go to the 'data' folder.
2. Open 'faqs.txt'.
3. Edit the text and save. The bot will automatically learn the changes.

..........How to Generate Your credentials.json File......................
Go to Google Cloud Console:
Visit console.cloud.google.com and create a New Project.
Enable API:
Search for "Google Calendar API" and click Enable.
Create Service Account:
Go to Credentials > Create Credentials > Service Account.
Give it a name (e.g., bot-admin) and click Done.
Download JSON Key:
Click on your newly created Service Account (email address).
Go to the "Keys" tab.
Click Add Key > Create new key > Select JSON.
A file will download. Rename it to credentials.json and place it in the project root folder.
🔴 CRITICAL STEP: Share Calendar:
Copy the Service Account Email (e.g., bot-admin@project-id.iam.gserviceaccount.com).
Open your Google Calendar (in browser).
Go to Settings and sharing for your specific calendar.
Scroll to "Share with specific people".
Click Add people, paste the email, and set permission to "Make changes to events".
========================================================================
contect: +923243497292
gmail: hammadahmed12360@gmail.com
========================================================================