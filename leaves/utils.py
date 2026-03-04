from twilio.rest import Client  # <--- Added this import

def send_leave_sms(receiver_number, student_name):
    account_sid = 'ACc17dd3ab5aa9ad34cb44a6f7814ef44c' 
    auth_token = '957ce5eed0fce12ed90b9bf10d60d530'   
    twilio_number = '+18703374991' 

    try:
        # Use uppercase 'Client' here
        client = Client(account_sid, auth_token) 
        message = client.messages.create(
            body=f"School Alert: {student_name} is absent today.",
            from_=twilio_number,
            to=receiver_number 
        )
        print(f"✅ SUCCESS! SID: {message.sid}")
        return True
    except Exception as e:
        # This will tell us if it's a 'unverified number' or 'auth' error
        print(f"❌ TWILIO ERROR: {e}") 
        return False