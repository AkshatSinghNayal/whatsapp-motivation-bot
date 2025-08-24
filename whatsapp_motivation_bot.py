# =================================================================================================
# WhatsApp FAANG+DSA Motivation Bot (using Google Gemini API)
#
# Final, secure version for GitHub Actions.
# =================================================================================================

import os
import google.generativeai as genai
from twilio.rest import Client

# --- 1. SECURE CONFIGURATION: READS FROM ENVIRONMENT VARIABLES ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
RECIPIENT_WHATSAPP_NUMBER = os.environ.get("RECIPIENT_WHATSAPP_NUMBER")

# RECOMMENDED: Add this check to make your bot more robust.
if not all([GOOGLE_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, RECIPIENT_WHATSAPP_NUMBER]):
    print("FATAL ERROR: One or more required secrets are not set in the environment.")
    print("Please check your GitHub Repository Secrets.")
    exit(1)

# --- Configure the clients ---
genai.configure(api_key=GOOGLE_API_KEY)
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# --- 2. CORE FUNCTIONS ---

def generate_motivation_message():
    """Generates a motivational message using the Gemini API."""
    try:
        # Use the updated and stable model name 'gemini-1.0-pro'
        model = genai.GenerativeModel('gemini-1.0-pro')
        prompt = "Generate a savage, tough-love motivational message for a coder procrastinating on their FAANG grind. Keep it short, brutal, and to the point. Include hype emojis like 💀, 🔥, ⚔️, 💻."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating message from Gemini: {e}")
        return "Gemini API failed. No excuses. Solve 'Two Sum' and dominate today! 🔥"

def send_whatsapp_message(body):
    """Sends the message using the Twilio API."""
    try:
        message = client_twilio.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=body,
            to=RECIPIENT_WHATSAPP_NUMBER
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")


# --- 3. SCRIPT EXECUTION ---
if __name__ == "__main__":
    print("Generating motivational message...")
    motivational_message = generate_motivation_message()
    
    print("Sending message via WhatsApp...")
    send_whatsapp_message(motivational_.message)
    
    print("Bot has finished its run. 💀🔥⚔️")
