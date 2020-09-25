import json
import boto3



client = boto3.client('connect')

def call_notification_part(company_info_data, notification_data):
    message = ('<speak><break time="0.5s"/>こちらは、<break time="0.3s"/>ハウスウォッチャーでございます<break time="0.5s"/>'
                 + str(notification_data['property_name']) + 'の<break time="0.2s"/>'+ str(notification_data['part_name']) +'の交換依頼がありました。<break time="0.5s"/>'
                '詳細につきましては、ハウスウォッチャーのウェブサイトをご確認ください<break time="0.5s"/></speak>')
    print(message)
    response = client.start_outbound_voice_contact(
        DestinationPhoneNumber='+818064907136',
        ContactFlowId='da193adf-e090-4e78-b25e-9acfd22d9195',
        InstanceId='094128ec-c902-4d91-abc7-5904a08a9e13',
        QueueId='3f43ecc6-73d9-4d7e-be88-bd540390a366',
        Attributes={
            'message': message
        }
    )
    return 


def call_notification_certification(request_body_data):
    response = client.start_outbound_voice_contact(
        DestinationPhoneNumber='+81' + str(request_body_data['phone_number'][1:20]),
        ContactFlowId='664cecb6-6432-4212-96f6-aa3ef6bd6f64',
        InstanceId='094128ec-c902-4d91-abc7-5904a08a9e13',
        QueueId='3f43ecc6-73d9-4d7e-be88-bd540390a366',
        Attributes={
            'company_id': request_body_data['company_id'],
            'company_name': request_body_data['company_name']
        }
    )
    return 