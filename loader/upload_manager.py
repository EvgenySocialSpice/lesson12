import os
import random
from loader.exceptions import PictureFormatNotSupportedError, PictureNotUploadedError, OutOfFreeNamesErrors


class UploadManager:

    def get_free_filename(self, folder, file_type):
        attempts = 0
        RANGE_OF_IMAGE_NUMBERS = 100
        LIMIT_OF_ATTEMPTS = 10000

        while True:
            pic_name = random.randint(0, RANGE_OF_IMAGE_NUMBERS)
            filename_to_save = f'{pic_name}.{file_type}'
            os_path = os.path.join(folder, filename_to_save)
            is_filename_occupied = os.path.exists(os_path)

            if not is_filename_occupied:
                return filename_to_save

            attempts += 1
            if attempts > LIMIT_OF_ATTEMPTS:
                raise OutOfFreeNamesErrors('There are no free names to save image')

    def is_file_type_valid(self, file_type):
        if file_type.lower() in ['png', 'jpg', 'jpeg', 'webp', 'svg', 'tiff', 'giff']:
            return True
        return False

    def save_with_random_name(self, picture):
        # получаем данные картинки
        filename = picture.filename
        file_type = filename.split('.')[-1]

        # Проверяем валидность картинки
        if not self.is_file_type_valid(file_type):
            raise PictureFormatNotSupportedError(f'Формат {file_type} не поддерживается')

        # получаем свободное имя
        folder = os.path.join('.', 'uploads', 'images')
        filename_to_save = self.get_free_filename(folder, file_type)

        # сохраняем под новым именем
        try:
            picture.save(os.path.join(folder, filename_to_save))
        except FileNotFoundError:
            raise PictureNotUploadedError(f'{folder, filename_to_save}')

        return filename_to_save
