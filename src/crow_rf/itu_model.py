#! /usr/bin/python3

from math import sqrt


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