from aiohttp import web
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

from middleware import RTMiddleTier

# 環境変数の取得
load_dotenv()
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")

if endpoint is None or deployment is None or api_key is None:
    raise ValueError("One or more environment variables are not set")

# RTMiddleTierのインスタンスを作成
rt_middle_tier = RTMiddleTier(
    endpoint=endpoint,
    deployment=deployment,
    credentials=AzureKeyCredential(api_key),
)

# aiohttpのアプリケーションを作成&アタッチ
app = web.Application()
rt_middle_tier.attach_to_app(app, "/realtime")

# サーバーを起動
web.run_app(app, host="0.0.0.0", port=8080)
