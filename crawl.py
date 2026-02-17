from urllib.parse import urlparse, urljoin
import asyncio
from bs4 import BeautifulSoup
import aiohttp

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.netloc}{parsed_url.path}"
    if normalized_url.endswith('/'):
        normalized_url = normalized_url[:-1]
    return normalized_url

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.get_text()
    return None

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    p_tag = None
    main = soup.find('main')
    if main:
        p_tag = main.find('p')

    if p_tag is None:
        p_tag = soup.find('p')

    return p_tag.get_text() if p_tag else ""

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        absolute_url = urljoin(base_url, href)
        urls.append(absolute_url)
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    images = []
    for img_tag in soup.find_all('img', src=True):
        src = img_tag['src']
        absolute_url = urljoin(base_url, src)
        images.append(absolute_url)
    return images

def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)
    }