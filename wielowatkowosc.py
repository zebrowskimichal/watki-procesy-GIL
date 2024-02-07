### Multithreading

#1. Korzystając z modułu `threading`, napisz prosty program, który w konsoli będzie wyświetlał ze znaków pasek ładowania przez czas określony jako argument funkcji głównego wątku.

import threading
import time

def loading_bar(duration):
    for i in range(101):
        print(f"[{'=' * i}{' ' * (100 - i)}] {i}%")
        time.sleep(duration / 100)

if __name__ == "__main__":
    duration = 10
    t = threading.Thread(target=loading_bar, args=(duration,))
    t.start()
    t.join()

#2. Zadanie projektowe: Stwórz listę kilkunastu linków do zdjęć z Wikipedii (lista może być wspólna dla całej grupy, jeżeli tak będzie prościej). Wykorzystaj moduł `urllib` do napisania prostej funkcji pobierającej obrazki z podanych linków (`urllib.request.urlretrieve`). Następnie, korzystając z `ThreadPoolExecutor` napisz skrypt, który korzystając z przygotowanej funkcji, wielowątkowo pobierze wszystkie obrazki do podfolderu `temp`.
#> Warto porównać czasy pobierania, jednowątkowego i wielowątkowego, korzystając np. z napisanych na poprzednie zajęcia dekoratorów. Wystarczy zmieniać argument `max_workers` na 1 lub większą liczbę.

import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def download_image(url):
    os.makedirs("temp", exist_ok=True)
    filename = os.path.join("temp", os.path.basename(url))
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded {url} to {filename}")


links = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/%D0%93%D0%B0%D1%80%D0%B0%D0%B4%D0%B7%D1%96%D1%88%D1%87%D0%B0_1.jpg/240px-%D0%93%D0%B0%D1%80%D0%B0%D0%B4%D0%B7%D1%96%D1%88%D1%87%D0%B0_1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Usa_edcp_relief_location_map.png/238px-Usa_edcp_relief_location_map.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Walka_o_sztandar_turecki.jpg/240px-Walka_o_sztandar_turecki.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Red_pog.svg/6px-Red_pog.svg.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/FIFA_Manager_10_logo.png/240px-FIFA_Manager_10_logo.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/HUN_Order_the_Red_Star.png/150px-HUN_Order_the_Red_Star.png",
]

with ThreadPoolExecutor(max_workers=4) as executor:
    for link in links:
        executor.submit(download_image, link)

### Multiprocessing - zadania

#1. Korzystając z ogólnodostępnych algorytmów (do znalezienia np. na Wikipedii), napisz funkcję sprawdzającą, czy dana liczba jest liczbą pierwszą. Wynikiem może być `print` do konsoli wartości `True` / `False`. Wykorzystaj moduł `multiprocessing`, żeby uruchomić napisaną funkcję w kilku procesach i zweryfikować, które z poniższych liczb są liczbami pierwszymi:

    #```txt
    #919, 920, 971, 991, 1000, 1193, 1931, 3119, 19937, 37199, 39119, 39121, 71993, 319993, 325477, 331999, 391939, 393919, 919393, 933199, ```

    #> Jeżeli obliczenia mimo wszystko zajmują dużo czasu - skróć listę w miarę potrzeb.

import multiprocessing

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    numbers = [919, 920, 971, 991, 1000, 1193, 1931, 3119, 19937, 37199, 39119, 39121, 71993, 319993, 325477, 331999, 391939, 393919, 919393, 933199]
    with multiprocessing.Pool() as pool:
        results = pool.map(is_prime, numbers)
    for number, result in zip(numbers, results):
        print(f"{number} Jest liczba pierwsza: {result}")

#2. Napisz prostą (dodawanie, mnożenie, dzielenie, etc.) i złożoną (ciąg Fibonacciego) funkcję obliczeniową. Korzystając z `ProcessPoolExecutor`, stwórz ok. 50 wywołań jednej i drugiej funkcji. Przy użyciu modułu `time` lub `datetime`, porównaj czasy wykonywania obu przypadków (czasy wykonywania obu przypadków dodaj do komentarza w pliku z zadaniem).

    #> Warto też porównać operacje z użyciem różnej liczby *workers*, np. `max_workers=2` vs. `max_workers=4` na procesorach wielordzeniowych

import time
from concurrent.futures import ProcessPoolExecutor

def simple_math(a, b, op):
    if op == "+":
        return a + b

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        for _ in range(50):
            executor.submit(simple_math, 10, 20, "+")
    end_time = time.time()
    print(f"Czas dodawania: {end_time - start_time:.5f} sekund")

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        for _ in range(50):
            executor.submit(fibonacci, 30)
    end_time = time.time()
    print(f"Czas wykonywania Fibonacciego: {end_time - start_time:.5f} sekund")

    #Czas dodawania: 1.49176 sekund
    #Czas wykonywania Fibonacciego: 30.44068 sekund