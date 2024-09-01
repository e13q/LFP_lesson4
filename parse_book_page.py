from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def parse_book_page(book_page):
    soup = BeautifulSoup(book_page, 'lxml')
    title_and_author = soup.select_one('#content h1').text
    title, author = tuple(title_and_author.split(' \xa0 :: \xa0 '))
    title_safe = sanitize_filename(title)
    cover_path = soup.select_one('.bookimage img').get('src')
    comments_raw = soup.select('.texts')
    comments = [
        comment_raw.select_one('span').text for comment_raw in comments_raw
    ]
    genres_raw = soup.select_one('span.d_book a')
    genres = [genre_raw.text for genre_raw in genres_raw]
    return title_safe, author, cover_path, comments, genres
