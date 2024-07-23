import requests

HOST = 'localhost'
DB_NAME = 'CW_№5'
USER = 'postgres'
PASSWORD = '201023'

url = 'https://api.hh.ru/vacancies'
headers = {'User-Agent': 'HH-User-Agent'}
params = {
    "employer_id": (3529, 78638, 1272486, 3388, 4233, 2180, 64174, 83056, 1433, 208189),
    "area": "113",
    "per_page": 100
}
response = requests.get(url, headers)
vacancies = response.json()['items']
print(vacancies)

