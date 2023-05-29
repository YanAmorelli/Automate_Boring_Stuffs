import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from smtplib import SMTP_SSL
from email.message import EmailMessage

# Set up the Chrome driver options
#chrome_options = Options()
#chrome_options.add_argument("--headless=new")  # Run Chrome in headless mode (no GUI)

# Set the path to your Chrome driver executable
chrome_driver_path = "file name with absolute path of chrome driver"

# Create a new Chrome driver instance
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Website URL to capture
url = "https://www.inetsoft.com/evaluate/bi_visualization_gallery/dashboard.jsp?dbIdx=8"

# Load the webpage
driver.get(url)
time.sleep(5)
screenshot_path = "Path_to_save_photo/screenshot.png"
driver.save_screenshot(screenshot_path)
driver.quit()

# Email configuration
sender_email = "sender_email@gmail.com"
sender_password = "gmail_auth_code"
recipient_email = "recipient_email@gmail.com"

# Create an EmailMessage object
email_message = EmailMessage()
email_message["Subject"] = "Sales report dashboard"
email_message["From"] = sender_email
email_message["To"] = recipient_email

# Attach the screenshot to the email
with open(screenshot_path, "rb") as screenshot_file:
    screenshot_data = screenshot_file.read()
    email_message.add_attachment(screenshot_data, maintype="image", subtype="png", filename="screenshot.png")

# Send the email
with SMTP_SSL("smtp.gmail.com") as smtp:
    smtp.login(sender_email, sender_password)
    smtp.send_message(email_message)

print("Screenshot captured and email sent successfully.")