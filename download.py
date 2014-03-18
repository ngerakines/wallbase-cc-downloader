import os
import mechanize
import cookielib
import argparse
from BeautifulSoup import BeautifulSoup
import re

__author__ = 'ngerakines'

source_urls = [
    'http://wallbase.cc/toplist?section=wallpapers&q=&res_opt=eqeq&res=0x0&thpp=60&purity=001&board=21&aspect=0.00&ts=1m',
    'http://wallbase.cc/toplist?section=wallpapers&q=&res_opt=eqeq&res=0x0&thpp=60&purity=010&board=21&aspect=0.00&ts=1m',
    'http://wallbase.cc/toplist?section=wallpapers&q=&res_opt=eqeq&res=0x0&thpp=60&purity=100&board=21&aspect=0.00&ts=1m'
]


def login(br, username, password):
    br.open('http://wallbase.cc/user/login')
    br.select_form(nr=0)
    br.form['username'] = username
    br.form['password'] = password
    br.submit()


def destination_path(directory, part):
    filename = "dl-wallpaper-%s.jpg" % part
    return os.path.join(directory, filename)


def crawl_data(directory, blacklisted_files, br, data):
    div_matcher = re.compile('<a href="(http://wallbase.cc/wallpaper/(\d+))" target="_blank">')
    iterator = div_matcher.finditer(data)
    wallpapers = dict()
    for match in iterator:
        (url, wallpaper_id) = match.groups()
        destination = destination_path(directory, wallpaper_id)
        if not os.path.isfile(destination):
            if destination not in blacklisted_files:
                wallpapers[wallpaper_id] = (url, destination)
    download_urls = dict()
    for wallpaper_id, (url, destination) in wallpapers.items():
        link_response = br.open(url)
        soup = BeautifulSoup(link_response.read())
        for img in soup.findAll('img'):
            if img['src'].startswith("http://wallpapers.wallbase.cc"):
                download_urls[wallpaper_id] = (img['src'], destination)
    for wallpaper_id, (url, destination) in download_urls.items():
        download(br, url, destination)


def download(br, url, destination):
    br.retrieve(url, destination)


def blacklist(filename):
    files = []
    with open(filename) as f:
        for line in f.readlines():
            files.append(line.rstrip())
    return files

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--directory')
    parser.add_argument('--blacklist')
    args = parser.parse_args()

    blacklisted_files = blacklist(args.blacklist)

    browser = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)
    browser.set_handle_equiv(True)
    # browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    browser.addheaders = [('User-agent', 'Chrome')]
    login(browser, args.username, args.password)
    for source_url in source_urls:
        response = browser.open(source_url)
        crawl_data(args.directory, blacklisted_files, browser, response.read())
