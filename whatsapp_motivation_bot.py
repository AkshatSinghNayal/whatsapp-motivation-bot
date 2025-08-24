# =================================================================================================
# WhatsApp FAANG+DSA Motivation Bot (using Google Gemini API)
#
# INSTRUCTIONS:
# 1. Install necessary Python libraries:
#    pip install google-generativeai twilio schedule
#
# 2. Replace the placeholder values below with your actual credentials:M8Z6C6TE6KF2PRZ7CWQPMGPB
#    - GOOGLE_API_KEY: Your secret API key from Google AI Studio (https://aistudio.google.com/app/apikey).
#    - TWILIO_ACCOUNT_SID: Your Account SID from the Twilio Console (https://www.twilio.com/console).
#    - TWILIO_AUTH_TOKEN: Your Auth Token from the Twilio Console.
#    - TWILIO_WHATSAPP_NUMBER: Your Twilio WhatsApp-enabled phone number (e.g., 'whatsapp:+14155238886').
#    - RECIPIENT_WHATSAPP_NUMBER: The recipient's WhatsApp number (e.g., 'whatsapp:+919999999999').
#
# 3. How to run the bot:
#    - Save this script as a Python file (e.g., whatsapp_motivation_bot_gemini.py).
#    - Run it from your terminal: python whatsapp_motivation_bot_gemini.py
#    - The script will run continuously and send a message every day at 7:00 AM local time.
#      Keep the terminal session alive or deploy it to a server for uninterrupted execution.
#
# =================================================================================================

import os

import time
import google.generativeai as genai
from twilio.rest import Client

# --- 1. CONFIGURATION: REPLACE WITH YOUR CREDENTIALS ---

# Google Gemini API Configuration
# Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey
# For better security, consider using environment variables.
# For example: os.environ.get("GOOGLE_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyAhbe20WS2t21IVCQ2VYAIaRzrUhfKLKps")
genai.configure(api_key=GOOGLE_API_KEY)

# Twilio API Configuration
# Find your Account SID and Auth Token at twilio.com/console
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "ACd5d2cb8e45375b13fdb51a8524a0dcf2")  # <-- REPLACE THIS
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "a883c7d9431d88e6dcf9e2a76e6c8089")  # <-- REPLACE THIS
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")  # <-- REPLACE THIS (e.g., 'whatsapp:+14155238886')
RECIPIENT_WHATSAPP_NUMBER = os.environ.get("RECIPIENT_WHATSAPP_NUMBER", "whatsapp:+919219426398") # <-- REPLACE THIS (e.g., 'whatsapp:+919999999999')

# Instantiate Twilio Client
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# --- 2. DYNAMIC MESSAGE GENERATION WITH GEMINI ---

def generate_motivation_message():
    model = genai.GenerativeModel('gemini-pro')
    prompt = """
    Generate a savage motivational message for a coder grinding FAANG interviews.
    Keep it short, harsh, and end with "dominate today!" + hype emojis.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") else response.candidates[0].content.parts[0].text.strip()

def send_whatsapp_message(body):
    client_twilio.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=body,
        to=RECIPIENT_WHATSAPP_NUMBER
    )

if __name__ == "__main__":
    msg = generate_motivation_message()
    send_whatsapp_message(msg)
    print("Motivation sent! 💀🔥⚔️")
