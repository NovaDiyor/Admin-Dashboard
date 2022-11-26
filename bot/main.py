import requests

# TOKEN = "5498068148:AAGjrSkT6rCy8pLCHE_IqDr5X941D7YTpa0"
# chat_id = "-1001619375200"


def send_message(token, chat_id, name, l_name, number, address, postal, email, region, city):
    result = f"Name: { name },\n Surname: { l_name }\n Phone number : { number }\n Address: { address }\n Postal code: { postal }\n Email :{ email }\n Region: { region }\n City { city }\n"
    url = f"https://api.telegram.org/bot{ token }/sendMessage?chat_id={ chat_id }&text={ result }"
    work = requests.get(url)
