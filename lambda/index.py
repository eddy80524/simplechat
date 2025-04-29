import json
import urllib.request

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))
        
        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        
        print("Processing message:", message)
        
        # Colabで立てたAPIのURL（ここを自分のものに変えてね）
        api_url = "https://xxx-xxx-xxx.ngrok-free.app/generate"
        
        # APIに送るデータ
        payload = json.dumps({"prompt": message}).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # APIリクエストを作成
        req = urllib.request.Request(api_url, data=payload, headers=headers)
        
        # APIリクエストを送信してレスポンスを受け取る
        with urllib.request.urlopen(req) as res:
            response_body = res.read()
            response_json = json.loads(response_body)
        
        print("API response:", json.dumps(response_json))
        
        # APIから返ってきたテキストを取得
        assistant_response = response_json['text']
        
        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response
            })
        }
        
    except Exception as error:
        print("Error:", str(error))
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }
