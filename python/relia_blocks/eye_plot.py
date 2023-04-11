import time
import json
import shutil

import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class eye_plot(gr.sync_block):

    input_data_type = np.float32

    def __init__(self, nop=1024, samp_rate=32*1024, time_delay=40, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Eye Plot",
            in_sig=[self.input_data_type],
            out_sig=[],
        )
        
        ##################################################
        # Parameters
        ##################################################
        self.nop = nop
        self.samp_rate = samp_rate
        self.time_delay = time_delay


    def get_nop(self):
        return self.nop

    def set_nop(self, nop):
        self.nop = nop

    def get_samp_rate(self):
        return self.samp_rate
       
    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_time_delay(self):
        return self.time_delay

    def set_time_delay(self, time_delay):
        self.time_delay = time_delay

    def say_hello(self):
        print("Hello!")

    def work(self, input_items, output_items):
        # https://github.com/gnuradio/gnuradio/blob/b2c9623cbd548bd86250759007b80b61bd4a2a06/gr-qtgui/lib/time_sink_f_impl.cc#L496
        # time.sleep(0.1)

        # input_items_bytes = input_items[0].tobytes()
        # self._rdb.set('relia-time-sink-0', input_items_bytes)

        streams = {
            # 0: {
            #     'real': [ str(num) for num in input_items[0] ]
            #     'imag': [ str(num) for num in input_items[0] ]
            # }
        }

        for pos, input_item in enumerate(input_items):
            streams[pos] = {
                'real': [ str(np.real(num)) for num in input_item],
            }

        data = {
            'block_type': 'relia_eye_plot_x',
            'type': self.input_data_type.__name__,
            'params': {
                'srate': self.samp_rate,
                'nop': self.nop,
                'time_delay': self.time_delay,
            },
            'data': {
                'streams': streams
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

