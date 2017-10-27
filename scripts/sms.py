from twilio.rest import Client
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("sms")
args = parser.parse_args()

# Your Account SID from twilio.com/console
account_sid = "AC6d42d0ac62804e75fa05b507b7ec0db6"
# Your Auth Token from twilio.com/console
auth_token  = "7a1c35503f8c13b21d5dac92c6ff55a3"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to = "+61419947250", 
    from_ = "+61476856529",
    body = args.sms)

print(message.sid)