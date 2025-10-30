import requests
from bs4 import BeautifulSoup
import csv # Добавим импорт для сохранения в CSV

# 1. Определяем URL, который будем парсить
URL = "http://books.toscrape.com/"

def scrape_books(url):
    print(f"--- Начинаем парсинг: {url} ---")
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Вызовет ошибку, если запрос неудачный
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    books_data = []

    # Находим все элементы с информацией о книгах
    all_books = soup.find_all('article', class_='product_pod')
    
    for book in all_books:
        title_element = book.find('h3').find('a')
        # Извлекаем название и обрезаем, если оно слишком длинное для заголовка
        title = title_element['title'] if title_element and 'title' in title_element.attrs else "Нет названия"
        
        # Находим цену (находится в теге <p> с классом 'price_color')
        price_element = book.find('p', class_='price_color')
        price = price_element.text.strip() if price_element else "Нет цены"
        
        books_data.append({
            "Title": title,
            "Price": price
        })
        
    return books_data

def save_to_csv(data, filename="scraped_books.csv"):
    if not data:
        print("Нет данных для сохранения.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Данные успешно сохранены в файл: {filename}")


if __name__ == "__main__":
    results = scrape_books(URL)
    save_to_csv(results)
