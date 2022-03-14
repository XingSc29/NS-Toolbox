import requests
import re
from urllib import parse
import asyncio
import aiohttp
from aiohttp.client import ClientSession
import argparse


class Crawler:
    def __init__(self, slow_mode):
        self.links_discovered = []
        self.slow_mode = False
        if slow_mode == "Enable":
            self.slow_mode = True

    def request(self, url):
        try:
            return requests.get("http://" + url)
        except requests.exceptions.ConnectionError:
            pass

    def subdomain_crawler(self, target_url, file):
        urls = []
        with open(file, "r") as wordlist:
            for line in wordlist:
                word = line.strip()
                test_url = "http://" + word + "." + target_url
                urls.append(test_url)
        asyncio.run(self.send_all_requests(urls))

    def directory_crawler(self, target_url, file):
        urls = []
        with open(file, "r") as wordlist:
            for line in wordlist:
                word = line.strip()
                test_url = "http://" + target_url + "/" + word
                urls.append(test_url)
        asyncio.run(self.send_all_requests(urls))

    async def asyn_request(self, url:str, session:ClientSession):
        async with session.get(url) as response:
            result = await response.text()
            if "404 Not Found" not in str(response.raise_for_status):
                print(f"[+] {url}") 

    async def send_all_requests(self, urls:list):
        if self.slow_mode:
            my_conn = aiohttp.TCPConnector(limit=5)
        else:
            my_conn = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(connector=my_conn) as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(self.asyn_request(url=url, session=session))
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)


    def link_crawler(self, target_url, recursive, attempt):
        response = self.request(target_url)
        if target_url[-1] != "/":
            target_url = target_url + "/"
        try:
            # print(re.findall('(?:href=")(.*?)"', str(response.content)))
            href_links = re.findall('(?:href=")(.*?)"', str(response.content))
            for link in href_links:
                try:
                    if link[0] == "/":
                        link = link[1:]
                except IndexError:
                    pass
                link = parse.urljoin(target_url, link)
                if "#" in link:
                    link = link.split("#")[0]
                if target_url in link and link not in self.links_discovered:
                    self.links_discovered.append(link)
                    print("[+] " + link)
                    attempt += 1
                    if attempt <= recursive:
                        self.link_crawler(link, recursive, attempt)
        except UnicodeDecodeError as e:
            print(e)
            pass
        except AttributeError: 
            pass


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode", dest="mode", help="The attack mode")
    parser.add_argument("-u", "--url", dest="url", help="The target URL to be crawled")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="The wordlist for directory or subdomain crawler")
    parser.add_argument("-r", "--recursive", dest="recursive", help="The recursive count for link crawler")
    parser.add_argument("-s", "--slowmode", dest="slowmode", help="Enable slow mode (Enable/Disable)")
    options = parser.parse_args()

    return options


options = get_arguments()

mode = options.mode
slow_mode = "Disable"
if mode == "Subdomain Crawler":
    url = options.url
    wordlist = options.wordlist
    slow_mode = options.slowmode
    crawler = Crawler(slow_mode)
    print("[+] Start sending requests...")
    crawler.subdomain_crawler(url, wordlist)
    print("[+] Attack Finished")
elif mode == "Directory Crawler":
    url = options.url
    wordlist = options.wordlist
    slow_mode = options.slowmode
    crawler = Crawler(slow_mode)
    print("[+] Start sending requests...")
    crawler.directory_crawler(url, wordlist)
    print("[+] Attack Finished")
elif mode == "Link Crawler":
    url = options.url
    recursive = int(options.recursive)
    crawler = Crawler(slow_mode)
    print("[+] Start crawling the webpage...")
    crawler.link_crawler(url, recursive, 0)
    print("[+] Attack Finished")


# wordlist = "wordlist/common.txt"
# target_url = "192.168.140.167/mutillidae/"
# test_url = "google.com/"
# crawler = Crawler()
# crawler.directory_crawler(test_url, wordlist)
# crawler.subdomain_crawler(test_url, wordlist)
# recursive = 10
# crawler.link_crawler(target_url, recursive, 0)