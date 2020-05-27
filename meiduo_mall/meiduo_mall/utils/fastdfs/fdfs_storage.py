from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """自定義文件儲存類"""

    # def __init__(self, option=None):
    #     if not option:
    #         option = settings.CUSTOM_STORAGE_OPTIONS
    #
    #     pass

    def _open(seld, name, mode='rb'):
        pass

    def _save(self, name, content):
        pass

    def url(self, name):
        """
        返回文件的全路徑
        :param name: 文件相對路徑
        :return: 文件的全路徑
        """

        return 'http://192.168.181.132:8888/' + name
