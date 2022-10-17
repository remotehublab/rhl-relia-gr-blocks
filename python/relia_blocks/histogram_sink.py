import time
import json
import shutil

import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class histogram_sink_x(gr.sync_block):

    input_data_type = None

    def __init__(self, size_hist=1024, bins=100, xmin=-1, xmax=1, name="", nconnections=1, parent=None, *args, **kwargs):

        self.input_data_type = (np.float32)

        gr.sync_block.__init__(
            self, 
            name="RELIA Histogram Sink",
            in_sig=[self.input_data_type],
            out_sig=[],
        )
        
        ##################################################
        # Parameters
        ##################################################
        self.size_hist = size_hist
        self.bins = bins
        self.xmin = xmin
        self.xmax = xmax
        self.name = name
        self.nconnections = nconnections
        # self.parent = parent

    def set_size_hist(self, size_hist):
        self.size_hist = size_hist

    def get_size_hist(self):
        return self.size_hist

    def set_bins(self, bins):
        self.bins = bins

    def get_bins(self):
        return bins

    def set_xmin(self, xmin):
        self.xmin = xmin

    def get_xmin(self):
        return self.xmin

    def set_xmax(self, xmax):
        self.xmax = xmax

    def get_xmax(self):
        return self.xmax

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_nconnections(self, nconnections):
        self.nconnections = nconnections

    def get_nconnections(self):
        return self.nconnections

    def say_hello(self):
        print("Hello!")

    def work(self, input_items, output_items):
        # https://github.com/gnuradio/gnuradio/blob/b2c9623cbd548bd86250759007b80b61bd4a2a06/gr-qtgui/lib/time_sink_f_impl.cc#L496
        # time.sleep(0.1)

        # input_items_bytes = input_items[0].tobytes()
        # self._rdb.set('relia-time-sink-0', input_items_bytes)
        data = {
            'block_type': 'relia_histogram_sink_x',
            'type': self.input_data_type.__name__,
            'params': {
                'size_hist': self.size_hist,
		 		'bins': self.bins,
		 		'xmin': self.xmin,
		 		'xmax': self.xmax,
            },
            'data': {
                'streams': {
                    '0': [ str(num) for num in input_items[0]],
                }
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])
