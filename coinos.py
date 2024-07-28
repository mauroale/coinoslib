import requests

class Coinos:

    def __init__(self, username: str, password: str):
        self.__url = "https://coinos.io/api"
        self.__token = dict()
        self.__username = username
        self.__password = password
    
    def call(self, method: str, path: str, params=None, json=None):
        if not (self.__token):
            self.get_auth()

        r = requests.request(
            method=method, 
            url=self.__url + path, 
            json=json,
            params=params, 
            headers={"Authorization": "Bearer " + self.__token["token"]}
        )
        r.raise_for_status()
        return r.json()

    def get_auth(self) -> dict:
        data = {
            "username": self.__username, 
            "password": self.__password
        }
        self.__token = requests.post(f"{self.__url}/login", json=data).json()
        return self.__token

    def invoice(self, amount: int, webhook=None, secret=None):
        data = {
            "invoice": {
                "amount": amount,
                "type": "lightning"
            }        
        }
        if webhook:
            data["invoice"]["webhook"] = webhook
            data["invoice"]["secret"] = secret
        
        return self.call("POST", "/invoice", json=data)

    def pay_bitcoin_and_liquid(self, amount: int, address: str):
        return self.call("POST", "/bitcoin/send", json={
            "amount": amount,
            "address": address
        })