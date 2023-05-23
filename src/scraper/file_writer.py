import os
import re


class FileWriter:
    """ Класс сохраняющий текст в файл.
        Может создавать путь файла на основе url (метод generate_path_from_url),
        также можно задать путь явно в конструкторе или в поле path.

        Использование:
        file_saver = FileSaver('https://example.com/news/page.html', './pages')
        file_saver.save(textVariable)
    """
    def __init__(self, url: str, target_directory: str ='./'):
        """
        :param url: ссылка
        :param target_directory: целевая директория.
        """
        
        self.__target_directory = target_directory
        self.update_path(url)

    def update_path(self, url: str):
        """ Обновление пути из url для сохранения текста статьи.
        :param url: ссылка
        """
        self.url = url
        self.__target_path = os.path.abspath(self.__target_directory)
        self.__generate_path_from_url()

    def __generate_path_from_url(self):
        """ Создание пути из url для сохранения текста статьи.
        """
        url_cut = re.findall(r'.*://(.*)', self.url)[0]

        if url_cut.endswith('/'):
            url_cut = url_cut[:-1]

        directory, file_name = os.path.split(url_cut)
        if file_name.find('.') != -1:
            file_name = re.sub(r'\.(.*)', '.txt', file_name)
        else:
            file_name += '.txt'

        self.__target_path = os.path.join(self.__target_path, directory, file_name)

    def write(self, text):
        """ Сохранение в файл.
        :param text: (str) текст.
        """
        directory, _ = os.path.split(self.__target_path)
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)

        text = text.encode('UTF-8')

        try:
            with open(self.__target_path, 'wb') as f:
                f.write(text)
            print(f'Статья сохранена в: {self.__target_path}')
        except Exception as e:
            print(f'Ошибка при сохранении статьи: {e}')

