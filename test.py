import asyncio
import json

import websockets


async def main():
    # WebSocketエンドポイントの設定
    ws_endpoint = "ws://localhost:8080/realtime"

    # 接続を開始
    async with websockets.connect(ws_endpoint) as websocket:
        # セッションを開始
        await websocket.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "turn_detection": {"type": "server_vad"},
                    },
                }
            )
        )

        # サーバーからの 'session.created' メッセージを待機
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "session.created":
                print("セッションが作成されました")
                break

        # サーバーからの 'session.updated' メッセージを待機
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "session.updated":
                print("セッションが更新されました")
                break

        # 会話を開始
        await websocket.send(
            json.dumps(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "こんにちは！今日の調子はどうですか？",
                            }
                        ],
                    },
                }
            )
        )

        # サーバーからの 'conversation.item.created' メッセージを待機
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "conversation.item.created":
                print("会話が開始されました")
                break

        # メッセージを送信
        await websocket.send(
            json.dumps(
                {
                    "type": "response.create",
                    "response": {
                        "modalities": ["audio", "text"],
                        "instructions": "ユーザーをサポートしてください。",
                        "voice": "echo",
                    },
                }
            )
        )

        # サーバーからの 'response.created' メッセージを待機
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "response.created":
                print("レスポンスが作成されました")
                break

        # サーバーからの 'response.done' メッセージを待機
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            if data["type"] == "response.done":
                print("レスポンスが完了しました")
                break
            elif data["type"] == "response.audio_transcript.delta":
                print(data["delta"])
            elif data["type"] == "response.audio_transcript.done":
                print(data["transcript"])
            elif data["type"] == "response.audio.delta":
                print(data["delta"])


# 実行
if __name__ == "__main__":
    asyncio.run(main())
