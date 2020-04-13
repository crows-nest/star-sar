
#! /usr/bin/python3

from scipy.constants import c, pi
from math import sqrt, log10
import numpy as np


class ITUModel(object):

    def __init__(self, **config):
        print("no config to setup")
        pass

    def ITU_model_attenuation(self, d1, d2, f, d, hl, ho):
        """
        The ITU terrain loss model is a radio propagation model that 
        provides a method to predict the median path loss for a 
        telecommunication link
        
        Parameters
        ----------
        d1 : float
            Distance of obstruction from one terminal (km)
        d2 : float
            Distance of obstruction from the other terminal (km)
        f : float
            Frequency of transmission (GHz)
        d : float
            Distance from transmitter to receiver (km)
        hl : float
            Height of the line-of-sight link (m)
        ho : float
            Height of the obstruction (m)
        
        Returns
        -------
        float
            Additional loss (in excess of free-space loss) due to 
            diffraction (dB)

        """
        F1 = self._F1_radius(d1, d2, f, d)
        h = self._h_diff(hl, ho)
        Cn = self._terrain_clearance(h, F1)
        attenuation = self._diffraction_loss(Cn)

        return attenuation
    
    def _F1_radius(self, d1, d2, f, d):
        """
        calculate the radius of the first fresnel zone (m)
        
        Parameters
        ----------
        d1 : float
             Distance of obstruction from one terminal (km)
        d3 : float
            Distance of obstruction from the other terminal (km)
        f : float
            Frequency of transmission (GHz)
        d : float
            Distance from transmitter to receiver (km)
        Returns
        -------
        float
             Radius of the first Fresnel zone (m)
        """
        F1 = 17.3*sqrt((d1*d2/(f*d)))
        return F1
        
    def _h_diff(self, hl, ho):
        """
        calculate height difference
        
        Parameters
        ----------
        hl : float
             Height of the line-of-sight link (m)
        ho : float
            Height of the obstruction (m)
        Returns
        -------
        float
             The height difference (negative in the case that the LOS 
             path is completely obscured) (m)
        """
        return hl - ho

    def _terrain_clearance(self, h, F1):
        """
        calulate normalized terrain clearance
        
        Parameters
        ----------
        h : float
            The height difference (negative in the case that the LOS path 
            is completely obscured) (m)
        F1 : float
             Radius of the first Fresnel zone (m)
        
        Returns
        -------
        float
             Normalized terrain clearance
        """
        return (h/F1)
    
    def _diffraction_loss(self, Cn):
        """
        calculate loss in excess of free space loss (dB)
        
        Parameters
        ----------
        Cn : float
            Normalized terrain clearance
        
        Returns
        -------
        float
            Additional loss (in excess of free-space loss) 
            due to diffraction (dB)
        """

        return 10 - (20*Cn)


class FriisTrans(object):

    def __init__(self, Pt=3, Gt=2, Gr=15, mhz=2400):
        
        self.Pt=Pt
        self.Gt=Gt
        self.Gr=Gr
        self.mhz=mhz

    def dist_power_received(self, d):

        return self.power_received(d, Pt=self.Pt, Gt=self.Gt, 
                                   Gr=self.Gr, mhz=self.mhz)
        
    def power_received(self, d, Pt=3, Gt=2, Gr=15, mhz=2400):

        lamb = self.mhz_to_lambda(mhz)
        log_loss = 20*log10(lamb/(4*pi*d))
        return  Pt + Gt + Gr + log_loss

    def mhz_to_lambda(self, mhz):

        lamb = c/(mhz*1000000)
        return lamb


class RFModel(object):

    def __init__(self, data_proxy, layer="depth", dbi_thres=0.001, Pt=3, Gt=2, Gr=15, mhz=2400):
        
        self.data_proxy = data_proxy
        self.layer = layer
        self.dbi_thres = dbi_thres
        self.Pt = Pt
        self.Gt = Gt
        self.Gr = Gr
        self.mhz = mhz
        self.friis_model = FriisTrans()


    def binary_threshold_map(self, geo_loc, threshold):

        dict_layer = self._get_dict_layer()
        #currently only using free space model
        prob_map = np.zeros(dict_layer["data"].shape)

        
        it = np.nditer(prob_map, flags=['multi_index'])
        while not it.finished:
            
            geo_curr = self.data_proxy.get_geo_coord(it.multi_index, dict_layer)
            dist = self.data_proxy.get_dist_coord(geo_loc, geo_curr)

            signal_strength = self.friis_model.dist_power_received(dist*1000)
            if signal_strength >= threshold:
                prob_map[it.multi_index] = 1
            it.iternext()

        return prob_map
    
    def _get_dict_layer(self):
        return self.data_proxy.get_layer(self.layer)
        