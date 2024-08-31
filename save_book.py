from urllib.parse import urljoin

import os
import json
import re

from fetch import fetch_data, BASE_URL
from parse_book_page import parse_book_page


def save_object(object, title, file_type='txt', directory=None):
    if not object:
        return
    path = f"{title}.{file_type}"
    if directory:
        os.makedirs(directory, exist_ok=True)
        path = f"./{directory}/{path}"
    write_type = 'w+'
    encoding_type = 'utf8'
    if file_type not in ['txt', 'json']:
        write_type = 'wb+'
        encoding_type = None
    with open(path, write_type, encoding=encoding_type) as file:
        if file_type == 'json':
            json.dump(object, file, indent=2, ensure_ascii=False)
        else:
            file.write(object)
    return path


def save_book(book_page_url):
    book = fetch_data(
        urljoin(BASE_URL, '/txt.php'),
        {'id': re.findall(r'\d+', book_page_url)}
    )
    if not book:
        return
    else:
        book = book.text
    book_page_url = urljoin(BASE_URL, book_page_url)
    book_page = fetch_data(book_page_url)
    if not book_page:
        return
    else:
        book_page = book_page.text
    (
        title, author, cover_path, comments, genres
    ) = parse_book_page(book_page)
    cover = fetch_data(urljoin(book_page_url, cover_path)).content
    _, img_ext = tuple(cover_path.split('.'))

    book_path = save_object(book, title, directory='books')
    img_path = save_object(cover, title, img_ext, 'images')
    book_summary = {
        "title": title,
        "author": author,
        "img_src": img_path,
        "book_path": book_path,
        "comments": comments,
        "genres": genres
    }
    return book_summary
