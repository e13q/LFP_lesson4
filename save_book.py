from urllib.parse import urljoin

import os
import json
import re

from fetch import fetch_data, BASE_URL
from parse_book_page import parse_book_page


def save_object(object, title, file_type='txt', dest_dir=None, sub_dir=None):
    if not object:
        return
    file_name = f"{title}.{file_type}"
    directory = ''
    path = ''
    if dest_dir and sub_dir:
        directory = os.path.join(dest_dir, sub_dir)
        path = os.path.join(directory, file_name)
    elif dest_dir:
        directory = dest_dir
        path = os.path.join(dest_dir, file_name)
    elif sub_dir:
        directory = sub_dir
        path = os.path.join(sub_dir, file_name)
    else:
        path = file_name
    if directory:
        os.makedirs(directory, exist_ok=True)
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


def save_book(book_page_link, skip_txt, skip_imgs, dest_folder):
    book = fetch_data(
        urljoin(BASE_URL, '/txt.php'),
        {'id': re.findall(r'\d+', book_page_link)}
    )
    if not book:
        return
    else:
        book = book.text
    book_page_link = urljoin(BASE_URL, book_page_link)
    book_page = fetch_data(book_page_link)
    if not book_page:
        return
    else:
        book_page = book_page.text
    (
        title, author, cover_path, comments, genres
    ) = parse_book_page(book_page)
    cover = fetch_data(urljoin(book_page_link, cover_path)).content
    _, img_ext = tuple(cover_path.split('.'))

    book_path = save_object(
            book, title, dest_dir=dest_folder, sub_dir='books'
        ) if not skip_txt else None
    img_path = save_object(
            cover, title, img_ext, dest_folder, 'images'
        ) if not skip_imgs else None
    book_summary = {
        "title": title,
        "author": author,
        "img_src": img_path or '',
        "book_path": book_path or '',
        "comments": comments,
        "genres": genres
    }
    return book_summary
