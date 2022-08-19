import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading
import time
import requests

# Shared Memory variables
CAPACITY = 10
buffer = [-1 for i in range(CAPACITY)]
in_index = 0
out_index = 0

# Declaring Semaphores
mutex = threading.Semaphore()
empty = threading.Semaphore(CAPACITY)
full = threading.Semaphore(0)


class FileFunctions:
    def extract(self, filename):
        urls = []
        with open(filename, "r") as f:
            while True:
                url = f.readline()
                if not url:
                    break
                urls.append(url[:-1])
        return urls

    def write_to_file(self, urls, filename):

        with open(f"finals.txt", "a+") as f:
            f.write("\n")
            f.writelines(urls)
                

# Producer Class
class Producer(threading.Thread):

    def fetch_url(self, url):
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return resp
        except Exception as e:
            # Note : might want to add this to a logger file.
            print(f"The url {url} failed! - {str(e)}")

    def run(self):
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full

        urls = FileFunctions().extract("urls.txt")

        for url in urls:
            resp = self.fetch_url(url)
            if resp:
                empty.acquire()
                mutex.acquire()

                buffer[in_index] = [resp, url]
                in_index = (in_index + 1)%CAPACITY
                print("Producer produced url : ", url)

                mutex.release()
                full.release()

# Consumer Class
class Consumer(threading.Thread):
    def extract_hyperlink(self, resp, url):
        """
            Extracts URLS from HTML and checks if url is valid.
            If valid, appends to a list
        """
        result_urls = [url+"\n"]
        try:
            soup = BeautifulSoup(resp.text, 'lxml')
            anchors = soup.find_all('a', attrs={'href': re.compile('^https?://')})

            for anchor in anchors:
                    href = anchor['href']
                    parsed_url = urlparse(href)
                    if parsed_url.scheme in ['http', 'https']:
                        result_urls.append(href+"\n")
        except Exception as e:
            # Note : Might want to add this to a logger file
            print(f"There was a problem parsing {url} - {str(e)}")
        finally:
            return result_urls

    def run(self):
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full
    
    
        while True:
            full.acquire()
            mutex.acquire()
            
            produce = buffer[out_index]
            out_index = (out_index + 1)%CAPACITY
            print("Consumer consumed item : ", produce[1])
            
            mutex.release()
            empty.release()      
            
            urls = self.extract_hyperlink(produce[0], produce[1])
            FileFunctions().write_to_file(urls, produce[1])

            



# Creating Threads
producer = Producer()
consumer = Consumer()

# Starting Threads
consumer.start()
producer.start()

# Waiting for threads to complete
producer.join()
consumer.join()