import requests
import smtplib
import time
from bs4 import BeautifulSoup

#checks the availabilty of the graphics card for a specific URL on Caseking.de
def check_availability(URL):
    #my user agent
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    #for the rtx3080 graphics card, this class contains the availability
    availability = soup.find(class_="frontend_plugins_index_delivery_informations").get_text()
    return(availability)

#sends an email with the buy link (URL)
def send_mail(URL):
    #gmail handling
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    #login credentials (make sure to activate less secure apps or two fact auth)
    server.login('*yourmail*@gmail.com','*password*')
    #email text
    subject = 'RTX 3080 available'
    body = "The link "+ URL
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        '*sender*@gmail.com',
        '*recipient*@gmail.com',
        msg
    )

#pages to check, graphics card I wanted
urls = ['https://www.caseking.de/asus-geforce-rtx-3080-rog-strix-o10g-10240-mb-gddr6x-gcas-399.html',
        'https://www.caseking.de/gigabyte-aorus-geforce-rtx-3080-master-10g-10240-mb-gddr6x-gcgb-331.html',
        'https://www.caseking.de/zotac-gaming-geforce-rtx-3080-amp-holo-10240-mb-gddr6x-gczt-166.html',
        'https://www.caseking.de/msi-geforce-rtx-3080-gaming-x-trio-10g-10240-mb-gddr6x-gcmc-248.html',
        'https://www.caseking.de/asus-geforce-rtx-3080-rog-strix-10g-10240-mb-gddr6x-gcas-400.html',
        'https://www.caseking.de/zotac-gaming-geforce-rtx-3080-trinity-oc-10240-mb-gddr6x-gczt-167.html'
        ]

#I just want one card
found_card = False
while(not found_card):
    for url in urls:
        #unbekannt->unavailable, everything else means the item is available
        if check_availability(url)[0:9]!='unbekannt':
            send_mail(url)
            print('Card available: '+url+'\n')
            found_card = True
            break
        else:
            print('No card available')
            #checking every 60 seconds until I find a card
            time.sleep(60)