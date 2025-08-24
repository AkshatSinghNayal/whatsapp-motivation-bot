import os
import sys
import google.generativeai as genai
from twilio.rest import Client

# --- 1. SECURE CONFIGURATION ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")
RECIPIENT_WHATSAPP_NUMBER = os.environ.get("RECIPIENT_WHATSAPP_NUMBER")

# --- 2. API AND SECRET VALIDATION ---
has_error = False
if not GOOGLE_API_KEY:
    print("FATAL ERROR: The GOOGLE_API_KEY secret is not set in your repository.", file=sys.stderr)
    has_error = True
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, RECIPIENT_WHATSAPP_NUMBER]):
    print("FATAL ERROR: One or more Twilio secrets are missing. Please check your repository secrets.", file=sys.stderr)
    has_error = True

if has_error:
    sys.exit(1)

# --- 3. CLIENT CONFIGURATION ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"FATAL ERROR: Failed to configure Google Gemini client. Your API key may be invalid. Error: {e}", file=sys.stderr)
    sys.exit(1)
    
client_twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# --- 4. CORE FUNCTIONS ---
def generate_motivation_message():
    """Generates a motivational message using the Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-1.0-pro-latest') # Using the latest model
        prompt = "Generate a savage, tough-love motivational message for a coder procrastinating on their FAANG grind. Keep it short, brutal, and to the point. Include hype emojis like 💀, 🔥, ⚔️, 💻."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"ERROR: Failed to generate message from Gemini API. This is often an API key or billing issue. Please check your Google Cloud project. Details: {e}", file=sys.stderr)
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
        print(f"ERROR: Failed to send WhatsApp message via Twilio. Check your Twilio credentials and phone numbers. Details: {e}", file=sys.stderr)
        sys.exit(1)

# --- 5. SCRIPT EXECUTION ---
if __name__ == "__main__":
    print("Generating motivational message...")
    motivational_message = generate_motivation_message()
    
    print("Sending message via WhatsApp...")
    # THIS IS THE FIX. The variable is correct.
    send_whatsapp_message(motivational_message)
    
    print("Bot has finished its run. 💀🔥⚔️")
