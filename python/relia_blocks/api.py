import os
import json
import time
import logging
import threading

logger = logging.getLogger(__name__)

import requests

from typing import Optional, List

class DataExchanger:
    def __init__(self):
        if not os.path.exists('relia.json'):
            import glob
            log = open('/tmp/output.txt', 'w')
            log.write(str(glob.glob('*'))  + '\n')
            log.write(os.path.abspath('.'))
            raise Exception("Configuration relia.json not found")
        
        self.configuration = json.load(open('relia.json'))
        self.uploader_base_url = self.configuration['uploader_base_url']
        self.session_identifier = self.configuration['session_id']
        self.device_identifier = self.configuration['device_id']

class DataUploader(DataExchanger):
    def upload_block_data(self, block_identifier: str, data: dict):
        result = requests.post(self.uploader_base_url + f'/api/upload/sessions/{self.session_identifier}/devices/{self.device_identifier}/blocks/{block_identifier}', json=data).json()
        if not result['success']:
            # TODO
            print(result)

class DataDownloader(DataExchanger):
    def __init__(self):
        super().__init__()
        self.blocks = {
            # identifier: {
            #    'pending': [],
            #    'block': <instance of the block>,
            # }
        }

    def register_block(self, identifier: str, block):
        self.blocks[identifier] = {
            'block': block,
            'pending': [],
        }

    def get_data(self, block_identifier: str, flattened: bool = True):
        if block_identifier not in self.blocks:
            raise KeyError(f"Cannot find block_identifier {block_identifier}. Did you call register_block first?")

        data = []
        while len(self.blocks[block_identifier]['pending']) > 0:
            item = self.blocks[block_identifier]['pending'].pop()
            data.append(item)

        if flattened:
            flattened_data = {}
            for item in data:
                flattened_data.update(item)
            return flattened_data

        return data

    def download_blocks_data(self, blocking: bool = True):
        if not self.blocks:
            time.sleep(0.1)
            return
        blocking_str = '1' if blocking else '0'
        url = self.uploader_base_url + f'/api/download/sessions/{self.session_identifier}/devices/{self.device_identifier}?blocking={blocking_str}'
        try:
            response = requests.get(url).json()
            if not response['success']:
                return

        except Exception as err:
            logger.error(f"Error downloading data from data downloader with url {url}: {err}", exc_info=True)
            time.sleep(0.1)
            return
        
        for block_identifier, block_data_list in response['data'].items():
            if block_identifier in self.blocks:
                for block_data in block_data_list:
                    self.blocks[block_identifier]['pending'].append(block_data)

class DownloadingThread(threading.Thread):
    def __init__(self):
        super().__init__(name="downloading-thread", daemon=True)

    def run(self):
        while True:
            downloader.download_blocks_data()

uploader = DataUploader()
downloader = DataDownloader()

downloading_thread = DownloadingThread()
downloading_thread.start()
