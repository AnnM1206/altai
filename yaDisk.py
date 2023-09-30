import yadisk
import os
import requests
from urllib.parse import urlencode
import zipfile
import io


class Storage():
    def __init__(self):
        self.disc = yadisk.YaDisk(token="")

    def download_files(self, url):
        base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        public_key = url
        # Получаем загрузочную ссылку
        final_url = base_url + urlencode(dict(public_key=public_key))
        response = requests.get(final_url)
        download_url = response.json()['href']
        # Загружаем файл и сохраняем его
        download_response = requests.get(download_url)
        with zipfile.ZipFile(io.BytesIO(download_response.content)) as zip_file:
            zip_file.extractall(path='predict')
            #print(zip_file.filelist[0].filename.split('/')[0])
            return zip_file.filelist[0].filename.split('/')[0]

    def mak_upload_file(self, files):
        l = list(self.disc.listdir(f"/predict"))
        max_num = 0
        for dirs in l:
            max_num = max(max_num, int(dirs.name))
        max_num = str(max_num + 1)
        self.disc.mkdir(f'/predict/{max_num}')
        self.disc.mkdir(f'/predict/{max_num}/clear')
        self.disc.mkdir(f'/predict/{max_num}/animal')
        self.disc.mkdir(f'/predict/{max_num}/broken')
        base_dir = f'/predict/{max_num}/'
        for key, value in files.items():
            name = key.split("/")[-1]
            try:
                self.disc.upload(key, base_dir + value + '/' + name)
            except:
                print('error')
        self.disc.publish(f'/predict/{max_num}')
        return [self.disc.get_meta(f'/predict/{max_num}').public_url, self.disc.get_download_link(f'/predict/{max_num}')]




