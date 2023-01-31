import time
import json
import shutil
from relia_blocks.config_params import *
import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader


class abstract_time_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, nop=1024, srate=32*1024, name="", ylabel="Amplitude", yunit="", grid=False, autoscale=False, colors=[],labels=[],widths=[],styles=[], nconnections=1, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Time Sink",
            in_sig=[self.input_data_type] * nconnections,
            out_sig=[],
        )
        
        ##################################################
        # Parameters
        ##################################################
        self.nop = nop
        self.srate = srate
        self.name = name
        self.ylabel = ylabel
        self.yunit = yunit
        self.grid = grid
        self.autoscale = autoscale
        self.colors = colors
        self.labels = labels
        self.nconnections = nconnections
        

    def get_nop(self):
        return self.nop

    def set_nop(self, nop):
        self.nop = nop

    def get_srate(self):
        return self.srate
       
    def set_srate(self, srate):
        self.srate = srate

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_nconnections(self):
        return self.nconnections

    def set_nconnections(self, nconnections):
        self.nconnections = nconnections

    def get_ylabel(self):
        return self.ylabel

    def set_ylabel(self, ylabel):
        self.ylabel = ylabel

    def get_yunit(self):
        return self.yunit

    def set_yunit(self, yunit):
        self.yunit = yunit

    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid

    def get_autoscale(self):
        return self.autoscale

    def set_autoscale(self, autoscale):
        self.autoscale = autoscale

    def get_colors(self):
        return self.colors

    def set_colors(self, colors):
        self.colors = colors

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
                'real': [ str(num.real) for num in input_item],
                'imag': [ str(num.imag) for num in input_item],
            }

        data = {
            'block_type': 'relia_time_sink_x',
            'type': self.input_data_type.__name__,
            'params': {
                'srate': self.srate,
                'nop': self.nop,
                'name': self.name,
                'nconnections': self.nconnections,                
                'ylabel': self.ylabel,                
                'yunit': self.yunit,                
                'grid': self.grid,                
                'autoscale': self.autoscale,                
                'colors': color_name2hex(self.colors),     
                'labels': self.labels,                                         
            },
            'data': {
                'streams': streams
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

class time_sink_c(abstract_time_sink):
    input_data_type = np.complex64

class time_sink_f(abstract_time_sink):
    input_data_type = np.float32

