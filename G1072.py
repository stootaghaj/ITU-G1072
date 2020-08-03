#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 13:54:29 2020

@author: saman
"""

#from __future__ import division

import numpy as np
import argparse

            
def MOSfromR_Value(Q):
    MOS_MAX = 4.64;
    MOS_MIN = 1.3;
    MOS = MOS_MIN + (MOS_MAX-MOS_MIN)/100*Q + Q*(Q-60)*(100-Q)* 7.0e-6
    return MOS.clip(min=1.3, max=4.64)
       
#transform data from R to MOS  for an array of values

def MOSfromR(Q):
    MOS = np.zeros(Q.shape)
    MOS_MAX = 4.64;
    MOS_MIN = 1.3;
    for i in range(len(Q)):
        if (Q[i] > 0 and Q[i] < 100):
            MOS[i] = MOS_MIN + (MOS_MAX-MOS_MIN)/100*Q[i] + Q[i]*(Q[i]-60)*(100-Q[i])* 7.0e-6
        elif (Q[i] >= 100):
            MOS[i] = MOS_MAX
        else:
            MOS[i] = MOS_MIN
        return MOS.clip(min=1.3, max=4.64)
    
 
def TVQ(framerate, FLR, coeff):
   
    if FLR < 1:
        FLR = 0;
    IVD= coeff[0]+coeff[1]*framerate**2+coeff[2]*framerate+coeff[3]*np.log(FLR+1)
    return IVD.clip(min=0, max=61.29)
    
def VF(bitrate, framerate, coding_res, coeff):
    bitrate = bitrate*1000    
    bitperpixel = bitrate/(framerate*coding_res)
    IVF = coeff[0] + coeff[1]*np.log(bitperpixel*bitrate) + coeff[2]*bitrate
    return IVF.clip(min=0, max=75.94)
    
    
def VU(bitrate, framerate, coding_res, coeff):
    bitrate = bitrate*1000 
    bitperpixel = bitrate/(framerate*coding_res)
    scaleratio = coding_res/(1080*1920)
    IVU = coeff[0] + coeff[1]*np.log(bitperpixel*bitrate) + coeff[2]*np.log(scaleratio)
    return IVU.clip(min=0, max=68.08)

    
def INPQ(Delay, coeff):
        
    IQR= coeff[0]/(1+np.exp(coeff[1]-coeff[2]*Delay))+coeff[3]    
    
    return IQR.clip(min=0, max=68.98)


def IQ_Frame(fr, FLR, coeff):    
    if FLR < 1:
        FLR = 0;
    I_IQ_frames = coeff[0]+coeff[1]*fr**2+coeff[2]*fr+coeff[3]*np.log(FLR+1);
    
    return I_IQ_frames.clip(min=0, max=68.98)
    

def VQ(bitrate, NumPixelPerFrame, framerate, TSpacketLossV, TSburstinessV, coeff):
             
     BitPerPixel = (bitrate*1000000)/(NumPixelPerFrame*framerate)
     
     ContentComplexity = coeff[4]*np.exp(coeff[5]*BitPerPixel) + coeff[6]
     
     QcodV = coeff[0]*np.exp(coeff[1]*BitPerPixel) + coeff[2]*ContentComplexity + coeff[3]
     TSburstinessV=0;
     I_codn = np.minimum(QcodV, 65.)
     LossMagnitudeNP = (coeff[9]-I_codn)*TSpacketLossV/(I_codn*(coeff[10]*TSburstinessV+coeff[11])+TSpacketLossV)
     LossMagnitudeE = coeff[12]*np.exp(coeff[13]*LossMagnitudeNP) - coeff[12]
     I_tras = coeff[7]*np.log(coeff[8]*LossMagnitudeE+1.)

     return I_codn.clip(min=0,max=78.78),I_tras

def FrameLR(br, fr, delay, pl):
    if delay < 16:
        AVG_fps = fr
    else:
        AVG_fps = fr*np.exp(-(0.08526 + 0.00073*fr + 1.425e-04*br*fr)*(0.09656*delay - 1.5)*pl);
    FLR = 100*(fr - AVG_fps)/fr
    print("AVG_fps:", AVG_fps)
    print("FLR:", FLR)
    return FLR

def test_model(bitrate, coding_res, flr, PL_UDP, framerate, delay, Iclss, Vclss):

# set the coefficients 
    
# VF Video Fragementation coef    
    VFcoef = [[2.1, -5.426, 0.0005258],
             [13.79, -8.017, 0.0005442],
             [11.21, -10.59, 0.0006314]];

# VU Video Unclearness coef    
    
    VUcoef = [[4.299, -2.016, -17.99], 
              [18.58, -3.422, -15.38],
              [17.13, -4.494, -7.844]];          
    
# VQ Video Quality coef based on the updated coef of G.1071    

    VQcoef = [[  5.25052380e+01,  -2.80170325e+01,  -2.68405109e+00,
            5.46647668e+00,   1.24214486e+01,  -2.80191642e+01,
            2.15799183e-01,   1.97091683e+01,   3.35830546e+03,
            2.83699150e+01,   4.60029723e-04,   2.34972977e-02,
            1.64739513e-03,   8.95913579e-02],[  3.79882097e+01,  -1.37207634e+01,   8.57836656e+00,
            3.26581290e+00,   6.83275916e+00,  -1.27997288e+02,
            4.79594798e-01,   6.12878511e-01,   1.39396166e-03,
            5.62892863e+01,   4.60000000e-04,   4.75669545e-03,
            5.81327058e-02,   2.38014343e+00], [  4.77463038e+01,  -1.20699723e+01,   9.05167501e+00,
            3.41919377e+00,   7.62306351e+00,  -1.67837954e+02,
            7.60332685e-02,   1.57176227e+00,   3.68595885e+00,
            7.40570804e+01,   4.59999348e-04,   4.06000335e-03,
            2.58892015e-08,   8.68406685e-01]];
# TVQ temporal video quality coef

    TVQcoef=[[29.13 , 0.01344,-1.283,6.724 ],
          [47.03, 0.01747, -1.823,10.7],  
          [47.03, 0.01747, -1.823,10.7]];

#VD Video Discontinuity coef
    
    Icoef = [[23.43 ,0.008574 ,-0.9253, 5.855],
             [54.71,  0.02589,-2.485,9.306 ],  
             [54.71,  0.02589,-2.485,9.306 ]];

#INP Input Quality Coef
      
    Inpcoef = [[47.97, 2.097, 0.01073, -4.567],
               [90, 1.191, 0.009775, -18.73],  
               [90, 1.191, 0.009775, -18.73]];

#choose the righ coef for the 1072 based on the class complexity
        
    if Iclss=='Low':
 
     
        I_Frame = IQ_Frame(bitrate, flr, Icoef[0]);
        I_TVQ = TVQ(bitrate, flr, TVQcoef[0]);
        I_INP = INPQ(delay, Inpcoef[0] );
        
        
    elif Iclss=='Medium':
    

        I_Frame = IQ_Frame(bitrate, flr, Icoef[1]);
        I_TVQ = TVQ(bitrate, flr, TVQcoef[1]);
        I_INP = INPQ(delay, Inpcoef[1]);
    
    elif Iclss=='High':
            

        I_Frame = IQ_Frame(bitrate, flr, Icoef[2]);
        I_TVQ = TVQ(bitrate, flr, TVQcoef[2]);
        I_INP = INPQ(delay, Inpcoef[2]);
    
    if Vclss=='Low':
 
        I_VU = VU(bitrate, framerate, coding_res,VUcoef[0]);
        I_VF = VF(bitrate, framerate, coding_res,VFcoef[0]);
        I_codn, I_tras = VQ(bitrate, coding_res, framerate, PL_UDP, 0, VQcoef[0])    
 
    elif Vclss=='Medium':
    
        I_VU = VU(bitrate, framerate, coding_res,VUcoef[1]);
        I_VF = VF(bitrate, framerate, coding_res,VFcoef[1]);
        I_codn, I_tras = VQ(bitrate, coding_res, framerate, PL_UDP, 0, VQcoef[1])
        
    elif Vclss=='High':
            
        I_VU = VU(bitrate, framerate, coding_res,VUcoef[2]);
        I_VF = VF(bitrate, framerate, coding_res,VFcoef[2]);
        I_codn, I_tras = VQ(bitrate, coding_res, framerate, PL_UDP, 0, VQcoef[2])
        
    R_QoE_1072 = 100 - 0.788*I_codn - 0.896*I_tras - 0.227*I_TVQ - 0.625*I_Frame - 0.848*I_INP;     
    print(" Quality in R-scale:",R_QoE_1072)  
    R_QoE_1072=R_QoE_1072.clip(min=0, max=78.49)
    print("Overal Quality:",MOSfromR_Value(R_QoE_1072))  
    print("Interaction Quality:",MOSfromR_Value(100-I_INP))  
   # print("Video Unclearness:", MOSfromR_Value(100-I_VU)) ;
    #print("Video Fragmentation:", MOSfromR_Value(100-I_VF)) ;
    return MOSfromR_Value(R_QoE_1072)

 
def test_para(bitrate, coding_res, packetloss, packetlossUDP, framerate, delay, Icomplexity, Vcomplexity):
    wh = coding_res.split('x');
    dim = int(wh[0])*int(wh[1]);
    FLR = FrameLR(bitrate, framerate, delay, packetloss)
    return test_model(bitrate, dim, FLR, packetlossUDP, framerate, delay, Icomplexity, Vcomplexity);


if __name__== "__main__":

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-br', '--bitrate', action='store', dest='bitrate', default=1000 ,
                    help='Specify the bitrate of video', type=float)
                    
    parser.add_argument('-re', '--coding_res', action='store', dest='coding_res', default='1920x1080' ,
                    help='Specify the coding resulotion of video')
                    
    parser.add_argument('-pl', '--packetloss', action='store', dest='packetloss', default=0,
                    help='Specify the packetloss of network in case of freezing', type=float)
                     
    parser.add_argument('-plu', '--packetlossUDP', action='store', dest='packetlossUDP', default=0 ,
                    help='Specify the packetloss of network in case of Slicing', type=float)

    parser.add_argument('-fr', '--framerate', action='store', dest='framerate', default=60 ,
                    help='Specify the framelossrate of video', type=int)
       
    parser.add_argument('-dl', '--delay', action='store', dest='delay', default=100 ,
                    help='Specify the delay of network', type=int)
    
    parser.add_argument('-Iclss', '--Icomplexity', action='store', dest='Icomplexity', default='High' ,
                    help='Specify the interaction complexity class of model, Low, Medium, High')
    
    parser.add_argument('-Vclss', '--Vcomplexity', action='store', dest='Vcomplexity', default='High' ,
                    help='Specify the video complexity class of model, Low, Medium, High')
                                     
    parser.add_argument('-vid', '--video', action='store', dest='video', default=r'CSGO_30fps_30sec_Part1_640x480_400_x264.mp4' ,
                    help='Number of Images')
    
    parser.add_argument('-t', '--test_type', action='store', dest='test_type', default='video',
                    help='Option to')
    
    values = parser.parse_args()
        
    if values.test_type == 'parameters':
            test_para(values.bitrate, values.coding_res, values.packetloss, values.packetlossUDP, values.framerate, values.delay, values.Icomplexity, values.Vcomplexity);
            
    else:
        print("No such option")