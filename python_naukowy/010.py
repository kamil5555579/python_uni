import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter
from io import BytesIO
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

def download_png(link):
    res = requests.get('https://www.if.pw.edu.pl/~mrow/dyd/wdprir/' + link)
    with open('python_naukowy/pngs/' + link, 'wb') as f:
        img = Image.open(BytesIO(res.content))
        img = img.filter(ImageFilter.GaussianBlur(radius=10))
        # black and white
        img = img.convert('L')
        img.save(f, 'png')
        print(f'Downloaded {link}')
            
if __name__ == '__main__':

    print(f'Number of processors: {multiprocessing.cpu_count()}')
    res = requests.get('https://www.if.pw.edu.pl/~mrow/dyd/wdprir/')
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.find_all('a')
    links = [link for link in links if link.get('href') and link.get('href').endswith('.png')]
    links = [link.get('href') for link in links]

    # Without threading
    start = time.time()
    for link in links:
        download_png(link)
    end = time.time()
    print(f'Without threading: {end - start} seconds')

    # With threading
    start = time.time()
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        futures = [executor.submit(download_png, link) for link in links]
        for future in as_completed(futures):
            future.result()
    end = time.time()
    print(f'With threading: {end - start} seconds')