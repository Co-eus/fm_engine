
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
            output += sawtooth(2*np.pi*freq*t + phase)
        elif type == 'saw2':
            output += sawtooth(2*np.pi*freq*t + phase, 0)
        elif type == 'tri':
            output += sawtooth(2*np.pi*freq*t + phase, 0.5)
        elif type == 'square':
            output += square(2*np.pi*freq*t + phase, mod)
        else:
            output += np.sin(2*np.pi*freq*t + phase)

    return output

# some settings
f = 440.0        # sine frequency, Hz, may be float
duration = 10.0   # in seconds, may be float
bitrate = 44800       # sampling rate, Hz, must be integer

# generate samples, note conversion to float32 array
# for paFloat32 sample values must be in range [-1.0, 1.0]
# sin(2*pi*f*t)
time = np.arange(bitrate*duration)/bitrate

soundf = oscillator(time, [261.63], [0], 0.5, 'sin') * envelope(time, 0.1, 0.001, 0.001, 0.5, 0.5)
sound0 = oscillator(time, [523.25], 0, 0.5, 'sin') * envelope(time, 0.1, 0.001, 0.001, 2, 0.5)
sound1 = oscillator(time, [261.63], sound0, 0.5, 'si') * envelope(time, 0.001, 0.001, 0.001, 0.5, 1)
sound2 = oscillator(time, [261.63, 311.13, 392.00], 0.9*sound0, 0.5, 'sin') * envelope(time, 0.001, 0.001, 0.001, 2, 2)


#plt.figure()
#plt.plot(sound1)
#plt.plot(sound2)
#plt.show()

'''
sound_1 = []
sound_2 = []
for t in time:
    carrier = oscillator(t, [440], [0.5*oscillator(t, [880], [0], 0.5, 'sin') *\
                                    envelope(t, 0.01, 0.001, 0.001, 2, 2)], 0.5, 'sin')
    carrier *= envelope(t, 0.0001, 0.001, 0.001, 2, 1)

    sound_1.append(carrier)

    carrier = oscillator(t, [440], [0], 0.5, 'sin')
    carrier *= envelope(t, 0.0001, 0.001, 0.001, 2, 1)

    sound_2.append(carrier)


sound_1 = np.array(sound_1)
sound_2 = np.array(sound_2)
'''

'''
# Modulator
mod = oscillator(t, [440], [0], 0.5, 'sin')
mod *= envelope(t, 0.0001, 0.001, 0.001, 0.5, 2)

# Carrier
# VCO
print('-')
carrier = oscillator(t, mod, [0], 0.5, 'sin')
# VCA + ENVELOPE
print('+')
carrier *= envelope(t, 0.0001, 0.001, 0.001, 0.5, 1)
'''

# OUTPUT

# play_shit(sound1.astype(np.float32), bitrate, volume=0.4)
play_shit(sound2.astype(np.float32), bitrate, volume=0.2)
