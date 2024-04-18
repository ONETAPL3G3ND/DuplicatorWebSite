from urllib.request import Request, urlopen
import os
import http.server
import socketserver


def download_webpage(url):
    req = Request(
        url=url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    webpage = urlopen(req).read()
    return webpage


def start_web_server(directory, port=8000):
    os.chdir(directory)  # Переходим в директорию с сайтом

    # Настраиваем и запускаем локальный веб-сервер
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Сервер запущен на порту", port)
        httpd.serve_forever()


if __name__ == "__main__":
    website_url = input("Введите URL веб-страницы для скачивания: ")
    print("Загрузка веб-страницы...")
    webpage_content = download_webpage(website_url)
    print("Веб-страница успешно загружена.")

    # Создаем директорию для сохранения сайта
    site_name = "downloaded_website"
    if not os.path.exists(site_name):
        os.makedirs(site_name)

    # Сохраняем содержимое веб-страницы
    with open(os.path.join(site_name, "index.html"), 'wb') as f:
        f.write(webpage_content)

    # Запускаем веб-сервер
    start_web_server(site_name)
