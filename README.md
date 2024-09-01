# Парсер книг с сайта tululu.org

В данном проекте реализован парсинг страниц для скачивания книг и информации о них с сайта [tululu.org](https://tululu.org/)

### Как установить

Python3 должен быть установлен. 
Используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```

### Запуск скрипта

Запускать скрипт можно с помощью команды
```
python3 main.py
```
В таком случае скачаются книги с 1 страницы по последнюю страницу (включительно) для категории /l55/.

Либо, указывая промежуток страниц с книгами на сайте
```
python3 main.py  --start_page 1 --end_page 2
```
В таком случае скачаются книги с 1 по 2 страницы (включительно).

Другие примеры:
```
# Первая страница
python3 main.py  --start_page 1 --end_page 1
```
```
# С третьей страницы по последнюю
python3 main.py  --start_page 3
```
```
№ С первой страницы по 20
python3 main.py  --end_page 20
```
Также, присутствуют другие параметры запуска:

```
--dest_folder — путь к каталогу с результатами парсинга: картинкам, книгам, JSON.
--skip_imgs — не скачивать картинки
--skip_txt — не скачивать книги
```
Пример работы приложения:
![image](https://github.com/user-attachments/assets/56f09a55-c755-4063-8ed2-93bb69709433)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
