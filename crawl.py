import asyncio
from urllib.parse import urlparse, urljoin
import aiohttp
from bs4 import BeautifulSoup
import requests

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


class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=1):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers={"User-Agent": "BootCrawler/1.0"})
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url not in self.page_data:
                self.page_data[normalized_url] = None
                return True
            else:
                return False
            
    async def get_html(self, url):

        try:
            async with self.session.get(url) as response:
                if response.status > 399:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None

                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    
    async def crawl_page(self, current_url=None):

        if urlparse(current_url).netloc != self.base_domain:
            return
        
        normalized_url = normalize_url(current_url)

        if not await self.add_page_visit(normalized_url):
            return
        
        async with self.semaphore:
            print(
                f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return
            
        async with self.lock:
            page_info = extract_page_data(html, current_url)
            self.page_data[normalized_url] = page_info

        next_urls= get_urls_from_html(html, self.base_url)
        
        tasks = []
        for url in next_urls:
            tasks.append(asyncio.create_task(self.crawl_page(url)))
        
        await asyncio.gather(*tasks)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    
async def crawl_site_async(base_url, max_concurrency):
    async with AsyncCrawler(base_url, max_concurrency) as crawler:
        page_data = await crawler.crawl()
        return page_data
