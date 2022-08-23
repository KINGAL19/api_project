import requests
from datetime import datetime
import os
import smtplib

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude


def is_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    print('latitude: ', iss_latitude, 'longitude: ', iss_longitude)
    if abs(MY_LAT - iss_latitude) < 5 and abs(MY_LONG - iss_longitude) < 5:
        return True
    else:
        return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print('日出~日落:', sunrise, '~', sunset)
    time_now = datetime.now()
    if time_now.hour > sunset or time_now.hour < sunrise:
        return True
    else:
        return False


def send_email():
    EMAIL = os.getenv('email')
    PASSWORD = os.getenv('password_password')
    TOMAIL = os.getenv['emailTo']
    content = f"Subject: SEE THE SKY!\n\nISS is close to you, To see the sky."
    print(content)
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=TOMAIL, msg=content)


if is_overhead() and is_dark():
    send_email()
