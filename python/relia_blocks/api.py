import os
import json
import requests

from typing import Optional

class DataUploader:
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

    def upload_block_data(self, block_identifier: str, data: dict):
        result = requests.post(self.uploader_base_url + f'/api/upload/sessions/{self.session_identifier}/devices/{self.device_identifier}/blocks/{block_identifier}', json=data).json()
        if not result['success']:
            # TODO
            print(result)



uploader = DataUploader()
