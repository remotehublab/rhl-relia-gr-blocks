import time
import json
import shutil
from relia_blocks.config_params import *
import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class abstract_const_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, nop=1024, name="", grid=False, autoscale=False, xmin=" ", xmax=" ",ymin=" ", ymax=" ", colors=[],labels=[],widths=[],styles=[],markers=[], nconnections=1, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Constellation Sink",
            in_sig=[self.input_data_type]* nconnections,
            out_sig=[],
        )

        
        ##################################################
        # Parameters
        ##################################################
        self.nop = nop
        self.name = name
        self.grid = grid
        self.autoscale = autoscale
        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.colors = colors
        self.labels = labels
        self.widths = widths
        self.styles = styles
        self.markers = markers
        self.nconnections = nconnections

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
            'block_type': 'relia_const_sink_x',
            'type': self.input_data_type.__name__,
            'params': {
                'nop': self.nop,
                'name': self.name,
                'nconnections': self.nconnections,                
                'grid': self.grid,                
                'autoscale': self.autoscale,
                'xmin': self.xmin,                
                'xmax': self.xmax,  
                'ymin': self.ymin,                
                'ymax': self.ymax,  
                'colors': color_name2hex(self.colors),     
                'labels': self.labels,   
                'widths': self.widths,   
                'styles': style_number2dotdash(self.styles),  
                'markers':  marker_number2shape(self.markers),
            },
            'data': {
                'streams': streams
            }

        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

class const_sink_c(abstract_const_sink):
    input_data_type = np.complex64

class const_sink_f(abstract_const_sink):
    input_data_type = np.float32

