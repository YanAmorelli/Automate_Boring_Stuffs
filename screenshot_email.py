import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from smtplib import SMTP_SSL
from email.message import EmailMessage

# Get variables saved in a txt file
file = open("variables.txt", "r")
variables = file.readlines()
file.close()

for index, item in enumerate(variables):
    variables[index] = item.split("=")[1].replace("\n", "").rstrip()

path_web_driver=variables[0]
path_screenshot_photo=variables[1]
sender_email=variables[2]
sender_password=variables[3]
recipient_email=variables[4].split(",")

# Set the path to your Chrome driver executable
chrome_driver_path = path_web_driver

# Create a new Chrome driver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Website URL to capture
url = "https://www.inetsoft.com/evaluate/bi_visualization_gallery/dashboard.jsp?dbIdx=8"

# Load the webpage
driver.get(url)
time.sleep(10)
screenshot_path = path_screenshot_photo + "screenshot.png"
driver.save_screenshot(screenshot_path)
driver.quit()

# Create an EmailMessage object
for recipient in recipient_email:
    email_message = EmailMessage()
    email_message["Subject"] = "Sales report dashboard"
    email_message["From"] = sender_email
    email_message["To"] = recipient

    # Attach the screenshot to the email
    with open(screenshot_path, "rb") as screenshot_file:
        screenshot_data = screenshot_file.read()
        email_message.add_attachment(screenshot_data, maintype="image", subtype="png", filename="screenshot.png")

    # Send the email
    with SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(email_message)

    print(f"Screenshot sent to {recipient}")

print("Screenshot captured and email sent successfully.")