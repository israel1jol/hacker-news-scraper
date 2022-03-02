import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

load_dotenv()
now = datetime.datetime.now()


content = ''


def extract_news(url):
    print('Extracting...')
    cnt = ''
    cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign' : ''})):
        cnt += ((str(i+1)+': '+tag.text+'\n'+'<br>')if tag.text != 'More' else '')
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += '<br>------<br>'
content += '<br><br>End of message'
content += '</body></html>'



SERVER = 'smtp.gmail.com'
PORT = 465
FROM = os.getenv('FROM')
TO = os.getenv('TO')
PASS = os.getenv('PASS')

msg = MIMEMultipart()
msg['Subject'] = 'Daily Dose News for ' + str(now.date()) + ' [Automated]'
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))


print("Initiating Server...")


server = smtplib.SMTP_SSL(SERVER, PORT)
server.set_debuglevel(0)
server.ehlo()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent')

server.quit()
  