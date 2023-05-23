import json

class ScraperConfig:
    """Класс для хранения параметров конфигурации для web scraping."""

    # ------------------------ настройки шаблонов форматирования исходного текста статьи
    # Ширина строки
    string_width = 80
    # Шаблон форматирования ссылок. %url_text% - текст ссылки. %url_href% - адрес ссылки.
    href_template = '%url_text% [%url_href%]'
    # Шаблон форматирования заголовка. %header% - текст заголовка.
    header_template = f'%header%\n\n'
    # Шаблон форматирования статьи. %article% - весь текст статьи.
    article_template = f'%article%\n'
    # Шаблон форматирования абзаца. %paragraph% - текст параграфа.
    paragraph_template = f'%paragraph%\n\n'

    # настройки для поиска тегов и имён классов html
    tag_processing_settings = {
        "default": {
            "tags_for_delete": ['script', 'noscript', 'style', 'noindex', 'form', 'img', 'figcaption'],
            "class_attrs_for_delete": ['social', 'reg', 'auth', 'footer', 'banner', 'mobile', 'comment', 'preview',
                                       'inject', 'incut', 'infoblock'],
            "tags_for_search": ['h2', 'p'],
            "class_attrs_for_search": ['content', 'context', 'article', 'text']
        }
    }

    target_directory = './'

    def __init__(self, path: str = None):
        """Инициализирует новый экземпляр объекта конфигурации.
        :param path: Строка, содержащая путь к файлу конфигурации. По умолчанию None.
        """
        if path:
            try:
                f = open(path, 'r')
                config = json.load(f)

                expected_keys = {
                    'target_directory', 'string_width', 'href_template', 'header_template', 
                    'article_template', 'paragraph_template', 'tag_processing_setup'
                }

                if expected_keys.issubset(config.keys()):
                    self.target_directory = config['target_directory']
                    # Устанавливаем ширину строки на значение из конфига.
                    self.string_width = config['string_width']
                    # Устанавливаем шаблон href на значение из конфига.
                    self.href_template = config['href_template']
                    # Устанавливаем шаблон заголовка на значение из конфига.
                    self.header_template = config['header_template']
                    # Устанавливаем шаблон статьи на значение из конфига.
                    self.article_template = config['article_template']
                    # Устанавливаем шаблон параграфа на значение из конфига.
                    self.paragraph_template = config['paragraph_template']
                    # Устанавливаем настройки обработки тегов на значение из конфига.
                    self.tag_processing_settings = config['tag_processing_setup']
                else:
                    raise Exception('[Error] Неверный формат конфигурации.')
                
            except Exception as e:
                print(f'Ошибка загрузки конфигурации, будет использована конфигурация по умолчанию. {e}')

            

