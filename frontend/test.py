import requests

print(requests.get("http://127.0.0.1:8000/entries").json())

# entry = input("Enter your entry: ")
# requests.post("http://127.0.0.1:8000/entries").json()
