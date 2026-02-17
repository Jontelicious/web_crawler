def normalize_url(url):
    # Remove the protocol (http:// or https://)
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]

    # Remove trailing slash if it exists
    if url.endswith("/"):
        url = url[:-1]

    return url