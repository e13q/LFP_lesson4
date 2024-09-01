from bs4 import BeautifulSoup

from fetch import fetch_data, BASE_URL
from urllib.parse import urljoin


def parse_page_for_urls(books_on_page):
    soup = BeautifulSoup(books_on_page, 'lxml')
    tables = soup.select('table.d_book')
    links_on_page = [table.select_one('tr a')['href'] for table in tables]
    return links_on_page


def parse_page_for_pages_count(books_on_page):
    soup = BeautifulSoup(books_on_page, 'lxml')
    pages_count = int(soup.select('.npage')[-1].text)
    return pages_count


def get_books_links_by_category(category, page_start, page_end=None):
    url_book_category = urljoin(BASE_URL, category)
    if not page_end:
        page_with_books = fetch_data(url_book_category)
        page_end = parse_page_for_pages_count(page_with_books.text)
    links = []
    for i in range(page_start, page_end+1):
        url_book_category_page = urljoin(url_book_category, f'{i}/')
        page_with_books = fetch_data(url_book_category_page)
        links_on_page = parse_page_for_urls(page_with_books.text)
        links += links_on_page
    return links
