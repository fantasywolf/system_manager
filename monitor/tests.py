# Create your tests here.
import requests

params = {'minutes': 1}
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post("http://172.25.254.33:8000/range_data/",
                         json=params,
                         headers=headers,)
print(response.text)
