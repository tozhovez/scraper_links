import re
import html
import requests
import json
import os
import asyncio
from urllib.parse import urlparse
from xml.sax.saxutils import escape, unescape
#from async_loader import Loader, LoaderError, LoaderContentTypeError
from tools.async_loader import Loader, LoaderError, LoaderContentTypeError



async def spyder_loader(base_url, max_depth, source_url, url, depth):
    print(base_url, max_depth, source_url, url, depth)
    client = Loader()
    try:
        t = await client.fetch(url)
        data = page_parser(base_url, t)
        data["url"] = url
        data["source_url"] = source_url
        data["depth"] = depth
        return data
    except LoaderError as ex:
        print(ex, url, base_url, max_depth, source_url, url, depth)
        return None
    except LoaderContentTypeError as ex:
        print(ex, url, base_url, max_depth, source_url, url, depth)
        return None


def get_link_url(base_url, url):
    t = urlparse(url)
    if t.fragment and (t.params or t.query):
        print(url)
        print(t)
    scheme =  f"{t.scheme}://" if t.scheme else ""
    domain = f"{scheme}{t.netloc}" if t.netloc else f"{base_url}"
    path = f"{t.path}" if t.path and t.path[0]=="/" else (f"/{t.path}" if t.path and t.path[0]!="/" else "")
    query = f"?{html.unescape(t.query)}" if t.query else ""
    fragment = f"#{t.fragment}" if t.fragment else ""
    link = f"{domain}{path}"
    if query:
        link = f"{link}{query}" if link[-1] == "/" else f"{link}/{query}"
    full = f"{link}{fragment}"
    return (link, full, domain)




pattern_title = re.compile(
    r'(?:<head\s?[^>]*>.*<title\s?[^>]*>\s*)([^<].*)(?:<\/title>.*<\/head>)',
    flags=(re.IGNORECASE|re.DOTALL|re.UNICODE)
    )
pattern_a_tag = re.compile(
    r'(<a\s+[^>]*>)(.*?)(?:<\/a>)',
    flags=(re.IGNORECASE|re.DOTALL|re.UNICODE)
    )

pattern_a_tag_attr_href = re.compile(
    r'(?:<a[^>]+href\s?=\s?[\'"])([^\'"]+)(?:[\'"].*?>)',
    flags=(re.IGNORECASE|re.DOTALL|re.UNICODE)
    )
pattern_a_tag_text = re.compile(r'<[^>]+>', flags=(re.IGNORECASE|re.DOTALL|re.UNICODE))
pattern_empty = re.compile(r'\s\s+', flags=(re.IGNORECASE|re.DOTALL|re.UNICODE))


def get_links_data(base_url, scanner_pattern_a_tag,
                   pattern_a_tag_attr_href=pattern_a_tag_attr_href,
                   pattern_a_tag_text=pattern_a_tag_text,
                   pattern_empty=pattern_empty):
    for tag_href, tag_text in scanner_pattern_a_tag:
        scanner_pattern_a_tag_attr_href = pattern_a_tag_attr_href.findall(tag_href)
        if scanner_pattern_a_tag_attr_href:
            link_url = scanner_pattern_a_tag_attr_href[0].strip()
            if link_url:
                real_link, full_link, domain_link = get_link_url(base_url, link_url)
                scanner_pattern_a_tag_text = pattern_a_tag_text.sub(' ', tag_text)

                link_text = pattern_empty.sub(' ', scanner_pattern_a_tag_text)

                link_text = html.unescape(link_text).strip()

                line = {
                    "real_link": real_link,
                    "full_link": full_link,
                    "link_text": (link_text, str(link_text)),
                    "domain_link": domain_link
                }
                print(line)
                yield line


def page_parser(base_url, text,
                pattern_title=pattern_title,
                pattern_a_tag=pattern_a_tag):
    #print(text)
    page_data = {}
    scanner_title = pattern_title.findall(text)
    if scanner_title:
        title = scanner_title[0].strip()
        if title:
            page_data["page_title"] = html.unescape(title)
        else:
            page_data["page_title"] = ""
            print(scanner_title)

    scanner_pattern_a_tag = pattern_a_tag.findall(text)
    all_links = [line for line in get_links_data(base_url, scanner_pattern_a_tag)]
    page_data["all_links"] = all_links
    
    return page_data







