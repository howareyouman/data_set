import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
from os.path import join
import codecs
from html.parser import HTMLParser


def get_article_links(number_of_pages=100):
    links = set()

    while number_of_pages > 0:
        print(number_of_pages)
        link = urllib.request.urlopen("https://www.theguardian.com/uk/ukcrime?page="
                                      + str(number_of_pages))
        response = link.read()
        link.close()
        response = response.decode("utf-8")
        soup = BeautifulSoup(response, "html.parser",
                             parse_only=SoupStrainer("a", attrs={'data-link-name': 'article'}))
        for link in soup:
            if link.has_attr('href'):
                links.add(link['href'])
        number_of_pages -= 1

    return links


def get_article_from_link(link_str):
    link = urllib.request.urlopen(link_str)
    response = link.read()
    link.close()
    response = response.decode("utf-8")
    soup = BeautifulSoup(response, "html.parser",
                         parse_only=SoupStrainer("div", attrs={'itemprop': 'articleBody'}))
    return soup.text.replace('\n', '').replace('Read more', '')

def save_article_to_file(article, filename, directory):
    file = codecs.open(join(directory, filename), 'w', "utf-8")
    file.write(article)
    file.close()

if __name__ == '__main__':
    directory = "data_set"
    links = get_article_links(754)
    i = 0
    for link in links:
        print(link)
        i += 1
        try:
            article = get_article_from_link(link)
            save_article_to_file(article, str(i) + ".txt", directory)
        except Exception as e:
            print(e.strerror)
