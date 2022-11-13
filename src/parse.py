#!/usr/bin/python

import requests
import sys
import getopt
from io import StringIO
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.foundPrice = False
        self.link = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[1] == "card-price usd":
                    self.foundPrice = True
                if attr[0] == "href" and self.foundPrice:
                    self.link = attr[1]

    def handle_data(self, data):
        if "$" in data:
            # TODO: parse Link for card, add price
            print(self.link)
            print("Encountered a price  :", data)
            self.foundPrice = False


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def main(argv):
    # <a class="card-price usd" href="https://store.tcgplayer.com/pokemon/sm-crimson-invasion/aggron?utm_campaign=affiliate&utm_medium=LimitlessTCG&utm_source=LimitlessTCG" target="_blank">$0.37</a>
    try:
        parser = MyHTMLParser()
        page_uri = "https://limitlesstcg.com/cards?q=type%3Apokemon+lang%3Aen+display%3Alist+sort%3Aname+unique%3Acards&page={0}".format(1)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
        r = requests.Session()
        response = r.get(page_uri, headers=headers)
        body = response.content.decode()
        parser.feed(body)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    totals = {}
    # Now that we've parsed all the decks and found all the cards, clean and aggregate
    # print aggregated results
    for key, value in totals.items():
        print("{0},{1}".format(value, key))

if __name__ == "__main__":
   main(sys.argv[1:])
