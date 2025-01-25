import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def enumerate_urls(url:str):
    unique_urls = set()
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    base_url = urlparse(url)

    for link in soup.find_all('a'):
        full_url = urljoin(url, link.get('href'))
        if urlparse(full_url).netloc == base_url.netloc:
            unique_urls.add(full_url)

    #links = ', '.join(f'"{item}"' for item in unique_urls)
    links = list(unique_urls)
    links = list(filter(lambda word: not word.endswith("pdf"), links))
    print(links)
    return links

enumerate_urls("https://sahamati.org.in/")
