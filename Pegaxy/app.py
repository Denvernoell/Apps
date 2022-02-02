# from email.policy import default
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import streamlit as st
# from send_email import email_alert


# from my_secrets import username, app_password
import smtplib
from email.message import EmailMessage


def email_alert(to, subject, body, email='personal'):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['to'] = to

    # From denvernoell@gmail.com
    if email == 'personal':

        msg['from'] = username
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

    # From apps@denvernoell.com
    elif email == 'apps':
        msg['from'] = 'apps@denvernoell.com'
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(username, app_password)
    server.send_message(msg)
    server.quit()


class Store:
    def __init__(self, driver):

        self.driver = driver
        self.num_horses = len(driver.find_elements(
            'class name', 'content-name-title'))
        self.horses = [Horse(driver, i) for i in range(
            self.num_horses-1) if type(Horse(driver, i).price) == int]


class Horse:
    def __init__(self, driver, i):
        self.driver = driver
        price = (driver.find_elements(
            'class name', 'content-name-title')[i].text)
        name = (driver.find_elements('class name', 'item-info-title')[i].text)
        rarity, breed_type, gender = (driver.find_elements(
            'class name', 'item-info-meta')[i].text).replace(' ', '').split('•')

        auction_link = driver.find_elements('tag name', 'a')[
            i].get_attribute('href')

        try:
            self.price = int(price.replace(',', ''))
        except:
            self.price = price
        self.name = name
        self.rarity = rarity
        self.breed_type = breed_type
        self.gender = gender
        self.auction_link = auction_link


# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import markdown
# import plyer
option = webdriver.ChromeOptions()
option.add_argument('--headless')
# option.add_argument('--no-sandbox')
# option.add_argument('--disable-dev-sh-usage')


s = Service(r"D:\Drive\Blog\Dependencies\chromedriver.exe")
# driver = webdriver.Chrome(service=s)
driver = webdriver.Chrome(
    executable_path=r"D:\Drive\Blog\Dependencies\chromedriver.exe",
    options=option)


st.set_page_config(
    page_title="Pegaxy Checker",
    page_icon=":horse:",
)
# menu_items={
#     'Get Help': 'https://www.extremelycoolapp.com/help',
#     'Report a bug': "https://www.extremelycoolapp.com/bug",
#     'About': "# This is a header. This is an *extremely* cool app!"
# }


st.title('Pegaxy Checker')
p_genders = ['Male', 'Female']
p_breeds = ['All', 'Foundling', 'Legendary', 'Epic', 'Rare', 'Pacer']
p_rarity = ['Zon', 'Hoz', 'Compono', 'Klin']

c_genders = st.multiselect('Gender', p_genders, default=p_genders)
c_breeds = st.multiselect('Breed', p_breeds, default=p_breeds)
c_rarity = st.multiselect('Rarity', p_rarity, default=p_rarity)
max_price = st.number_input("Max Price (USDT)", value=1000, step=1)
my_email = st.text_input("Email")
# my_email = "Denvernoell@gmail.com"

URL = 'https://play.pegaxy.io/marketplace?sortBy=price&sortType=ASC'

if st.button("Check"):

    # start_time = time.time()
    # while (time.time() - start_time) < (60 * 60):
    found = False
    while found == False:
        driver.get(URL)
        # This will look for 5 seconds for any element to appear
        driver.implicitly_wait(5)

        S = Store(driver)
        # print(len(S.horses))

        def check_criteria(horse):
            return (horse.gender in c_genders) and (horse.breed_type in c_breeds) and (horse.rarity in c_rarity) and (horse.price <= max_price)

        available_horses = [
            horse for horse in S.horses if check_criteria(horse)]
        if len(available_horses) > 0:
            message = "Horse List"
            for horse in available_horses:

                #                 # Markdown
                #                 markdown_msg += f"""Name: {horse.name}

                # Price: ${horse.price}

                # Link: (Here)[{horse.auction_link}]
                #                 """

                # Text
                message += "\n" + "\n" + \
                    (f"""Name: {horse.name}
Price: ${horse.price}
Link: {horse.auction_link}
---   
""")
            # st.markdown(message)

            #     plyer.notification.notify(
            # 	title='Pega For You',s
            # 	message='This Pega meets your criteria',
            # 	app_icon='pegasus.ico',
            # 	timeout=10
            # )

            # # Markdown
            # multipart_msg = MIMEMultipart("alternative")
            # html = markdown.markdown(markdown_msg)

            # part1 = MIMEText(markdown_msg, "plain")
            # part2 = MIMEText(html, "html")

            # multipart_msg.attach(part1)
            # multipart_msg.attach(part2)

            # message = multipart_msg.as_string()

            # Send
            email_alert(
                to=my_email,
                subject="Pegas for you",
                body=message)

            found = True
            st.success("Message sent")

        time.sleep(60 * 5)
