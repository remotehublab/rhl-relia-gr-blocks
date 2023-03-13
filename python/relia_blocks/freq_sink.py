import time
import json
import shutil
from relia_blocks.config_params import *
import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class abstract_freq_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, fftsize=512, wintype="window.WIN_BLACKMAN_hARRIS", fc=0, bw=1,name="",label="",units="",grid=False, autoscale=False,ymin=" ", ymax=" ",axislabels=True, average=1.0,colors=[],labels=[],widths=[], nconnections=1, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Frequency Sink",
            in_sig=[self.input_data_type]* nconnections,
            out_sig=[],
        )

        
        ##################################################
        # Parameters
        ##################################################
        self.fftsize = fftsize
        self.wintype = wintype
        self.fc = fc
        self.bw = bw
        self.name = name
        self.label = label
        self.units = units
        self.grid = grid
        self.autoscale = autoscale
        self.ymin=ymin
        self.ymax=ymax
        self.axislabels=axislabels
        self.colors = colors
        self.widths = widths
        self.nconnections = nconnections
        self.labels = labels
        self.average=average
        

    def get_autoscale(self):
        return self.autoscale

    def set_autoscale(self, autoscale):
        self.autoscale = autoscale


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
        #print (np.shape(input_items),type(input_items),"Freq raw")
        input_items=relia_fft(input_items,self.fftsize,self.nconnections)

        #fft_input_items=relia_fft(temp2)

        #print (np.shape(temp),type(temp),"Freq")

        for pos, input_item in enumerate(input_items):
            streams[pos] = {
                'real': [ str(num) for num in input_item],

            }
        #print(np.shape(streams))

        data = {
            'block_type': 'relia_freq_sink_x',
            'type': self.input_data_type.__name__,
            'params': {

                'fftsize': self.fftsize,
                #'wintype': "'"+self.wintype+"'",
                'fc': self.fc,
                'bw': self.bw,
                'name': self.name,
                'label': self.label,
                'units': self.units,
                'grid': self.grid,                
                'autoscale': self.autoscale,
                'ymin': self.ymin,                
                'ymax': self.ymax,  
                'axislabels': self.axislabels,  
                'colors': color_name2hex(self.colors),     
                'labels': self.labels,   
                'widths': self.widths,   
                'nconnections': self.nconnections,  
                'average': average_n2n(self.average), 
            },
            'data': {
                'streams': streams
            }

        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

class freq_sink_c(abstract_freq_sink):
    input_data_type = np.complex64

class freq_sink_f(abstract_freq_sink):
    input_data_type = np.float32

