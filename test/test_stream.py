import asyncio
import aiohttp
import json

async def test_streaming():
    url = "http://localhost:8010/ollama/chat/stream"
    data = {
        "dog_id": 1,
        "message": "안녕하세요"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")
            
            if response.status == 200:
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        try:
                            data = json.loads(line_str[6:])
                            if 'content' in data:
                                print(f"Content: {data['content']}", end='', flush=True)
                            if data.get('done'):
                                print("\n=== 스트리밍 완료 ===")
                                break
                        except json.JSONDecodeError:
                            print(f"JSON 파싱 오류: {line_str}")
            else:
                error_text = await response.text()
                print(f"Error: {error_text}")

if __name__ == "__main__":
    asyncio.run(test_streaming()) 