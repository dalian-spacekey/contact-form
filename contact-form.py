import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import textwrap
import os

adminMailAddress = os.environ['MAIL_ADDRESS']

def lambda_handler(event, context):

    try:
        msgToUser = createMessageToUser(event)
        msgToAdmin = createMessageToAdmin(event)

        server = smtplib.SMTP(os.environ['MAIL_SERVER'], os.environ['PORT'])
        server.starttls()
        server.login(os.environ['ACCOUNT'], os.environ['PASSWORD'])
        server.send_message(msgToUser)
        server.send_message(msgToAdmin)
        server.close()
        
        return {
            'statusCode': 200
        }
    except Exception as e:
        return { 
            'statusCode': 500,
            'body': e
        }


def createMessageToUser(event):
    body = textwrap.dedent(f'''
        お問い合わせありがとうございます。

        お名前：
        {event['name']}

        フリガナ：
        {event['furigana']}

        法人名：
        {event['company']}

        メールアドレス：
        {event['email']}

        電話番号：
        {event['tel']}

        お問い合わせ種別：
        {event['category']}

        お問い合わせ内容：
        {event['content']}
''').strip()

    msg = MIMEText(body)
    msg['Subject'] = 'お問い合わせありがとうございます'
    msg['From'] = adminMailAddress
    msg['To'] = '{} 様 <{}>'.format(event['name'], event['email'])
    msg['Date'] = formatdate()
    
    return msg

def createMessageToAdmin(event):
    body = textwrap.dedent(f'''
        この度はお問い合わせありがとうございます。
        いただいた情報は以下の通りです。

        お名前：
        {event['name']}

        フリガナ：
        {event['furigana']}

        法人名：
        {event['company']}

        メールアドレス：
        {event['email']}

        電話番号：
        {event['tel']}

        お問い合わせ種別：
        {event['category']}

        お問い合わせ内容：
        {event['content']}
''').strip()

    print(body)
    msg = MIMEText(body)
    msg['Subject'] = 'サイトからの問い合わせ'
    msg['From'] = '{} <{}>'.format(event['name'], event['email'])
    msg['To'] = adminMailAddress
    msg['Date'] = formatdate()
    
    return msg