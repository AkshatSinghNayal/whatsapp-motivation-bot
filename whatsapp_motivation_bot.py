import os
import sys
import google.generativeai as genai
from twilio.rest import Client

# --- 1. SECURE CONFIGURATION ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")  # e.g. +14155238886
RECIPIENT_WHATSAPP_NUMBER = os.environ.get("RECIPIENT_WHATSAPP_NUMBER")  # e.g. +91XXXXXXXXXX

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
        model = genai.GenerativeModel("models/gemini-1.5-flash")  # ✅ supported model
        prompt = "Write a long, relentless, in-your-face motivational message of 100–200 words for someone addicted "
    "to scrolling, games, and procrastination. Make it vivid, brutal, and impossible to ignore. "
    "Call out their laziness, show the consequences of wasting time, and contrast it with what winners do. "
    "Make them feel the urgency and the pressure—they must get up and start grinding immediately. "
    "End the message with a sharp, actionable DSA advice for improving coding skills. "
    "Use hype emojis like 💀🔥⚔️💻, but make the message long, intense, and multi-paragraph."

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"ERROR: Failed to generate message from Gemini API. Details: {e}", file=sys.stderr)
        return "Gemini API failed. No excuses. Solve 'Two Sum' and dominate today! 🔥"

def send_whatsapp_message(body):
    """Sends the message using the Twilio API."""
    try:
        message = client_twilio.messages.create(
            from_=f"whatsapp:{TWILIO_WHATSAPP_NUMBER}",
            body=body,
            to=f"whatsapp:{RECIPIENT_WHATSAPP_NUMBER}"
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"ERROR: Failed to send WhatsApp message via Twilio. Details: {e}", file=sys.stderr)
        sys.exit(1)

# --- 5. SCRIPT EXECUTION ---
if __name__ == "__main__":
    print("Generating motivational message...")
    motivational_message = generate_motivation_message()
    
    print("Sending message via WhatsApp...")
    send_whatsapp_message(motivational_message)
    
    print("Bot has finished its run. 💀🔥⚔️")
