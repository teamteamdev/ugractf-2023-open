import os
import re
import requests


URL = "https://redscare.o.2023.ugractf.ru/7dqlxaitrtei4x63"


def normalize(s):
    return re.sub(r"[^а-яё0-9]+", " ", s.lower()).strip()


text = ""
for name in os.listdir("books"):
    if name.endswith(".fb2"):
        with open(f"books/{name}") as f:
            text += f.read()
text = normalize(text)


request = requests.get(URL).text

while True:
    percentage = request.splitlines()[7].partition("YELLOW>")[2].partition("<")[0]
    print(percentage)

    question = request.splitlines()[11].partition("WHITE>")[2].partition("<")[0]
    print("Q:", question)

    norm_q = normalize(question)

    try:
        index = text.index(norm_q) + len(norm_q)
        answer = " ".join(text[index:index + 10000].split()[:500])
    except ValueError as e:
        print("A: (no answer found)")
        request = requests.get(URL).text
        continue

    print("A:", answer)
    request = requests.post(URL + "/reply", data={"question": question, "answer": answer}).text
