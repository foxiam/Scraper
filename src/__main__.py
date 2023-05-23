import sys
from scraper.scraper import Scraper
from scraper.file_writer import FileWriter
from scraper.scraper_config import ScraperConfig


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Ошибка! Укажите ссылку в качестве аргумента. Пример: python __main__.py https://example.com/news/page.html')
        exit()

    url = sys.argv[1]

    try:
        config = ScraperConfig(path = './config/scraper_config.json')
        
        parser = Scraper(url = url, config=config)
        parser.parse_page()
        text = parser.get_formatted_text()

        saver = FileWriter(url, config.target_directory)
        saver.write(text)
    except Exception as e:
        print(f'Ошибка обработки страницы: {e}')
