#!/usr/bin/env python3
import requests
from lxml import html, etree
from pprint import pprint


def lambda_handler(event, context):
    url = 'https://bogota.gov.co/que-hacer/agenda-cultural'
    base_url = 'https://bogota.gov.co'
    response = requests.get(url)
    response.raise_for_status()

    tree = html.fromstring(response.content)
    articles = tree.xpath("//div[contains(@class, 'view-content')]//a[contains(@class, 'agenda-cultural-v2__tarjeta-basica')]")

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
        etree.SubElement(xmlElement, 'title').text = article.xpath(".//h3/text()")[0]
        etree.SubElement(xmlElement, 'link').text = base_url + article.xpath("./@href")[0]
        etree.SubElement(xmlElement, 'guid').text = base_url + article.xpath("./@href")[0]
        # etree.SubElement(xmlElement, 'description').text = article.xpath(".//div[@class='body']")[0].text_content().strip()
        category = article.xpath(".//div[@class='categoria-tarjeta']/span/text()")
        etree.SubElement(xmlElement, 'category').text = '' if len(category) == 0 else category[0]
        etree.SubElement(xmlElement, 'place').text = article.xpath(".//div[contains(@class, 'evento-detalle-lugar')]//span/text()")[0].strip()
        etree.SubElement(xmlElement, 'isFree').text = article.xpath(".//div[contains(@class, 'evento-detalle-es-pago')]/span/text()")[0]
        etree.SubElement(xmlElement, 'date').text = article.xpath(".//span[contains(@class, 'fechas__destacadas')]")[0].text_content()
        etree.SubElement(xmlElement, 'enclosure', attrib={
            'url': base_url + article.xpath(".//img/@src")[0],
            'length': '0',
            'type': 'image/jpeg'
        })


    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/rss+xml; charset=utf-8"
        },
        "body": etree.tostring(rss, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
    }

