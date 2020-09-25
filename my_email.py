import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



# 交換いらがあったことを管理会社に依頼する
def email_notification(company_info_data, notification_data):
    message = Mail(
        from_email='oosiro708@gmail.com',
        to_emails=company_info_data['email'],
        subject='HouseQRからのお知らせです',
        html_content=(
                '「' + notification_data['property_name'] + '」の住人から、「' + notification_data['part_name'] + '」の交換依頼がありました。<br><br>'
                '下記リンクから詳細をご確認ください。<br>'
                'http://housewatcher.ryukyuupdate.com/propertytable<br>'
                )
        )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



# メールアドレス認証
def email_notification_certification(request_body_data):
    message = Mail(
        from_email='oosiro708@gmail.com',
        to_emails=request_body_data['email'],
        subject='【HouseQR】メールアドレスの認証',
        html_content=(
            'HouseQRからメールアドレス認証のお知らせです<br><br>'
            '下記URLをクリックしメールアドレス認証を完了してください<br>'
            'http://3.114.195.102:8080/propertytable/authemail?company_id=' + str(request_body_data['company_id'])
                )
        )
    
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)