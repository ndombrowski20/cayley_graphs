import numpy as np
import matplotlib.pyplot as plt
import simpleaudio as sa

F = lambda x: np.sin(2*np.pi*(1/8192)*x)

a = list(range(8192))
b = list(range(8192))

c = list(map(F, a))

print(c)

# playobj = sa.play_buffer(c, 2, 2, 44100)

# playobj.wait_done()

plt.figure()
plt.plot(a, c)
plt.show()