import csv

def write_csv_report(page_data, filename="report.csv"):
    fieldnames = ["page_url", "h1", "first_paragraph", "outgoing_link_urls", "image_urls"]
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for page in page_data.values():
            if page is None:
                continue
                
            writer.writerow({
                "page_url": page["url"],
                "h1": page.get("h1", ""),
                "first_paragraph": page.get("first_paragraph", ""),
                "outgoing_link_urls": ";".join(page.get("outgoing_links", [])),
                "image_urls": ";".join(page.get("image_urls", []))
            })