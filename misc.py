import urllib


def download_file(url, path):
    urllib.urlretrieve(url, path)
