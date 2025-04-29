# lambda/index.py

import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    # 1. 環境変数から FastAPI の URL を取得
    api_url = os.environ.get("MODEL_API_URL")
    if not api_url:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "環境変数 MODEL_API_URL が設定されていません"})
        }

    # 2. リクエストボディをパースして user message を取り出す
    try:
        body = json.loads(event.get("body", "{}"))
        message = body.get("message", "")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "body が JSON ではありません"})
        }

    # 3. FastAPI に投げる JSON を作成
    payload = {"message": message}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    # 4. FastAPI に POST してレスポンスを受け取る
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp_text = resp.read().decode("utf-8")
            result = json.loads(resp_text)
            # FastAPI 実装に合わせてキーを読み替え
            answer = result.get("response") or result.get("assistant_response")
            if answer is None:
                raise ValueError("レスポンスに 'response' フィールドがありません")
    except Exception as e:
        # ネットワークエラーや JSON 解析エラー時はこちら
        answer = f"エラー: {e}"

    # 5. Lambda のレスポンス形式に整形して返す
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "response": answer
        })
    }
