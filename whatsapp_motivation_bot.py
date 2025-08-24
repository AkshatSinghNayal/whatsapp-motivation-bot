# =================================================================================================
# WhatsApp FAANG+DSA Motivation Bot (using Google Gemini API)
#
# Final, secure version for GitHub Actions.
# =================================================================================================

import os
import sys
import google.generativeai as genai
from twilio.rest import Client

# --- 1. SECURE CONFIGURATION: READS FROM ENVIRONMENT VARIABLES ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
RECIPIENT_WHATSAPP_NUMBER = os.environ.get("RECIPIENT_WHATSAPP_NUMBER")

# --- Let's add a check to see if the Google key is present ---
if not GOOGLE_API_KEY:
    print("FATAL ERROR: GOOGLE_API_KEY is not set. The script cannot run.")
    sys.exit(1)

# --- Configure the clients ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"FATAL ERROR: Failed to configure Google Gemini client. Your API key may be invalid. Error: {e}")
    sys.exit(1)
    
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# --- 2. CORE FUNCTIONS ---

def generate_motivation_message():
    """Generates a motivational message using the Gemini API."""
    try:
        # Using the correct, stable model name
        model = genai.GenerativeModel('gemini-1.0-pro')
        prompt = "Generate a savage, tough-love motivational message for a coder procrastinating on their FAANG grind. Keep it short, brutal, and to the point. Include hype emojis like 💀, 🔥, ⚔️, 💻."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        # This will now give us a much more precise error message
        print(f"ERROR: Failed to generate message from Gemini API. Please check your Google Cloud project settings and API key permissions. Details: {e}")
        # Return a fallback message so the script can still try to send something
        return "Gemini API failed. No excuses. Solve 'Two Sum' and dominate today! 🔥"

def send_whatsapp_message(body):
    """Sends the message using the Twilio API."""
    try:
        # Check if any of the Twilio secrets are missing
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, RECIPIENT_WHATSAPP_NUMBER]):
            print("FATAL ERROR: One or more Twilio secrets are missing. Cannot send WhatsApp message.")
            sys.exit(1)
            
        message = client_twilio.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=RECIPIENT_WHATSAPP_NUMBER
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"ERROR: Failed to send WhatsApp message via Twilio. Please check your Twilio credentials. Details: {e}")
        sys.exit(1)


# --- 3. SCRIPT EXECUTION ---
if __name__ == "__main__":
    print("Generating motivational message...")
    motivational_message = generate_motivation_message()
    
    print("Sending message via WhatsApp...")
    # THIS IS THE FIX: Changed 'motivational_.message' to 'motivational_message'
    send_whatsapp_message(motivational_message)
    
    print("Bot has finished its run. 💀🔥⚔️")
