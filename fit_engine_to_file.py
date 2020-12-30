import pyaudio
import numpy as np
from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from fm_engine import fm_engine
from scipy.optimize import minimize, shgo
from audio_test import play_shit

# load wave file
a = read("sample_a.wav")

target = np.array(a[1][:int(len(a[1])/3), 0], dtype = float)
target = target/max(target)

target_bitrate = a[0]
target_length = len(target)/a[0]


test = fm_engine()
bla = test.return_sample( [220], 20)

errors = []

# define fitting function
def residuals(args, data):
    # print(np.shape(args), np.shape(data))
    # set sound parameters
    test.set_all(args[2:])
    # test.print_settings()
    # get sound
    bla = test.return_sample([args[0]], duration = target_length, bitrate = target_bitrate)

    errors.append(np.abs(bla-data)**2)

    # print(np.shape(bla), np.shape(data))
    # return difference
    return ((bla-data)**2).cumsum()[-1]

# inital guess
guess = [220, 20, 0,\
         1.0, 1.0, 0, 0.01, 0.5, 2,\
         0.2, 2.0, 0, 0.001, 0.2, 2,\
         0.1, 3.0, 0, 0.001, 0.1, 2,\
         0.05, 4.0, 0, 0.001, 0.1, 2, 0.01]

bounds = [(0, 20000), (0, 100), (0, 10),\
          (0, 1), (0, 12), (0,1), (0, 2), (0,4), (0,2),
          (0, 1), (0, 12), (0,1), (0, 2), (0,4), (0,2),
          (0, 1), (0, 12), (0,1), (0, 2), (0,4), (0,2),
          (0, 1), (0, 12), (0,1), (0, 2), (0,4), (0,2), (0,10)]


# test.set_all(guess[2:])
# test.print_settings()
# test.play_note(0.5, [guess[0]], guess[1])

test.set_all(guess[2:])
print('initial score:', residuals(guess, target))
test.print_settings()
test.play_note(0.5, [guess[0]], guess[1])
initial = test.return_sample([guess[0]], duration = target_length, bitrate = target_bitrate)

print('\n\nstart fitting...')
fit = minimize(fun = residuals, x0 = guess, args = (target), method = 'Nelder-Mead', options = {'maxiter' : 1000})
print(fit.message)
print('final score:', residuals(fit.x, target))
print(test.print_settings())

final = test.return_sample([fit.x[0]], duration = target_length, bitrate = target_bitrate)

# blub = shgo(residuals, bounds, args = ([target]))

plt.figure()
plt.subplot(3,1,1)
plt.plot(target, label = 'target')
plt.plot(initial, label = 'initial')
plt.plot(final,  label = 'fit')
plt.grid()
plt.legend()

plt.subplot(3,1,2)
plt.plot(np.abs(target - initial))
plt.subplot(3,1,3)
plt.plot(np.abs(target - final))

plt.show()

plt.figure()
plt.pcolormesh(np.array(errors))
plt.colorbar()
plt.show()


test.play_note(0.5, [fit.x[0]], fit.x[1])
play_shit(target.astype(np.float32), bitrate = target_bitrate, volume=0.1)
