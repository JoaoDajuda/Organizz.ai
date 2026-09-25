import requests

headers = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZXhwIjoxNzg3NzQ0MTgyfQ.XAq9JYmyEvK5dSqCdC4tvVrnsslF2ok2dBoMXtoO-go"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(requisicao)
print(requisicao.json())