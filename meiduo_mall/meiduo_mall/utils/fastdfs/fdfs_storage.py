from django.core.files.storage import Storage
from django.conf import settings


class FastDFSStorage(Storage):
    """自定義文件儲存類"""

    def __init__(self, fdfs_base_url=None):
        # if not fdfs_base_url:
        #     self.fdfs_base_url = settings.FDFS_BASE_URL
        #
        # self.fdfs_base_url = fdfs_base_url
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

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

        return self.fdfs_base_url + name