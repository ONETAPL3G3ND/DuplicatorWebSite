import os
import http.server
import socketserver
from urllib.request import Request, urlopen
from urllib.error import URLError


def download_website(url, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()
        with open(os.path.join(directory, "index.html"), "wb") as f:
            f.write(webpage)
    except URLError as e:
        print("Ошибка при скачивании сайта:", e)


def start_web_server(directory, port=8000):
    os.chdir(directory)
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("Сервер запущен на порту", port)
        httpd.serve_forever()


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/downloadnew/'):
            domain = self.path[len('/downloadnew/'):]
            download_website('http://' + domain, 'downloaded_website')
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            super().do_GET()


if __name__ == "__main__":
    httpd = socketserver.TCPServer(("", 8000), MyRequestHandler)
    print("Сервер запущен на порту 8000")
    httpd.serve_forever()
