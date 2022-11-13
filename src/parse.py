#!/usr/bin/python

import requests
import sys
from html.parser import HTMLParser
import re


class PokemonCard:
    def __init__(self, cardSet, price):
        self.CardSet = cardSet
        self.Price = price


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.foundPrice = False
        self.link = ""
        self.cards = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[1] == "card-price usd":
                    self.foundPrice = True
                if attr[0] == "href" and self.foundPrice:
                    self.link = attr[1]

    def handle_data(self, data):
        if "$" in data:
            x = re.search("(https://store.tcgplayer.com/pokemon/)([A-Za-z-0-9]*)/([A-Za-z-_0-9]*)?(.*)", self.link)
            # print(x.groups())
            if x is not None:
                price = data.split("$")[1]
                set_name = x.groups()[1]
                card_name = x.groups()[2]
                if "-" in card_name:
                    parsed_name = ""
                    card_parsed = card_name.split("-")
                    if card_parsed[0] == "alolan":
                        parsed_name = card_parsed[1]
                    else:
                        parsed_name = card_parsed[0]
                    card_name = parsed_name
                if card_name not in self.cards:
                    self.cards[card_name] = PokemonCard(set_name, price)
                if price < self.cards[card_name].Price:
                    self.cards[card_name] = PokemonCard(set_name, price)
                self.foundPrice = False

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def main(argv):
    all_cards = {}
    # <a class="card-price usd" href="https://store.tcgplayer.com/pokemon/sm-crimson-invasion/aggron?utm_campaign=affiliate&utm_medium=LimitlessTCG&utm_source=LimitlessTCG" target="_blank">$0.37</a>
    parser = MyHTMLParser()
    page_uri = "https://limitlesstcg.com/cards?q=type%3Apokemon+lang%3Aen+display%3Alist+sort%3Aname+unique%3Acards&page={0}".format(
        1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
    r = requests.Session()
    response = r.get(page_uri, headers=headers)
    body = response.content.decode()
    parser.feed(body)
    for name in parser.cards:
        set_name = parser.cards[name].CardSet
        price = parser.cards[name].Price
        if name not in all_cards:
            all_cards[name] = PokemonCard(set_name,price)
        if price < all_cards[name].Price:
            all_cards[name] = PokemonCard(set_name, price)
    print(all_cards)
if __name__ == "__main__":
    main(sys.argv[1:])
