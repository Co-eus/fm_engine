import pyaudio
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from fm_engine import fm_engine

# load wave file
# wf = wave.open('sample_a.wav', 'rb')

a = read("sample_a.wav")
target = np.array(a[1], dtype = float)


test = fm_engine()
bla = test.return_sample( [220], 20)


# target = np.frombuffer(data, dtype=np.int16)

plt.figure()
plt.subplot(2,1,1)
plt.plot(target)

plt.subplot(2,1,2)
plt.plot(bla)

plt.show()
