import json
from classes.exceptions import DataSourceBrokenException
# from pprint import pprint as pp


class DataManager:
    def __init__(self, path):
        self.path = path  # путь к файлу с данными
        pass

    def _load_data(self):
        """Загружает данные из файла для использования другими методами"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException('Файл с данными поврежден')
        return data

    def _save_data(self, data):
        """перезаписывает переданные данные в файл"""
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """отдает полный список данных"""
        data = self._load_data()
        return data

    def search(self, substring):
        """отдает посты содержащие substring"""
        posts = self._load_data()
        substring = substring.lower()
        matching_posts = [post for post in posts if substring in post['content'].lower()]
        return matching_posts

    def add(self, post):
        """добавляет этот пост в список постов"""
        if type(post) != dict:
            raise TypeError('This is not right format')

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)
