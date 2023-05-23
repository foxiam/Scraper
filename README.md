# Scrapper
Утилита для сбора только полезной информации с сайтов. И для сохранения отформатированных данных в файл.

## Contents
1. [Requirements](#requirements)
2. [Usage](#usage)
3. [How to work](#how-to-work)
4. [ScraperConfig](#scraperconfig)
5. [Scraper](#scraper)
6. [FileWriter](#filewriter)
7. [Work example](#work-example)
8. [Further development](#further-development)

## Requirements

- python 3.10+
- beautifulsoup4 4.12.2
- certifi 2023.5.7
- charset-normalizer 3.1.0
- idna 3.4
- requests 2.31.0
-  soupsieve 2.4.1
- urllib3 2.0.2

Автоматическая установка всех зависимостей.
```console
pip install -r requirements.txt
```

##### [Back to Contents](#contents)

## Usage
Executable file \_\_main\_\_.py

Пример запуска:
```console
python __main__.py https://example.com/news/page.html
```

##### [Back to Contents](#contents)

## How to work

- `__send_request()`: отправляет запрос на указанный URL и возвращает HTML-страницу в виде текста. В этой функции мы используем библиотеку requests для отправки HTTP-запроса на указанный URL.
- `__create_soup_obj()`: создает объект класса `BeautifulSoup`, используя полученную HTML-страницу из предыдущего шага. В этой функции используется библиотека `bs4` для создания объекта класса `BeautifulSoup`, который позволяет нам обрабатывать HTML-код и находить нужные нам элементы на странице.
- `__delete_unnecessary_tags()`: проходит по объекту BeautifulSoup и удаляет все теги, названия которых указаны в списке `tags_for_delete`, а также все теги с именами классов, указанных в списке `class_attrs_for_delete`.
- __find_header_from_soup(): ищет тег `<h1>` и тег `<meta>` с атрибутом `name="title"`. Если находит заголовок, то записывает его в `__header`.
- `__find_paragraphs()`: ищет все теги, названия которых содержатся в списке `tags_for_search`, и атрибуты класса, которые содержатся в списке `class_attrs_for_search`, и сохраняет их содержимое в `__paragraphs_obj_list`.
- `__formate_text()`: функция форматирует текст статьи с помощью заданных шаблонов форматирования, которые мы можем настроить в файле `scraper_config.json`.
- Далее создается объект класса `FileWriter`, в который передается URL и путь до целевой директории. Данный класс автоматически генерирует путь к файлу из URL.
- После выполнения всех шагов используется метод `write` из класса `FileWriter`, для записи отформатированной статьи в текстовый файл.

##### [Back to Contents](#contents)

## ScraperConfig
Класс ScraperConfig предназначен для хранения параметров конфигурации для web scraping. В нем определены настройки шаблонов форматирования исходного текста статьи, а также настройки для поиска тегов и имён классов html.

В конструкторе класса ScraperConfig мы принимаем строку path, содержащую путь к файлу конфигурации. Если путь задан, то мы пытаемся открыть файл и загрузить настройки из него с помощью модуля json. Если загрузка прошла успешно, то мы устанавливаем значения настроек из конфигурации. Если произошла ошибка при загрузке конфигурации, то мы выводим соответствующее сообщение и используем настройки по умолчанию.

- [**scraper_config.json**](https://github.com/foxiam/Scraper/blob/master/src/config/scraper_config.json)
- [**scraper_config.scheme.json**](https://github.com/foxiam/Scraper/blob/master/src/config/scraper_config_schema.json)

##### [Back to Contents](#contents)

## Scraper
Класс `Scraper` предназначен для выборки полезной информации из веб-страницы. Класс содержит методы для отправки запроса на получение страницы, создания BeautifulSoup объекта страницы, удаления тегов, поиска заголовка и абзацев, форматирования и разбиения текста. Класс позволяет получить отформатированный текст страницы, который можно сохранить или использовать в дальнейшем. Класс также содержит настройки конфигурации, которые определяют, какие теги и классы будут удалены, как будет отформатирован текст и т.д.

### Usage example
```python
config = ScraperConfig(path = './config/scraper_config.json')
        
parser = Scraper(url = url, config=config)
parser.parse_page()
text = parser.get_formatted_text()
```

##### [Back to Contents](#contents)

## FileWriter
Класс `FileWriter` предназначен для сохранения текста в файл. Он создаеь путь к файлу на основе URL-адреса. Класс содержит методы для обновления пути из URL-адреса и для записи текста в файл.

### Usage example
```python
saver = FileWriter(url, config.target_directory)
saver.write(text)
```

##### [Back to Contents](#contents)

### Work example

- [lenta.ru](https://lenta.ru/news/2023/05/23/futurephone/) -> [Formatted text](https://github.com/foxiam/Scraper/blob/master/src/pages/lenta.ru/news/2023/05/23/futurephone.txt)
- [habr.com](https://habr.com/ru/news/737080/) -> [Formatted text](https://github.com/foxiam/Scraper/blob/master/src/pages/habr.com/ru/news/737080.txt)
- [habr.com](https://habr.com/ru/companies/smartengines/news/737002/) -> [Formatted text](https://github.com/foxiam/Scraper/blob/master/src/pages/habr.com/ru/companies/smartengines/news/737002.txt)
- [www.gazeta.ru](https://www.gazeta.ru/tech/news/2023/05/23/20505092.shtml) -> [Formatted text](https://github.com/foxiam/Scraper/blob/master/src/pages/www.gazeta.ru/tech/news/2023/05/23/20505092.txt)
- [example.com](https://example.com/news/page.html)-> [Formatted text](https://github.com/foxiam/Scraper/blob/master/src/pages/example.com/news/page.txt)

### Further development
- Добавить возможность сохранения файлов в разных форматах, например markdown или html.
- Добавить поддержку изображений, таблиц, блоков с кодом и т. д.
- Встроить языковую модель, для более точной фильтрации текста и упрощения конфигурации.
