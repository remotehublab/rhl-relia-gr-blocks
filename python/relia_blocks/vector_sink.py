import time
import json
import shutil

import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class vector_sink_f(gr.sync_block):


    def __init__(self, vlen=1024, x_start=0, x_step=1.0, x_axis_label="x-Axis", y_axis_label="y-Axis", name="", nconnections=1, parent=None, *args, **kwargs):

        self.input_data_type = (np.float32, vlen)

        gr.sync_block.__init__(
            self, 
            name="RELIA Vector Sink",
            in_sig=[(np.float32, vlen)],
            out_sig=[],
        )
        
        ##################################################
        # Parameters
        ##################################################
        self.vlen = vlen
        self.x_start = x_start
        self.x_step = x_step
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.name = name
        self.nconnections = nconnections
        # self.parent = parent

    def set_vlen(self, vlen):
        self.vlen = vlen

    def get_vlen(self):
        return self.vlen

    def set_x_start(self, x_start):
        self.x_start = x_start

    def get_x_start(self):
        return x_start

    def set_x_step(self, x_step):
        self.x_step = x_step

    def get_x_step(self):
        return self.x_step

    def set_x_axis_label(self, x_axis_label):
        self.x_axis_label = x_axis_label

    def get_x_axis_label(self):
        return self.x_axis_label

    def set_y_axis_label(self, y_axis_label):
        self.y_axis_label = y_axis_label

    def get_y_axis_label(self):
        return self.y_axis_label

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
		#https://github.com/gnuradio/gnuradio/blob/b2c9623cbd548bd86250759007b80b61bd4a2a06/gr-qtgui/lib/const_sink_c_impl.cc#L353        
		# time.sleep(0.1)
        # input_items_bytes = input_items[0].tobytes()
        # self._rdb.set('relia-time-sink-0', input_items_bytes)

        stream_0 = []
        if len(input_items[0]):
            stream_0 = [ str(num) for num in input_items[0][-1] ]

        data = {
            'block_type': 'relia_vector_sink_f',
            'type': self.input_data_type[0].__name__,
            'params': {
                'vlen': self.vlen,
		 		'x_start': self.x_start,
		 		'x_step': self.x_step,
		 		'x_axis_label': self.x_axis_label,
		 		'y_axis_label': self.y_axis_label,
            },
            'data': {
                'streams': {
                    '0': stream_0,
            	}
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

