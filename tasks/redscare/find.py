import nltk
import os
from treetagger import TreeTagger
import xml.etree.ElementTree as ET


tt = TreeTagger(language="russian")


ns = {
    "fb2": "http://www.gribuser.ru/xml/fictionbook/2.0"
}


for book_file_name in sorted(os.listdir("books")):
    if not book_file_name.endswith(".fb2"):
        continue
    print("Book", book_file_name)

    tree = ET.parse(os.path.join("books", book_file_name))

    title = tree.find(".//fb2:book-title", ns).text
    print(" | Title:", title)

    text = ""
    for section in tree.findall(".//fb2:section", ns):
        text += "\n".join(section.itertext()) + "\n\n"
    text = text.replace("\xa0", " ")
    print(" | Text size:", round(len(text) / 1024 / 1024, 2), "MiB")

    pairs = []
    for line in text.split("\n"):
        sentences = [sentence.strip() for sentence in nltk.sent_tokenize(line, language="russian")]
        for i in range(len(sentences) - 1):
            question = sentences[i]
            answer = sentences[i + 1]
            # Questions must be real questions
            if len(question) > 30 and question.endswith("?") and answer[-1] in ".!" and "?" not in answer and question[0].isalpha() and question[0].isupper() and answer[0].isalpha() and answer[0].isupper():
                pairs.append((question, answer))

    # Unique
    pairs = list({question: answer for question, answer in pairs}.items())

    print(" | Question candidates:", len(pairs))

    all_texts = ""
    offset_of_text = []
    for question, answer in pairs:
        offset_of_text.append(len(all_texts))
        all_texts += question + "\n"
        offset_of_text.append(len(all_texts))
        all_texts += answer + "\n"

    # Batch tagging is more efficient
    offset = -1
    text_id = 0
    tags_by_text = [[] for _ in offset_of_text]
    for word, tag, canonical_form in tt.tag(all_texts):
        offset = all_texts.find(word, offset + 1)
        while text_id + 1 < len(pairs) and offset >= offset_of_text[text_id + 1]:
            text_id += 1
        tags_by_text[text_id].append((word, tag, canonical_form))

    print(" | Questions:")
    for (question, answer), question_tags, answer_tags in zip(pairs, tags_by_text[::2], tags_by_text[1::2]):
        print("   | Q:", question)
        print("   | A:", answer)

    print()
