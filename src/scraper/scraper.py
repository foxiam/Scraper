from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re
from .scraper_config import ScraperConfig

class Scraper:
    """ Класс для выборки из веб-страницы полезной информации
    """

    # ссылка на сайт
    __url = ''
    # доменное имя
    __domain = ''
    # доменное имя для конфигурации
    __d_key = 'default'
    # инициализация переменой в которой будет хранится html код старицы (str)
    _html_page = ''
    # BeautifulSoup объект страницы
    __soup_obj = None
    # заголовок страницы (str)
    __header = ''
    # список объектов абзацев [bs4.element.Tag, ]
    __paragraphs_obj_list = []
    # отформатированный текст
    __formatted_text = ''
    # объект конфигурации
    __config = None

    def __init__(self, url: str, config: ScraperConfig = None):
        """Инициализирует объект парсера со ссылкой на сайт и объектом конфигурации. 
        :param url: ссылка на страницу для парсинга. Пример: "https://example.com/news/page.html"
        :param config: экземпляр класса ScraperConfig, содержащий настройки парсера.
        """

        if config and 'default' in config.tag_processing_settings:
            self.__config = config
        else:  
            self.__config = ScraperConfig()

        self.update_url(url)

    def update_url(self, url: str):
        """ Обновление ссылки на сайт
        :param url: ссылка на страницу для парсинга.
        """
        self.__url = url
        self.__domain = urlparse(url).netloc
        if self.__domain in self.__config.tag_processing_settings:
            self.__d_key = self.__domain
        else:
            self.__d_key = 'default'
        

    def __send_request(self):
        """ Отправка запроса для получения страницы
        """
        response = requests.get(self.__url)
        self.__html_page = response.text

    def __create_soup_obj(self):
        """ Создание объекта BeautifulSoup
        """
        if not self.__html_page:
            self.__soup_obj = None
            return

        self.__soup_obj = BeautifulSoup(self.__html_page, "html.parser")

    def __delete_unnecessary_tags(self):
        """ Удаление не нужных тегов из soup.
        """
        tag_processing_settings = self.__config.tag_processing_settings[self.__d_key]
        tags_for_delete = tag_processing_settings['tags_for_delete']
        class_attrs_for_delete = '|'.join(tag_processing_settings['class_attrs_for_delete'])

        if tags_for_delete:
            for tag in self.__soup_obj.body.findAll(tags_for_delete):
                tag.extract()

        if class_attrs_for_delete:
            for tag in self.__soup_obj.body.findAll(attrs={'class': re.compile(class_attrs_for_delete)}):
                tag.extract()

    def __find_header_from_soup(self):
        """ Нахождение заголовка из self.__soup_obj
        """
        header_obj = self.__soup_obj.body.find('h1')
        header = ''
        if header_obj is not None:
            header = header_obj.get_text()
        else:
            header_obj = self.__soup_obj.head.find('meta', attrs={'name': 'title'})
            if header_obj:
                header = header_obj.attrs['content']

        self.__header = header

    def __find_paragraphs(self):
        """ Нахождение тегов (bs4.element.Tag) с абзацами
        """
        tag_processing_settings = self.__config.tag_processing_settings[self.__d_key]
        tags_for_search = tag_processing_settings['tags_for_search']
        class_attrs_for_search = '|'.join(tag_processing_settings['class_attrs_for_search'])
        content_pattern = re.compile(class_attrs_for_search)
        content = self.__soup_obj.body.findAll(attrs={"class": content_pattern})
        p_objects = []
        already_used = []

        for item in content:
            paragraphs = item.findAll(tags_for_search)
            for p in paragraphs:
                if id(p) in already_used:
                    continue
                p_objects.append(p)
                already_used.append(id(p))

        self.__paragraphs_obj_list = p_objects

    def __add_to_paragraph_href(self, paragraph_obj):
        """ Добавление в текст объекта параграфа URL в квадратных скобках
        :param paragraph_obj: bs4.element.Tag
        """
        for a in paragraph_obj.findAll('a'):
            if a.has_attr('href') and a.string:
                href_template = self.__config.href_template
                href = a.attrs['href']
                if href.startswith('/'):
                    href = f'https://{self.__domain}{href}'
                href_template = href_template.replace('%url_href%', href)
                href_template = href_template.replace('%url_text%', a.string)
                a.string.replace_with(href_template)

    def __split_paragraph(self, paragraph=''):
        """ Разбивка одного абзаца по указанному размеру self.__config.string_width.
        :param paragraph: абзац.
        :return: строка разбитая по максимальной длине
        """
        string_width = self.__config.string_width
        words_list = paragraph.split()
        formatted_paragraph = ''
        tmp = ''

        for word in words_list:
            current_tmp = f'{tmp} {word}'.strip()

            if len(current_tmp) == string_width:
                formatted_paragraph += f'{current_tmp}\n'
                tmp = ''
            elif len(current_tmp) > string_width:
                formatted_paragraph += f'{tmp}\n'
                tmp = word
            else:  # len(tmp_current) < max_len
                tmp = current_tmp

        formatted_paragraph += tmp
        return formatted_paragraph.strip()

    def __split_all_paragraphs(self, paragraphs=''):
        """ Разбивка всех абзацев по указанному размеру.
        :param paragraphs: абзацы.
        :return:
        """
        string_list = paragraphs.splitlines()
        new_string_list = []
        for string in string_list:
            new_string_list.append(self.__split_paragraph(string))

        return '\n'.join(new_string_list)

    def __formate_text(self):
        """ Форматирование промежуточных данных в текст для сохранения
        """
        # добавление заголовка
        header_template = self.__config.header_template
        header = header_template.replace('%header%', self.__header)
        rendered_text = header

        # добавление абзацев статьи
        article = ''
        for p_obj in self.__paragraphs_obj_list:
            self.__add_to_paragraph_href(p_obj)
            paragraph = p_obj.get_text()
            paragraph_template = self.__config.paragraph_template
            article += paragraph_template.replace('%paragraph%', paragraph)
        article_template = self.__config.article_template
        rendered_text += article_template.replace('%article%', article)

        # разбиение на максимальную длину
        rendered_text = self.__split_all_paragraphs(rendered_text)

        self.__formatted_text = rendered_text

    def get_formatted_text(self):
        """
        :return: отформатированный текст
        """
        return self.__formatted_text

    def parse_page(self):
        """ Парсинг страницы
        """
        self.__send_request()
        self.__create_soup_obj()
        if self.__soup_obj is not None:
            self.__delete_unnecessary_tags()
            self.__find_header_from_soup()
            self.__find_paragraphs()
            self.__formate_text()
