import sys
import socket
from bs4 import BeautifulSoup


def help():
    print("""Available commands:\n"
  -u <URL>             Makes an HTTP request to URL and prints the response
  -s <search-term>     Searches the term using your favourite search engine and prints top 10 results
  -h                   Shows this help menu""")


def search(term):
    target_port = 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2)

    client.connect(("www.google.com", target_port)) #connecting the client

    request = "GET /search?q=%s HTTP/1.1\r\nHost: www.google.com\r\n\r\n" % term
    client.send(request.encode()) #send data

    # receive data
    response = b""
    try:
        while True:
            response = response + client.recv(1024)
    except socket.timeout:
        pass
    http_response = repr(response)
    len(http_response)

    #parser
    html_response = response[response.find(b'<!doctype html>'):response.find(b'</html>') + 7]
    soup = BeautifulSoup(html_response, 'html.parser')
    tags = soup.find_all(class_="egMi0") #get elements

   #printing results for searching term
    for item in tags:
        fullURL = str(item.a['href'])
        url = fullURL[fullURL.find("http"):fullURL.find("&sa=")]
        print(url)


def getURL(url):
    target_port = 80
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(2)

    # host part
    http_len = 7
    http = url.find("http://")
    if http == -1:
        http_len = 8 #https

    path_start = url[http_len:].find("/")
    str()
    if path_start == -1:
        # no path
        path_start = len(url) + 1
        path = "/"
    else:
        path_start += http_len
        path = url[path_start:]
    host = url[http_len:path_start]

    print("Request to", host, "at", path, "\n")

    client.connect((host, target_port)) #connecting the client

    request = "GET " + path + " HTTP/1.1\r\nHost: " + host + "\r\n\r\n"
    client.send(request.encode()) # send data

    # receive data
    response = b""
    try:
        while True:
            response = response + client.recv(1024)
    except socket.timeout:
        pass
    http_response = repr(response)
    len(http_response)

    #parser
    html_response = response[response.find(b'<html'):response.find(b'</html>') + 7]
    soup = BeautifulSoup(html_response, 'html.parser')

    for link in soup.find_all("a"):
        print("Inner Text: {}".format(link.text))
        print("Title: {}".format(link.get("title")))
        print("href: {}".format(link.get("href")))


if __name__ == "__main__":
    n = len(sys.argv)

    if n == 2 and sys.argv[1] == '-h':
        help()

    if n == 3 and sys.argv[1] == '-s':
        term = sys.argv[2]
        search(term)

    if n == 3 and sys.argv[1] == '-u':
        url = sys.argv[2]
        getURL(url)