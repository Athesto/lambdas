#!/usr/bin/env python3
# Builin imports
from dataclasses import dataclass
from datetime import datetime
import os
import re
import json

# 3rd party import
import requests
from lxml import html
from dotenv import load_dotenv

# Local imports
from libs import TelegramClient

@dataclass
class Book():
    title: str
    author: str
    description: str
    image: str
    pages: int
    published: str

    def __str__(self):
        msg = f"""
        Title: {self.title}
        Author: {self.author}
        Description: {self.description}
        Image: {self.image}
        Pages: {self.pages}
        Published: {self.published}
        """
        return re.sub(r"\n\s+", "\n", msg)

class HTMLExtractor():
    @staticmethod
    def extract(data):
        tree = html.fromstring(data)

        author_raw = tree.xpath(
            ".//span[contains(@class, 'product-info__author')]"
            "/text()"
        )[0].replace("By", "")
        author = re.sub(r"\s+", " ", author_raw).strip()

        description_node = tree.xpath(
            ".//div[contains(@class, 'free_learning__product_description')]"
            "/span"
            "/text()"
        )
        description = description_node[0] if description_node else "No description"

        pages = tree.xpath(
            ".//div[@class='free_learning__product_pages']"
            "/span"
            "/text()"
        )[0].replace("Pages: ", "")

        published = tree.xpath(
            ".//div[@class='free_learning__product_pages_date']"
            "/span"
            "/text()"
        )[0].split(":")[1].strip()

        return {
            "title": tree.xpath(".//h3/text()")[0],
            "author": author,
            "description": description,
            "image": tree.xpath(".//img[contains(@class, 'product-image')]/@src")[0],
            "pages": pages,
            "published": published
        }

def lambda_handler(event, context):
    url = "https://www.packtpub.com/free-learning/"
    response = requests_page(url)
    data = response.content
    book = Book(**HTMLExtractor.extract(data))

    message = transform_message(book)

    load_dotenv()
    telegram_client = TelegramClient(os.environ["TELEGRAM_BOT_TOKEN"])
    response = telegram_client.sendMessage(
        chat_id=os.environ["CHAT_ID"],
        text=message,
        link_preview_options=json.dumps({
            "url": book.image
        })
    )
    print(response.status_code)


def requests_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def export_file(data, path):
    with open(path, 'wb') as f:
        f.write(data)


def read_file(path):
    with open(path, 'r') as f:
        return f.read()




def transform_message(book:Book):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""
    <b><a href='https://www.packtpub.com/free-learning/'>{book.title}:</a></b>
    {book.description}

    <b>Published:</b> {book.published}
    <b>Pages:</b> {book.pages}
    <b>By</b> {book.author}

    {today}
    """
    message = re.sub(r"\n \s+", "\n", message_raw)
    return message




if __name__ == __name__:
    main()
