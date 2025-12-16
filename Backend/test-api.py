import requests

res = requests.post("http://localhost:8000/chat", json={"question": "What is physical AI"})
print(res.json())