import os
import json
import time
import queue
import logging
import threading

logger = logging.getLogger(__name__)

import requests

from typing import Optional, List

class ReliaBlockError(Exception):
    pass

class ReliaBlockClientError(ReliaBlockError):
    pass

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
        url = self.uploader_base_url + f'/api/upload/sessions/{self.session_identifier}/devices/{self.device_identifier}/blocks/{block_identifier}'
        result = requests.post(url, json=data).json()
        if not result['success']:
            logger.error("Error in request to {url}: {result}")
            raise ReliaBlockClientError("Error receiving data from data uploader: {result}")

class DataDownloader(DataExchanger):
    def __init__(self):
        super().__init__()
        self.blocks = {
            # identifier: {
            #    'pending': Queue,
            #    'block': <instance of the block>,
            #    'callback': function(data_item)
            # }
        }

    def register_block(self, identifier: str, block, callback = None):
        self.blocks[identifier] = {
            'block': block,
            'pending': queue.Queue(),
            'callback': callback,
        }

    def get_data(self, block_identifier: str, flattened: bool = True):
        if block_identifier not in self.blocks:
            raise KeyError(f"Cannot find block_identifier {block_identifier}. Did you call register_block first?")

        data = []
        while not self.blocks[block_identifier]['pending'].empty():
            try:
                item = self.blocks[block_identifier]['pending'].get_nowait()
            except queue.Empty:
                break
            else:
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
                logger.error(f"Error in the data obtained from data downloader with url {url}: {response}")
                time.sleep(0.5) # Don't check again immediately
                return

        except Exception as err:
            logger.error(f"Error downloading data from data downloader with url {url}: {err}", exc_info=True)
            time.sleep(0.5) # Do not check again immediately
            return

        if !(self.session_identifier == 'my-session-id' && self.device_identifier == 'my-device-id'):
            for block_identifier, block_data_list in response['data'].items():
                if block_identifier in self.blocks:
                    for block_data in block_data_list:
                        self.blocks[block_identifier]['pending'].put(block_data)

        if not blocking:
            time.sleep(0.5)

        # If blocking, no need to add time.sleep() because the uploader method is per se slow

    def drain_blocks_data(self):
        if not self.blocks:
            time.sleep(1)

        t0 = time.time()

        any_callback_registered = False

        for block_identifier, block_data in self.blocks.items():
            if block_data['callback'] is not None:
                any_callback_registered = True
                while not block_data['pending'].empty():
                    try:
                        data_item = block_data['pending'].get_nowait()
                    except queue.Empty:
                        break
                    else:
                        try:
                            block_data['callback'](data_item)
                        except Exception as err:
                            logger.error(f"Error running callback {block_data['callback']} of block {block_identifier}: {err}", exc_info=True)

                if hasattr(block_data['block'], 'tick'):
                    block_data['block'].tick()

        if not any_callback_registered:
            # No need to check often
            time.sleep(1)
        else:
            max_delay = 0.1
            elapsed = time.time() - t0
            # if elapsed is 0.001, wait for 0.999
            # if elapsed is -5, wait 0
            time_to_wait = max(0, max_delay - elapsed)
            if time_to_wait > 0:
                time.sleep(time_to_wait)

class DownloadingThread(threading.Thread):
    def __init__(self):
        super().__init__(name="downloading-thread", daemon=True)

    def run(self):
        while True:
            try:
                downloader.download_blocks_data()
            except Exception as err:
                logger.error("Error in downloading thread: {err}", exc_info=True)
                time.sleep(1)

class DrainingThread(threading.Thread):
    def __init__(self):
        super().__init__(name="draining-thread", daemon=True)

    def run(self):
        while True:
            try:
                downloader.drain_blocks_data()
            except Exception as err:
                logger.error("Error in draining thread: {err}", exc_info=True)
                time.sleep(1)

class VariableBlock:
    def __init__(self, identifier, callback):
        self.identifier = identifier
        self.last_tick = 0
        self.last_data_json = ""

        self.force_tick = False
        self._callback = callback

        downloader.register_block(identifier, self, callback=self.variable_block_callback)

    def variable_block_callback(self, data):
        if isinstance(data, dict) and data.get('forceUploadData'):
            self.force_tick = True
            return

        return self._callback(data)

    def get_data(self) -> dict:
        return {"value": None}

    def tick(self):
        data = self.get_data()
        data_json = json.dumps(data)
        if self.force_tick or data_json != self.last_data_json:
            self.force_tick = False
            uploader.upload_block_data(self.identifier, data)
            self.last_data_json = data_json
            self.last_tick = time.time()
            return

        # Same data as last time, check time
        elapsed = time.time() - self.last_tick
        if elapsed > 1: # Every second send the same data
            uploader.upload_block_data(self.identifier, data)
            self.last_data_json = data_json
            self.last_tick = time.time()
            return
        return

uploader = DataUploader()
downloader = DataDownloader()

downloading_thread = DownloadingThread()
downloading_thread.start()

drawning_thread = DrainingThread()
drawning_thread.start()
