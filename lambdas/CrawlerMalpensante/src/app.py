#!/usr/bin/env python3
import requests
from lxml import html, etree


def lambda_handler(event, context):
    url = 'https://elmalpensante.com/ultimaedicion'
    base_url = 'https://elmalpensante.com'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://elmalpensante.com/"
    }
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    tree = html.fromstring(response.content)

    articles = tree.xpath('//div[contains(@class,"articulos-ultima")]//div[contains(@class, "row")]')

    rss = etree.Element("rss", version="2.0", nsmap={"atom": "http://www.w3.org/2005/Atom"})
    channel = etree.SubElement(rss, 'channel')

    etree.SubElement(channel, 'title').text = 'El Malpensante'
    etree.SubElement(channel, 'link').text = url
    etree.SubElement(channel, 'description').text = 'El Malpensante'
    etree.SubElement(channel, "{http://www.w3.org/2005/Atom}link", attrib={
        "href": "https://gustavomejia.tech/rss/malpensante",
        "rel": "self",
        "type": "application/rss+xml"
    })

    for article in articles:
        xmlElement = etree.SubElement(channel, 'item')
        etree.SubElement(xmlElement, 'title').text = article.xpath(".//div[@class='titulo']")[0].text_content().strip()
        etree.SubElement(xmlElement, 'link').text = base_url + article.xpath(".//div[@class='titulo']/a")[0].attrib['href']
        etree.SubElement(xmlElement, 'guid').text = base_url + article.xpath(".//div[@class='titulo']/a")[0].attrib['href']
        etree.SubElement(xmlElement, 'description').text = article.xpath(".//div[@class='body']")[0].text_content().strip()
        etree.SubElement(xmlElement, 'author').text = article.xpath(".//div[@class='autor']")[0].text_content().strip()
        etree.SubElement(xmlElement, 'category').text = article.xpath(".//div[@class='categoria']")[0].text_content().strip()
        etree.SubElement(xmlElement, 'enclosure', attrib={
            'url': base_url + article.xpath(".//img")[0].attrib['src'],
            'length': '0',
            'type': 'image/jpeg'
        })
        etree.SubElement(xmlElement, 'tag').text = article.xpath(".//div[@class='tags']")[0].text_content().strip()


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/rss+xml; charset=utf-8"
        },
        "body": etree.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
    }
