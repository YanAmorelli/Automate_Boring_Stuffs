import time
import json
import base64
from selenium import webdriver
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

file = open("variables_real.json", "r")
variables = json.load(file)
file.close()

sender_email=variables["sender_email"]
sender_password=variables["sender_password"]
recipient_email=variables["recipient_email"].split(",")

chrome_driver_path = variables["path"] + "chromewebdriver.exe"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")  
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

url = "https://www.inetsoft.com/evaluate/bi_visualization_gallery/dashboard.jsp?dbIdx=8"

driver.get(url)
driver.fullscreen_window()
time.sleep(10)
screenshot_path = variables["path"] + "screenshot.png"
driver.save_screenshot(screenshot_path)
driver.quit()

with open(screenshot_path, "rb") as screenshot_file:
    screenshot_data = screenshot_file.read()

screenshot_data_encoded = base64.b64encode(screenshot_data).decode("ascii")

for recipient in recipient_email:
    email_message = MIMEMultipart()
    email_message["Subject"] = "Visão relatorial de nosso dashboard de vendas"
    email_message["From"] = sender_email
    email_message["To"] = recipient

    html_message = f"""
    <html>
        <body>
            <h1>Visão relatorial de nosso dashboard de vendas</h1>
            </br>
            <p>Boa tarde, </p>
            <p>Segue o print de nosso dashboard de vendas:</p>
            </br>
            <img src="data:image/png;base64,{screenshot_data_encoded}" alt="Dashboard Screenshot" width="500" heigh="300">
            </br>
            </br>
            <p>Caso queira mais informações de nosso dashboard <a href="https://www.inetsoft.com/evaluate/bi_visualization_gallery/dashboard.jsp?dbIdx=8">clique aqui</a> ou me envie um email para discutirmos nossas estratégias.<p/>
            </br>
            <p>Atenciosamente,</p>
            <p>Yan L. Amorelli.</p>
        </body>
    </html>
    """

    email_message.attach(MIMEText(html_message, "html"))

    with SMTP_SSL("smtp.gmail.com") as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(email_message)

    print(f"Screenshot sent to {recipient}")

print("Screenshot captured and email sent successfully.")