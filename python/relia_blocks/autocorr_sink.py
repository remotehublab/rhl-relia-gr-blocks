import time
import json
import shutil
from relia_blocks.config_params import *
import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader

class autocorr_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, fac_size=512, fac_decimation=10,title='',autoScale=False, grid=True,yMin=0,yMax=1, useDB=True,sampRate=32000,*args, **kwargs):

        #print(args, kwargs)
        self.input_data_type = (np.complex64)

        gr.sync_block.__init__(
            self, 
            name="RELIA AutoCorr Sink",
            in_sig=[self.input_data_type],
            out_sig=[],
        )

        
        ##################################################
        # Parameters
        ##################################################
        self.fac_size = fac_size
        self.fac_decimation = fac_decimation
        self.title = title
        self.autoScale = autoScale
        self.grid = grid
        self.yMin = yMin
        self.yMax = yMax
        self.useDB = useDB       
        self.sampRate=sampRate 

    def get_autoscale(self):
        return self.autoscale

    def set_autoscale(self, autoscale):
        self.autoscale = autoscale


    def say_hello(self):
        print("Hello22!")

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
        #input_items=relia_fft(input_items,self.fftsize,self.nconnections)

        #fft_input_items=relia_fft(temp2)
        acf_input_items=relia_autocorr(input_items,self.fac_size,self.useDB)

        #print (np.shape(temp),type(temp),"Freq")

        for pos, input_item in enumerate(acf_input_items):
            streams[pos] = {
                'real': [ str(num) for num in input_item],

            }
        #print(np.shape(streams))

        data = {
            'block_type': 'relia_autocorr_sink',
            'type': self.input_data_type.__name__,
            'params': {
                'fac_size': self.fac_size,
                'fac_decimation': self.fac_decimation,
                'title': self.title,
                'autoScale': self.autoScale,
                'grid': self.grid,                
                'yMin': self.yMin,
                'yMax': self.yMax,                
                'useDB': self.useDB,
                'sampRate': self.sampRate,  
            },
            'data': {
                'streams': streams
            }

        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

