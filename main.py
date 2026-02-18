import asyncio
import sys
from crawl import crawl_site_async
from csv_report import write_csv_report

async def main_async():

    args = sys.argv
    print("Script name:", sys.argv[0])

    if len(args) < 4:
        print("no website provided")
        sys.exit(1)
    
    if len(args) > 4:
        print("too many arguments provided")
        sys.exit(1)
    
    if len(args) == 4:
        print(f"starting async crawl of: {args[1]}")
    
    if not args[2].isdigit() or not args[3].isdigit():
        print("max_concurrency and max_pages must be integers")
        sys.exit(1)

    print("Argument:", args[1])

    max_concurrency = int(args[2])
    max_pages = int(args[3])

    page_data = await crawl_site_async(args[1], max_concurrency, max_pages=max_pages)

    for url, data in page_data.items():
        if data is None:
            continue
        print(f"URL: {url}")
        print(f"H1: {data['h1']}")


    print(f"Found {len(page_data)} total pages!")
    write_csv_report(page_data)
    print("Report written to report.csv")

    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main_async())
