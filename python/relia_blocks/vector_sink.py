import time
from relia_blocks.config_params import *
import json
import shutil

import numpy as np
from gnuradio import gr

from relia_blocks.api import uploader, downloader

class vector_sink_f(gr.sync_block):

    def __init__(self, vlen=1024, name="",x_start=0, x_step=1.0, x_axis_label="x-Axis", y_axis_label="y-Axis",  x_units="", y_units="", ref_level=0.0, grid=True, average=False,autoscale=False,ymin=-140.0,ymax=10.0, colors=[], labels=[], widths=[],nconnections=1, parent=None, *args, **kwargs):

        self.input_data_type = (np.float32, vlen)

        gr.sync_block.__init__(
            self, 
            name="RELIA Vector Sink",
            in_sig=[(np.float32, vlen)]*nconnections,
            out_sig=[],
        )


        downloader.register_block(self.identifier(), self)
        
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
        self.x_units = x_units
        self.y_units = y_units
        self.ref_level = ref_level
        self.grid = grid
        self.average = average
        self.autoscale = autoscale
        self.ymin = ymin
        self.ymax = ymax
        self.colors = colors
        self.labels = labels
        self.widths = widths


    def set_vlen(self, vlen):
        self.vlen = vlen

    def get_vlen(self):
        return self.vlen

    def set_x_start(self, x_start):
        self.x_start = x_start

    def get_x_start(self):
        return self.x_start

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

        web_data = downloader.get_data(self.identifier())
        if web_data:
            # TODO
            print()
            print('*' * 100)
            print(web_data)
            print('*' * 100)
            print()

#        print (np.shape(input_items[:,0,:]),"Vector")

        input_items2=np.array(input_items)
        input_items3=input_items2[:,0,:]
        input_items4=np.ndarray.tolist(input_items3)
        #print (np.shape(input_items4),type(input_items4),"Vector raw")
        #print (input_items4,"Vector")

        x,y=np.shape(input_items4) 
        if y>self.vlen:
            input_items4=adapt_array(input_items4,self.vlen)

        streams = {
            # 0: {
            #     'real': [ str(num) for num in input_items[0] ]
            #     'imag': [ str(num) for num in input_items[0] ]
            # }
        }
        for pos, input_item in enumerate(input_items4):
            #print (type(input_items4),"Vector")
            streams[pos] = {
                'x': [ str(num) for num in input_item],
            }


#        streams = {
            # 0: {
            # }
#        }
        #x,y,z=np.shape(input_items)
        #temp=np.reshape(np.array(input_items),(x,y*z))
        #temp=temp[:,:self.vlen]
        #temp=temp.tolist()
        #print(x,y,z)
        #print(np.shape(input_items.squeeze()[[0, 2]]))
        #temp=np.array([input_items[0][0][i] for i in range(self.nconnections)] + [input_items[0][2][i] for i in range(self.nconnections)])
        #print (np.shape(input_items),type(input_items),"Vector")
#        for pos, input_item in enumerate(input_items):
#             streams[pos] = {
#                 '0': [ str(num) for num in input_item],
#             }
             #print(streams[0])
        #print (np.shape(stream_0),type(stream_0[0]),"Vector")
        #print (stream_0[0],len(stream_0[3]),"Vector")

        data = {
            'block_type': 'relia_vector_sink_f',
            'type': self.input_data_type[0].__name__,
            'params': {
                'vlen': self.vlen,
                'x_start': self.x_start,
                'x_step': self.x_step,
                'x_axis_label': self.x_axis_label,
                'y_axis_label': self.y_axis_label,
                'name': self.name,
                'nconnections': self.nconnections,
                'x_units': self.x_units,
                'y_units': self.y_units,
                'ref_level': self.ref_level,
                'grid': self.grid,
                'average': self.average,
                'autoscale': self.autoscale,
                'ymin': self.ymin,
                'ymax': self.ymax,
                'colors': color_name2hex(self.colors),
                'labels': self.labels,
                'widths': self.widths,		 		
		 		
            },
#             'data': {
#                 'streams': {
#                     '0': stream_0,
#             	}
#             }
#        }
            'data': {
                'streams': streams
            }
        }

        uploader.upload_block_data(self.identifier(), data)

        time.sleep(0.1)
        return len(input_items[0])

