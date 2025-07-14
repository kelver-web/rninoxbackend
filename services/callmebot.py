import requests


class CallmeBot:
    
    def __init__(self):
        self.__base_url = 'https://api.callmebot.com/whatsapp.php'
        self.__phone_number = '558496068403'
        self.__api_key = '5976829'


    def send_message(self, message):
        response = requests.get(
            f'{self.__base_url}?phone={self.__phone_number}&text={message}&apikey={self.__api_key}'
        )

        return response.text
