import urllib3
import argparse
import os
from tqdm.auto import tqdm

from save_book import save_book, save_object
from parse_tululu_category import get_books_links_by_category


def valid_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        if os.access(path, os.W_OK):
            return path
        else:
            raise argparse.ArgumentTypeError(f"Директория '{path}' не доступна для записи.")
    except OSError as e:
        raise argparse.ArgumentTypeError(f"Невозможно создать директорию '{path}': {e}")


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    parser = argparse.ArgumentParser(
        description='Download books from https://tululu.org')
    parser.add_argument(
        '--start_page',
        help='Book page from',
        nargs='?',
        type=int,
        default=1
    )
    parser.add_argument(
        '--end_page',
        help='Book page to',
        nargs='?',
        type=int
    )
    parser.add_argument(
        '--dest_folder',
        help='Save to dir',
        type=valid_directory
    )
    parser.add_argument(
        '--skip_imgs',
        action='store_true',
        help='Dont save images',
    )
    parser.add_argument(
        '--skip_txt',
        action='store_true',
        help='Dont save books text'
    )
    parser = parser.parse_args()
    start_page = parser.start_page
    end_page = parser.end_page
    skip_txt = parser.skip_txt
    skip_imgs = parser.skip_imgs
    dest_folder = parser.dest_folder
    links = get_books_links_by_category('/l55/', start_page, end_page)
    books_summary = []
    for book_page_link in tqdm(
        links, ascii=True, desc='Download books'
    ):
        books_summary.append(
            save_book(book_page_link, skip_txt, skip_imgs, dest_folder)
        )
    save_object(
        books_summary, 'books_summary', 'json', dest_folder
    )


if __name__ == '__main__':
    main()
