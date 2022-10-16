 class SDR:
     def __init__(self, path, NFFT):
         self.file_name = path
         self.NFFT      = NFFT
         
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
 
     def avg_SDR(self):
        """
        """
        spec2 = []
        for i in range(len(spec[0])/self.avg-1):
            spec2.append(np.mean(spec1[:,i*self.avg:(i+1)*self.avg], axis=1))
        spec2=array(spec2).T
        return roll(spec2, self.NFFT//2, axis=0)
      
      
def main():
  import argparse
