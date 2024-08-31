from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def parse_book_page(book_page):
    soup = BeautifulSoup(book_page, 'lxml')
    title_and_author = soup.find(id='content').find('h1').text
    title, author = tuple(title_and_author.split(' \xa0 :: \xa0 '))
    title_safe = sanitize_filename(title)
    cover_path = soup.find(class_='bookimage').find('img')['src']
    comments_raw = soup.find_all(class_='texts')
    comments = [comment_raw.find('span').text for comment_raw in comments_raw]
    genres_raw = soup.find('span', class_='d_book').find_all('a')
    genres = [genre_raw.text for genre_raw in genres_raw]
    return title_safe, author, cover_path, comments, genres
