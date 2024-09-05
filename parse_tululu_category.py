from bs4 import BeautifulSoup

from request_with_retries import request_with_retries, BASE_URL
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


def check_page_end(category, page_end=None):
    book_category_url = urljoin(BASE_URL, category)
    if not page_end:
        page_with_books = request_with_retries(book_category_url)
        page_end = parse_page_for_pages_count(page_with_books.text)
    return page_end


def get_books_links_by_category(category, page_start, page_end):
    book_category_url = urljoin(BASE_URL, category)
    links = []
    for page_number in range(page_start, page_end+1):
        book_category_page_url = urljoin(book_category_url, f'{page_number}/')
        page_with_books = request_with_retries(book_category_page_url)
        links_on_page = parse_page_for_urls(page_with_books.text)
        links += links_on_page
    return links
