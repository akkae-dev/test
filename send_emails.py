import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

# Hardcoded credentials (replace with your actual details)
EMAIL_ADDRESS = 'contact@akkae.cc'
EMAIL_PASSWORD = 'Nz065czPHg9MuTx'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1368778279544426580/K9z-YfhcxKfdF7TG1_dFSLXdGRNQWHkdABTipX4h1h8bqn2xeIJTTlvPTLjqmTmqAXft'
SMTP_SERVER = 'mail.privateemail.com'
SMTP_PORT = 465  # SSL

def send_email(recipient_email, username, uuid1, uuid2):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = 'Quick Inquiry'

    body = f"""\
Hi,

I hope you're doing well!

I came across your Minecraft username and was wondering if you'd ever consider parting with the account. I know this might be unexpected, but I thought I'd reach out and ask politely.

Also just to let you know, your username is tied to an email within a collection of public pastes which is how people have gotten your contact info over the years (including me). I can show you where these pastes are if you'd like & how you'd get your info off of them.

If you're not interested, no worries at all — just reply to me and I won't reach out again.

Thanks for your time!

Best regards,  
Akkae
"""
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        server.quit()
        log_to_discord(f"✅ Email sent successfully to {recipient_email}")
        notify_discord(username, uuid1, uuid2, recipient_email, "success")
    except Exception as e:
        log_to_discord(f"❌ Failed to send email to {recipient_email}. Error: {str(e)}")
        notify_discord(username, uuid1, uuid2, recipient_email, "failure")

def log_to_discord(message):
    payload = {
        "content": message,
    }
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code == 204 or res.status_code == 200:
            print(f"✅ Log sent to Discord: {message}")
    except Exception as e:
        print(f"❌ Failed to log to Discord: {str(e)}")

def notify_discord(username, uuid1, uuid2, recipient_email, status):
    status_message = "Email sent successfully" if status == "success" else "Failed to send email"
    payload = {
        "content": f"📧 {status_message} to {recipient_email}",
        "embeds": [
            {
                "title": "Email Details",
                "fields": [
                    {"name": "Username", "value": username, "inline": True},
                    {"name": "UUID", "value": uuid1, "inline": True},
                    {"name": "UUID2", "value": uuid2, "inline": True},
                    {"name": "Email", "value": recipient_email, "inline": True}
                ]
            }
        ]
    }
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code == 204 or res.status_code == 200:
            print(f"✅ Discord notified about {status} email.")
    except Exception as e:
        print(f"❌ Failed to notify Discord: {str(e)}")

def main():
    with open('usernames.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 4:
                username, uuid1, uuid2, email = parts
                send_email(email, username, uuid1, uuid2)
            else:
                log_to_discord(f"⚠️ Skipping invalid line: {line.strip()}")

if __name__ == "__main__":
    main()
