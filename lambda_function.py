from urllib import request, parse
import json
import base64
import io
import cgi
import boto3
import time
import ast
import my_call
import my_email



def lambda_handler(event, context):
    fp = io.BytesIO(base64.b64decode(event['body']))
    environ = {'REQUEST_METHOD': 'POST'}
    headers = {
        'content-type': event['headers']['content-type'],
        'content-length': event['headers']['content-length'],
    }
    
    form = cgi.FieldStorage(fp=fp, environ=environ, headers=headers)

    # ボディーを辞書型に変換
    request_body_data = {}
    for f in form.list:
        request_body_data[str(f.name)] = f.value
    
    # 取得したデータに「全角スペース」があったら半角スペースに変換する
    for key, val in request_body_data.items():
        request_body_data[key] = val.replace('\u3000', ' ')
    
    # URLパスを取得
    request_url_path = event['path']
    
    if request_url_path == '/api/notification/notification/part':
        notification_part(
            request_body_data = request_body_data,
        )
    elif request_url_path == '/api/notification/certification':
        notification_certification(
            request_body_data = request_body_data
        )
    return 0



# 会社情報を取得
def notification_certification(request_body_data):
    if request_body_data['certification_type'] == 'phone_number':
        my_call.call_notification_certification(
            request_body_data = request_body_data
        )
    elif request_body_data['certification_type'] == 'email_address':
        my_email.email_notification_certification(
            request_body_data = request_body_data
        )
    return 0


# 会社情報を取得
def notification_part(request_body_data):
    url = "http://api.housewatcher.ryukyuupdate.com/api/part/notification"
    data = {
        'id': request_body_data['id'],
        'part_name': request_body_data['part_name'],
        'part_status': request_body_data['part_status'],
        'property_id': request_body_data['property_id'],
        'property_name': request_body_data['property_name'],
    }
    post_form_data = parse.urlencode(data)
    post_form_headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_req = request.Request(url, data=post_form_data.encode(), method='POST')
    
    with request.urlopen(post_req) as response:
        response_body = response.read().decode("utf-8")
    
    # 文字列を辞書型に変換
    response_body = ast.literal_eval(response_body)
    
    # emailを送信する関数を実行
    if response_body['notification_email']:
        my_email.email_notification(
            company_info_data = response_body,
            notification_data = request_body_data
        )

    # 電話をかける関数を実行
    if response_body['notification_phone']:
        my_call.call_notification_part(
            company_info_data = response_body,
            notification_data = request_body_data
        )
    
    return 0


# 会社情報を取得（電話番号）
def get_company_info(request_body_data):
    url = "http://api.housewatcher.ryukyuupdate.com/api/part/notification"
    data = {
        'id': request_body_data['id'],
        'part_name': request_body_data['part_name'],
        'part_status': request_body_data['part_status'],
        'property_id': request_body_data['property_id'],
        'property_name': request_body_data['property_name'],
    }
    post_form_data = parse.urlencode(data)
    post_form_headers = {'content-type': 'application/x-www-form-urlencoded'}
    post_req = request.Request(url, data=post_form_data.encode(), method='POST')
    
    with request.urlopen(post_req) as response:
        response_body = response.read().decode("utf-8")
    
    company_info_data = ast.literal_eval(response_body)
    
    return company_info_data