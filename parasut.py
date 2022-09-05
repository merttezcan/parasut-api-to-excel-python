import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
user = os.getenv('user')
password = os.getenv('password')

invoice_id = input("Fatura ID: ")

access_point = 'https://api.parasut.com/oauth/token'
grant_type = 'password'

headersx = {'Content-Type': 'application/x-www-form-urlencoded'}

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

data = {'grant_type': grant_type,
        'username': user,
        'password': password}

resp = None

def parasut_token():
    try:
        resp = requests.post(access_point, auth=auth, data=data, headers=headersx, timeout=5)
    except requests.exceptions.ConnectionError:
        exit(1)

    if resp.status_code == 200:
        resp = json.loads(resp.text)
        if 'access_token' in resp:
            my_token = resp['access_token']
            #print(my_token)
            url = "https://api.parasut.com/v4/519727/sales_invoices/" + invoice_id + "?include=contact,details.product"
            payload={}
            headers = {
            'Authorization': 'Bearer ' + my_token
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            #print(headers)

            #print(response.text)

            output = response.json()
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=4)

            exit(0)
    else:
        print("Token alınamadı. Giriş bilgilerini kontrol edin.")  

        exit(1)

    

if __name__ == "__main__":
    parasut_token()
