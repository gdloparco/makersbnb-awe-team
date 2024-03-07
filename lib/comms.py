# file mailgun.py
# This file stores information regarding the mailgun emailing 
# functions for MakersBnB
import requests


# MakersBnB Mailgun API key and domain
MAILGUN_API_KEY = 'ae881b8406e640763bfdde827edecbbf-2c441066-2698ec22'
MAILGUN_DOMAIN = 'sandbox48b81c47f2e24b7591d704aedfb22efe.mailgun.org'


class EmailManager():

    def __init__(self):
        pass

    def send_email(self, to, subject, text):
        return requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={"from": "MakersBnB <series4000kryten@gmail.com>",
                  "to": to,
                  "subject": subject,
                  "text": text})

# if __name__ == "__main__":
#     to = "series4000kryten@gmail.com"
#     subject = "Test Email"
#     text = "This is a test email sent from Mailgun."
#     response = send_email(to, subject, text)
#     print(response.text)