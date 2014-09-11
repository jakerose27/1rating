from flask import Flask, render_template, request, url_for
import bottlenose, json, urllib
from pprint import pprint
from lxml import etree
from HTMLParser import HTMLParser
import pynq



app = Flask(__name__)


@app.route('/')
def index():
    return render_template(
        "index.html"
    )

@app.route('/search', methods = ['GET', 'POST'])
def diff():
    search_text = request.form['search']
    thing = bottlenose.Amazon(
    'AKIAJV4MVIAB5Z7BOH5Q',
    'cnZViZA5pXHNxYHOZmJ2hRPSpW78G+hQsSFAjoBR',
    'paulrose9@cox.net'
    )

    response = thing.ItemSearch(Keywords=search_text, SearchIndex="All")
    root = etree.fromstring(response)
    ASIN = root[1][4][0].text
    reviews = thing.ItemLookup(ItemId=ASIN, ResponseGroup="Reviews")
    reviews = etree.fromstring(reviews)
    print etree.tostring(reviews, pretty_print=True)
    iframe_url = reviews.getchildren()[1].getchildren()[1].getchildren()[-1].getchildren()[0].text
    search_title = root.getchildren()[1].getchildren()[4].getchildren()[-1].getchildren()[-1].text


    class MyHTMLParser(HTMLParser):
        def handle_startendtag(self, tag, attrs):
            if tag == "img":
                for item in attrs:
                    if item[0] == "src":
                        if item[1].startswith("http://g-ecx.images-amazon.com/images/G/01/x-locale/common/customer-reviews/ratings/"):
                            self.rating = attrs[2][1].split(" ")[0]

    data = urllib.urlopen(iframe_url).read() # open iframe src url
    parse = MyHTMLParser()
    parse.feed(data)
    # print etree.tostring(tree, pretty_print=True)
    return render_template(
        "search.html",
        iframe_url=iframe_url,
        search_title=search_title,
        rating=parse.rating
    )


if __name__ == '__main__':
    app.run(debug=True)
