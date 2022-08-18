import time
import json
import shutil

import numpy as np
import redis

from gnuradio import gr

class abstract_time_sink(gr.sync_block):

    input_data_type = None

    def __init__(self, nop=1024, srate=32*1024, autoscale=False, *args, **kwargs):

        print(args, kwargs)

        gr.sync_block.__init__(
            self, 
            name="RELIA Time Sink",
            in_sig=[self.input_data_type],
            out_sig=[],
        )
        
        self._rdb = redis.StrictRedis()

        ##################################################
        # Parameters
        ##################################################
        self.nop = nop
        self.srate = srate
        self.autoscale = autoscale


    def get_nop(self):
        return self.nop

    def set_nop(self, nop):
        self.nop = nop

    def get_srate(self):
        return self.srate
       
    def set_srate(self, srate):
        self.srate = srate

    def get_autoscale(self):
        return self.autoscale

    def set_autoscale(self, autoscale):
        self.autoscale = autoscale

    def say_hello(self):
        print("Hello!")

    def work(self, input_items, output_items):
        # https://github.com/gnuradio/gnuradio/blob/b2c9623cbd548bd86250759007b80b61bd4a2a06/gr-qtgui/lib/time_sink_f_impl.cc#L496
        # time.sleep(0.1)

        input_items_bytes = input_items[0].tobytes()
        self._rdb.set('relia-time-sink-0', input_items_bytes)

        # real_numbers = [ str(num.real) for num in input_items[0]]
        # imag_numbers = [ str(num.imag) for num in input_items[0]]

        # contents = json.dumps(dict(real=real_numbers, imag=imag_numbers))
        # import hashlib
        # print(f"[{time.asctime()}] Writing...", hashlib.md5(contents.encode()).hexdigest())
        # open('/tmp/relia-data.json.tmp', 'w').write(contents)
        # shutil.move('/tmp/relia-data.json.tmp', '/tmp/relia-data.json')

        # print(time.asctime(), len(input_items[0]), input_items[0][0])
        # print("hola")
        return len(input_items[0])

class time_sink_c(abstract_time_sink):
    input_data_type = np.complex64

class time_sink_f(abstract_time_sink):
    input_data_type = np.float32

