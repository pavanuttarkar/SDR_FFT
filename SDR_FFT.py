import numpy as np
from matplotlib.pyplot import *
from os.path import getsize
from scipy import fftpack





class SDR:
    def __init__(self, path, NFFT, avg):
        self.file_name = path
        self.NFFT      = NFFT
        self.avg       = avg         
    def SDR_FFT(self):
        '''
            Module to plot Dynamic spectrum of the SDR acquired IQ dataset,
            Data structure of file : I(1 byte), Q (1 byte), ...
        
            Input:  file_name
            Output: Dynamic numpy array spectrum
        '''
        siz            =       getsize(self.file_name)/(self.NFFT*2)
        print(siz)
        dt                      =       np.dtype([('I', '>i1'), ('Q', '>i1'), ])
        #dt                     =       np.dtype([('data', '>i1', int(siz))])
        comf                    =       np.memmap(self.file_name,  dtype = dt, mode = 'c')
        comf1   =       np.memmap.copy(comf)
        IQ      =       comf1['I']-127.4+1j*comf1['Q']-127.4
        IQ                      =       IQ[0:(len(IQ)-1*len(IQ)%(self.NFFT*2))]
        IQr                     =       IQ.reshape(int(len(IQ)/self.NFFT), self.NFFT)
        IQf                     =       np.transpose(fftpack.fft(IQr, axis =1))

        return (IQf*np.conj(IQf)).real

    def avg_SDR(self, spec):
       """
       """
       spec2 = []
       for i in range(len(spec[0])//self.avg-1):
           spec2.append(np.mean(spec[:,i*self.avg:(i+1)*self.avg], axis=1))
       spec2=np.array(spec2).T
       return np.roll(spec2, self.NFFT//2, axis=0)




def main():
    import argparse

    parser = argparse.ArgumentParser(description='SDR acq')
    parser.add_argument('-N',
                        '--NFFT',
                        type=int,
                        help='NFFT',
                        required=True)

    parser.add_argument('-p',
                        '--path',
                        type=str,
                        help='path of file',
                        required=True)


    parser.add_argument('-a',
                        '--avg', 
                        type=int,
                        help='avgerage - (resolution - NFFT*avg)', 
                        required=True)

    parser.add_argument('-o',
                        '--out_file',
                        type=str,
                        help='saving figure filename', 
                        default='out.pdf')
    
    parser.add_argument('-of',
                        '--out_file_npy',     
                        help='saving figure npy format',                    
                        default='out')

    args = parser.parse_args()
    SDR_obj =   SDR(
                    path=args.path,
                    NFFT=args.NFFT,
                    avg=args.avg
                    )
    spec    = SDR_obj.SDR_FFT()
    spec_avg= SDR_obj.avg_SDR(spec)
    spec_avg[0] =   0

    figure()
    imshow(spec_avg, origin='lower',cmap='viridis', aspect = 'auto')
    xlabel('Time / NFFT*avg*1/BW')
    ylabel('Channel / N')
    savefig(args.out_file)

    np.save(f"{args.out_file_npy}_SDR", spec_avg)

if __name__ == "__main__":
    main()
