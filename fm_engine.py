
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import sawtooth, square


from fm_engine_elements import envelope, oscillator

class fm_engine:
    '''
    First version of a FM engine. It is hardcoding a 4 operator
    FM engine, with the following algorithms:
    [0] OP4>OP3>OP2>OP1
    '''

    def __init__(self, settings = {}, algorithm = 0):

        self.settings = {}
        self.algorithm =  0

        self.settings['op1'] = [1.0, 1.0, 'sin', 0.001, 3, 2]
        self.settings['op2'] = [1.0, 0.5, 'sin', 0.001, 1, 1]
        self.settings['op3'] = [1.0, 1.0, 'sin', 0.5, 1, 1]
        self.settings['op4'] = [0.1, 2, 'sin', 0.0001, 1, 1]

        print(self.settings['op4'])


    def return_sample(self, frequency, duration = 10, bitrate = 44800):

        '''plays a single note for a specifed duration'''

        print(duration, bitrate)
        time = np.arange(bitrate*duration)/bitrate
        sound = np.zeros(len(time))

        # print(frequency)
        # print([f*self.settings['op4'][1] for f in frequency])


        if self.algorithm == 0:
            sound = oscillator(time,
                               [f*self.settings['op4'][1] for f in frequency],
                               sound,
                               0.5,
                               self.settings['op4'][2]) *\
                    envelope(time,
                             self.settings['op4'][3],
                             0.001,
                             0.001,
                             self.settings['op4'][4],
                             self.settings['op4'][5])

            sound = oscillator(time,
                               [f*self.settings['op3'][1] for f in frequency],
                               sound*self.settings['op4'][0],
                               0.5,
                               self.settings['op3'][2]) *\
                    envelope(time,
                             self.settings['op3'][3],
                             0.001,
                             0.001,
                             self.settings['op3'][4],
                             self.settings['op3'][5])

            sound = oscillator(time,
                               [f*self.settings['op2'][1] for f in frequency],
                               sound*self.settings['op3'][0],
                               0.5,
                               self.settings['op2'][2]) *\
                    envelope(time,
                             self.settings['op2'][3],
                             0.001,
                             0.001,
                             self.settings['op2'][4],
                             self.settings['op2'][5])

            sound = oscillator(time,
                               [f*self.settings['op1'][1] for f in frequency],
                               sound*self.settings['op2'][0],
                               0.5,
                               self.settings['op1'][2]) *\
                    envelope(time,
                             self.settings['op1'][3],
                             0.001,
                             0.001,
                             self.settings['op1'][4],
                             self.settings['op1'][5])

        samples = sound.astype(np.float32)

        return samples


    def play_note(self, volume, frequency, duration = 10, bitrate = 44800):

        samples = self.return_sample(frequency, duration, bitrate)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=bitrate,
                        output=True)

        stream.write(volume*samples)
        stream.stop_stream()
        stream.close()
        p.terminate()
