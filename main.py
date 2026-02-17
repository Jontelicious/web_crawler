import asyncio
import sys
from crawl import crawl_site_async

async def main_async():

    print("Script name:", sys.argv[0])

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    
    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        print(f"starting crawl of: {sys.argv[1]}")
    
    print("Argument:", sys.argv[1])

    page_data = await crawl_site_async(sys.argv[1], max_concurrency=5)

    for url, data in page_data.items():
        if data is None:
            continue
        print(f"URL: {url}")
        print(f"H1: {data['h1']}")

        print(f"Found {len(page_data)} total pages!")

if __name__ == "__main__":
    asyncio.run(main_async())
