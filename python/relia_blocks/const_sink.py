import time
import json
import shutil

import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class abstract_const_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, nop=1024, autoscale=False, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Constellation Sink",
            in_sig=[self.input_data_type],
            out_sig=[],
        )
        
        ##################################################
        # Parameters
        ##################################################
        self.nop = nop
        self.autoscale = autoscale

    def get_autoscale(self):
        return self.autoscale

    def set_autoscale(self, autoscale):
        self.autoscale = autoscale

    def get_nop(self):
        return self.nop

    def set_nop(self, nop):
        self.nop = nop

    def say_hello(self):
        print("Hello!")

    def work(self, input_items, output_items):
		#https://github.com/gnuradio/gnuradio/blob/b2c9623cbd548bd86250759007b80b61bd4a2a06/gr-qtgui/lib/const_sink_c_impl.cc#L353        
		# time.sleep(0.1)
        # input_items_bytes = input_items[0].tobytes()
        # self._rdb.set('relia-time-sink-0', input_items_bytes)
        data = {
            'block_type': 'relia_const_sink_x',
            'type': self.input_data_type.__name__,
            'params': {
                'nop': self.nop,
		 		'autoscale': self.autoscale,

            },
            'data': {
                'streams': {
                    '0': {
                        'real': [ str(num.real) for num in input_items[0]],
                        'imag': [ str(num.imag) for num in input_items[0]],
                     }
            	}
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

class const_sink_c(abstract_const_sink):
    input_data_type = np.complex64

class const_sink_f(abstract_const_sink):
    input_data_type = np.float32

