#!/usr/bin/env python3

import requests
import json
from faker import Faker


APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

# Get the Auth Token Key
apiKey = getAuthToken()

print(apiKey)

fake = Faker()
for i in range(4, 130):
    fakeTitle = fake.catch_phrase()
    fakeAuthor = fake.name()
    fakeISBN = fake.isbn13()
    book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
    # add the new random "fake" book using the API
    addBook(book, apiKey) 


def delBook(id):
    r = requests.delete(
        f"{APIHOST}/api/v1/books/{id}", 
        headers = {
            "Accept":"application/json",
            "X-API-Key": apiKey
        },
    )

    if r.status_code == 200:
        print(f"Book ID {id} deleted.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to delete book {id}.")

# Delete the first 5 books
for i in range(1, 6):
    delBook(i)

# Delete the last 5 books (assuming books 4-129 were added)
for i in range(125, 130):
    delBook(i)
