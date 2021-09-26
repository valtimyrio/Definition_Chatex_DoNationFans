import requests
import json
import datetime


class Chatex:
    def __init__(self):
        self.last_access_datetime = ""
        self.access_token = ""
        self.fresh_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0NGQ5ZmZmZS1jMzI3LTQwNjEtYWU1My1kNmM4ZmY1YjA1ZWEiLCJpYXQiOjE2MzI1NzQ4NDIsImlzcyI6ImNoYXRleC1pZCIsInN1YiI6InVzZXIiLCJ1aWQiOjE0MzksInZlciI6MSwicmVzIjpbMV0sInR5cCI6MSwic2NvcGVzIjpbImNvcmU6cmVhZCIsInByb2ZpbGU6cmVhZCIsInByb2ZpbGU6YWN0aW9uIiwiYXV0aDphY3Rpb24iLCJjaGF0ZXhfcGF5OnJlYWQiLCJjaGF0ZXhfcGF5OmFjdGlvbiIsImV4Y2hhbmdlOnJlYWQiLCJleGNoYW5nZTphY3Rpb24iLCJub3RpZmljYXRpb25zOnJlYWQiLCJub3RpZmljYXRpb25zOmFjdGlvbiIsIndhbGxldDpyZWFkIiwid2FsbGV0OmFjdGlvbiIsImFmZmlsaWF0ZTpyZWFkIiwiYWZmaWxpYXRlOmFjdGlvbiIsImNvbnZlcnNhdGlvbjpyZWFkIiwiY29udmVyc2F0aW9uOmFjdGlvbiIsInBheW91dHM6cmVhZCIsInBheW91dHM6YWN0aW9uIl0sImlzXzJmYV9kaXNhYmxlZCI6ZmFsc2V9.gMxVXfDeCmVwmd-AsFAUjMZLUcz9oYgEpMOZRyCfK8TNynk5PTP0E2bVgclUpLod8QsrgQLxjIvN_EUsMA1wBw"
        self.name = "valtimyrio"
        self.server = "https://api.staging.iserverbot.ru/v1/"
        self.session = requests.Session()

    def _post_request(self, address, data, headers):
        return self.session.post(url=self.server + address, data=data, headers=headers)

    def _get_request(self, address, headers):
        return self.session.get(url=self.server + address, headers=headers)

    def get_access_token(self):
        if self.last_access_datetime == "" or (
                datetime.datetime.now() - self.last_access_datetime).total_seconds() > 3000:
            data = {
                "mode": "CHATEX_BOT",
                "identification": self.name
            }
            text = "Bearer " + self.fresh_token
            headers = {
                "Authorization": text
            }
            r = self._post_request("auth/access-token", json.dumps(data), headers)
            temp = json.loads(r.text)
            self.access_token = temp["access_token"]
            self.last_access_datetime = datetime.datetime.now()
        return self.access_token

    def create_invoice(self, coin, amount):
        data = {
            "amount": amount,
            "coin": coin,
            "country_code": "EST",
            "fiat": "RUB",
            # "fiat_amount": "2500.00",
            "lang_id": "en",
            "payment_system_id": 347,
            "data": "string",
        }
        headers = {
            "Authorization": "Bearer " + self.get_access_token()
        }
        print(data)
        print(headers)
        r = self._post_request("invoices", json.dumps(data), headers)
        print(r.text)
        temp = json.loads(r.text)
        id = temp["id"]
        url = temp["payment_url"]
        return id, url

    def get_invoice(self, id):
        headers1 = {
            "Authorization": "Bearer " + self.get_access_token()
        }
        r = self.session.get(self.server + "invoices/" + id, headers=headers1)
        print(r.text)
        temp = json.loads(r.text)
        status = temp["status"]
        return status

    def transfer_money(self, coin, amount, receiver):
        data = {
            "coin": coin,
            "amount": str(amount),
            "recipient": "+79852320336",
            "second_factor": {
                "mode": "PIN",
                "code": "1111"
            }
        }
        headers = {
            "Authorization": "Bearer " + self.get_access_token()
        }
        r = self._post_request("wallet/transfers", json.dumps(data), headers)
        print(r, r.text)
