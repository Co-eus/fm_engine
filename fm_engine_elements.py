import pyaudio
import numpy as np
from scipy.signal import sawtooth, square


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


def filter_lp2(cutoff, t, wave, sample_rate = 44800):
    '''
    a 2nd order low pass filter
    without resonance
    '''
    freqs = fftfreq(len(t), 1.0/sample_rate)
