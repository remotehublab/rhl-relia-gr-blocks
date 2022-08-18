import numpy as np
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
        # print("hola")
        return 0

class time_sink_c(abstract_time_sink):
    input_data_type = np.complex64

class time_sink_f(abstract_time_sink):
    input_data_type = np.float32

