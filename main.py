import urllib3
import argparse
from tqdm.auto import tqdm

from save_book import save_book, save_object
from parse_tululu_category import get_books_links_by_category


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser(
        description='Download books from https://tululu.org')
    parser.add_argument(
        'start_page',
        help='Book page from',
        nargs='?',
        type=int,
        default=1
    )
    parser.add_argument(
        'end_page',
        help='Book page to',
        nargs='?',
        type=int,
        default=4
    )
    parser = parser.parse_args()
    start_page = parser.start_page
    end_page = parser.end_page
    links = get_books_links_by_category('/l55/', start_page, end_page)
    books_summary = []
    for book_page_link in tqdm(
        links, ascii=True, desc='Download books'
    ):
        books_summary.append(save_book(book_page_link))
    save_object(books_summary, 'books_summary', 'json')


if __name__ == '__main__':
    main()
