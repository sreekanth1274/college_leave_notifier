from twilio.rest import Client
import os

def send_leave_sms(receiver_number, student_name):
    # 1. Try to get keys from Render environment variables
    # 2. If they don't exist, use the strings as a backup
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', 'ACc17dd3ab5aa9ad34cb44a6f7814ef44c')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '957ce5eed0fce12ed90b9bf10d60d530')
    twilio_number = '+18703374991' 

    # DEBUG: This will show up in your Render Logs
    print(f"DEBUG: Attempting SMS to {receiver_number} for {student_name}...", flush=True)

    try:
        client = Client(account_sid, auth_token) 
        message = client.messages.create(
            body=f"School Alert: {student_name} is absent today.",
            from_=twilio_number,
            to=receiver_number 
        )
        print(f"✅ SUCCESS! SID: {message.sid}", flush=True)
        return True
    except Exception as e:
        # This will now definitely show up in Render Logs
        print(f"❌ TWILIO ERROR: {str(e)}", flush=True) 
        return False