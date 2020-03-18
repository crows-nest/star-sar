from scipy.constants import c, pi
from math import log10

class FrisTrans(object):

    def __init__(self, **config):
        print("no config to setup")
        
    
    def power_received(self, d, Pt=100, Gt=-50, Gr=10, mhz=2400):

        lamb = self.mhz_to_lambda(mhz)
        log_loss = 20*log10(lamb/(4*pi*d))
        return  Pt + Gt + Gr + log_loss

    def mhz_to_lambda(self, mhz):

        lamb = c/(mhz*1000000)
        return lamb
