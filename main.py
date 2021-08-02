import requests
import os
import smtplib
import pandas
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")
account_sid = ""
auth_token = os.environ.get("AUTH_TOKEN")

MY_EMAIL = "@gmail.com"
MY_PASSWORD = os.environ.get("GM_PWD")

weather_params = {
    "lat": ,
    "lon": ,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:11]

sun_params = {
    "lat": ,
    "lng": ,
}

sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=sun_params)
sun_response.raise_for_status()
sunrise_sunset_data = sun_response.json()
sunrise = sunrise_sunset_data["results"]["sunrise"]
sunset = sunrise_sunset_data["results"]["sunset"]


def convert_time(a):
    sun_split = a.split(":")
    hours = int(a.split(":")[0]) + 8 - 12
    minutes = sun_split[1]
    if a == sunrise:
        return f"{hours}:{minutes} AM"
    elif a == sunset:
        return f"{hours}:{minutes} PM"


h = []
temperature_c = []
feels_like = []
description = []
data_dict = {
    "Time": h,
    "Temperature°C": temperature_c,
    "Feels Like°C": feels_like,
    "Description": description,
}
hour = 7
for hourly_data in weather_slice:
    hour += 1
    if hour < 10:
        hour_info = str(f"0{hour}00hrs")
    else:
        hour_info = str(f"{hour}00hrs")
    h.append(hour_info)
    temperature_c.append(f"{round((hourly_data['temp'] - 273.15), 2)}°C")
    feels_like.append(f"{round((hourly_data['feels_like'] - 273.15), 2)}°C")
    description.append(hourly_data["weather"][0]["description"].title())
data = pandas.DataFrame(data_dict)
print(data)

recipients = ["@gmail.com", "@yahoo.com",
              "@yahoo.com", "@gmail.com",
              "@yahoo.com"]
email_list = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg["Subject"] = f"Today's Weather Forecast! Sunrise@{convert_time(sunrise)} Sunset@{convert_time(sunset)}"
msg["From"] = formataddr((str(Header(" ", "utf-8")), MY_EMAIL))

html = """\
<html>
  <head></head>
  <body>
    {0}
  </body>
</html>
""".format(data.to_html())

part1 = MIMEText(html, 'html')
msg.attach(part1)

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(msg["From"], email_list, msg.as_string())
