#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


subprocess.run(["unzip", "book.epub"], check=True)


with open("mimetype") as f:
    if f.read() != "application/epub+zip":
        print("This is not a EPUB file")
        sys.exit(1)


container = ET.parse("META-INF/container.xml")

rootfile = (
    container
    .find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfiles")
    .find("{urn:oasis:names:tc:opendocument:xmlns:container}rootfile")
    .get("full-path")
)
print("Rootfile found at", rootfile)


opf = ET.parse(rootfile)

title = (
    opf
    .find("{http://www.idpf.org/2007/opf}metadata")
    .find("{http://purl.org/dc/elements/1.1/}title")
    .text
)
print("Title:", title)

os.makedirs("/tmp/converted", exist_ok=True)
out_path = f"/tmp/converted/{title}.md"[:100]
f_out = open(out_path, "w")

items = (
    opf
    .find("{http://www.idpf.org/2007/opf}manifest")
    .findall("{http://www.idpf.org/2007/opf}item")
)
items_by_id = {}
for item in items:
    items_by_id[item.get("id")] = item

itemrefs = (
    opf
    .find("{http://www.idpf.org/2007/opf}spine")
    .findall("{http://www.idpf.org/2007/opf}itemref")
)
for itemref in itemrefs:
    idref = itemref.get("idref")
    item = items_by_id[idref]
    if item.get("media-type") == "application/xhtml+xml":
        with open(os.path.join(os.path.dirname(rootfile), item.get("href"))) as f:
            chapter = f.read()
        chapter = re.sub(r"<style[\s\S]*?>[\s\S]*?</style>", "", chapter)
        for n in range(1, 7):
            chapter = re.sub(f"<h{n}>", "#" * n + " ", chapter)
        chapter = re.sub(r"</?(b|strong)>", "**", chapter)
        chapter = re.sub(r"</?(i|em)>", "_", chapter)
        chapter = re.sub(r"<[\s\S]*?>", "", chapter)
        chapter = re.sub(r"\n{3,}", "\n\n", chapter).strip()
        f_out.write(f"{chapter}\n\n---\n\n")

print("Output:", out_path)
with open("out-path.txt", "w") as f:
    f.write(out_path)
