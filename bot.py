import requests
import time

TWILIO_SID = "ACd31cba1f28b4e622a89dcc5e4b8513a4"
TWILIO_TOKEN = "e6ea9ca613383f6fb9d28c5097bd8082"
FROM = "whatsapp:+14155238886"
TO = "whatsapp:+972522583815"

seen = set()

def get_alerts():
    try:
        r = requests.get("https://www.oref.org.il/WarningMessages/alert/alerts.json",
            headers={"Referer": "https://www.oref.org.il/"},
            timeout=5)
        if r.status_code == 200 and r.text.strip():
            return r.json().get("data", [])
    except:
        pass
    return []

def send_whatsapp(msg):
    requests.post(
        f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json",
        data={"From": FROM, "To": TO, "Body": msg},
        auth=(TWILIO_SID, TWILIO_TOKEN))

while True:
    for city in get_alerts():
        if city not in seen:
            seen.add(city)
            send_whatsapp(f"🚨 צבע אדום - {city}")
    time.sleep(5)
