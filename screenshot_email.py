import time
from selenium import webdriver
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# Get variables saved in a txt file
file = open("variables_real.txt", "r")
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
    email_message = MIMEMultipart()
    email_message["Subject"] = "Sales report dashboard"
    email_message["From"] = sender_email
    email_message["To"] = recipient

    # Attach the screenshot to the email
    with open(screenshot_path, "rb") as screenshot_file:
        screenshot_data = screenshot_file.read()

    # Encode the screenshot data using Base64
    screenshot_data_encoded = base64.b64encode(screenshot_data).decode("ascii")


    html_message = f"""
    <html>
        <body>
            <h1>Sales Report Dashboard</h1>
            <p>Here is the sales report dashboard:</p>
            <img src="data:image/png;base64,{screenshot_data_encoded}" alt="Dashboard Screenshot">
        </body>
    </html>
    """
    # Attach the HTML message to the email
    email_message.attach(MIMEText(html_message, "html"))

    # Send the email
    with SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(email_message)

    print(f"Screenshot sent to {recipient}")

print("Screenshot captured and email sent successfully.")