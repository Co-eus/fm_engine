
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq
from scipy.signal import sawtooth, square


def play_shit(samples, bitrate=44100, volume=0.5):
    '''plays shit'''
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=bitrate,
                    output=True)

    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    p.terminate()


def envelope(t, attack, decay, sustain, release, shape = 2):
    '''
    a simple envelope
    attack is time to max, release is time from max to zero

    decay/sustain are not implemented yet
    shape is the shape of the curve (linear, curved, ...)
    '''
    start_ind = 0
    max_ind = np.argmin((attack-t)**2)
    rise = np.clip((1/attack) * t, 0, 1)
    release = np.clip(-(1/release) * t + attack * (1/release),-1, 0)

    return (rise+release)**shape

def filter_lp2(cutoff, t, wave, sample_rate = 44800):
    '''
    a 2nd order low pass filter
    without resonance
    '''
    freqs = fftfreq(len(t), 1.0/sample_rate)

def oscillator(t, frequency = [440], phase = [0], mod = 0.5, type = 'sin'):

    # create silent output array
    output = np.zeros(len(t))

    # loop over frequencies and add oscillation
    # depending on chosen oscillator type
    for freq in frequency:
        if type == 'saw1' or type == 'saw':
            output += sawtooth(2*np.pi*freq*t + phase[0])
        elif type == 'saw2':
            output += sawtooth(2*np.pi*freq*t + phase[0], 0)
        elif type == 'tri':
            output += sawtooth(2*np.pi*freq*t + phase[0], 0.5)
        elif type == 'square':
            output += square(2*np.pi*freq*t + phase[0], mod)
        else:
            output += np.sin(2*np.pi*freq*t + phase[0])

    return output

# some settings
f = 440.0        # sine frequency, Hz, may be float
duration = 5.0   # in seconds, may be float
bitrate = 44800       # sampling rate, Hz, must be integer

# generate samples, note conversion to float32 array
# for paFloat32 sample values must be in range [-1.0, 1.0]
# sin(2*pi*f*t)
t = np.arange(bitrate*duration)/bitrate

# VCO
output = oscillator(t, [220], [0], 0.5, 'square')
# VCA + ENVELOPE
output *= envelope(t, 0.0001, 0.001, 0.001, 0.5, 2)
# OUTPUT

play_shit(output.astype(np.float32), bitrate, volume=0.5)
