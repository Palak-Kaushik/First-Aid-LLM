from twilio.rest import Client

# Ngrok URL and Twilio voice URL
ngrok_url = "ngrok_url"
voice_url = f"{ngrok_url}/voice"

# Twilio credentials
account_sid = 'twilio_sid'
auth_token = 'twilio_authtoken'
client = Client(account_sid, auth_token)

# Create a new call using the ngrok URL
call = client.calls.create(
    url=voice_url,  
    to='phone no',  # your phone number
    from_='phone no'  #  your Twilio number
)

print("Call SID:", call.sid)
