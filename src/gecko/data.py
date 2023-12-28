import datetime
import os
import logging
import re
import requests


logger = logging.getLogger()


class DataLoader:

    def __init__(self, base_url: str, data_dir='./data/soho/tmp') -> None:
        self.base_url = base_url
        self.data_dir = os.path.abspath(data_dir)
        os.makedirs(self.data_dir, exist_ok=True)

    def ls_images(start_datetime: datetime.datetime, end_datetime: datetime.datetime):
        pass

    def download_single(self, url: str, output_path: str, download_format: str) -> None:
        try:
            resp = requests.get(
                url=url,
                params={'downloadformat': download_format}
            )
            if resp.ok is True:
                with open(output_path, mode='wb') as f:
                    f.write(resp.content)
        except Exception as e:
            logger.error(f'Failed to load single URL: {url}')
            raise(e)


class JPEGDataLoader(DataLoader):

    def __init__(self, camera: str, data_dir: str='./data/soho/jpeg') -> None:
        self._year_escape_str = '+++++++++++'
        self.camera = camera
        if camera not in ('c2', 'c3'):
            raise ValueError(f'`camera` parameter should be one of these: c1, c2. You\'ve passed {camera}')

        super().__init__(
            base_url=f'https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/{self._year_escape_str}/{camera}/',
            data_dir=data_dir
        )

    def download_full_date(self, download_date: datetime.date) -> None:
        date_str = datetime.datetime.strftime(download_date, '%Y%m%d')
        base_url = self.base_url.replace(self._year_escape_str, str(download_date.year))
        download_url = os.path.join(base_url, date_str)
        logger.info(f'Downloading images from: {download_url}')
        resp = requests.get(download_url)
        
        if resp.ok is False:
            raise RuntimeError(f'Failed to download data from {download_url}: {resp.content.decode()}')

        all_images = sorted(list(set(re.findall(r'\d+_\d+_c\d_1024.jpg', resp.content.decode()))))
            
        for img in all_images:
            d_url = os.path.join(base_url, date_str, img)
            output_dir = os.path.join(self.data_dir, self.camera, date_str)
            os.makedirs(output_dir, exist_ok=True)
            d_output = os.path.join(output_dir, img)
            logger.info(f'Downloading {d_url} to {d_output}')
            print(f'Downloading {d_url} to {d_output}')
            self.download_single(
                d_url,
                d_output,
                'jpg'
            )


class FITSDataLoader(DataLoader):
    
    def __init__(self, camera: str, data_dir: str='./data/soho/fits') -> None:
        self._date_escape_str = '+++++++++++'
        if camera not in ('c2', 'c3'):
            raise ValueError(f'`camera` parameter should be one of these: c1, c2. You\'ve passed {camera}')

        super().__init__(
            base_url=f'https://umbra.nascom.nasa.gov/pub/lasco_level05/{self._date_escape_str}/{camera}/',
            data_dir=data_dir
        )

    def load_single(url: str) -> None:
        pass
