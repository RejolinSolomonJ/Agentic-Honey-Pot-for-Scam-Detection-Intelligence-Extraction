import requests
try:
    with open("connection_info.txt", "r") as f:
        content = f.read()
        url = content.split("from ")[1].strip() + "/api/v1/message"
    
    print(f"Checking URL: {url}")
    response = requests.post(url, json={"sessionId": "check", "message": {"sender":"user", "text":"ping", "timestamp":123}}, headers={"x-api-key": "secret"}, timeout=5)
    print(f"Status: {response.status_code}")
except Exception as e:
    print(f"Failed: {e}")
