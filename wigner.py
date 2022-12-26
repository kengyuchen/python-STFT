import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
def expi(x):
	return np.exp(2j * pi * x)

def Wigner(x, T, F):
	dt = T[1] - T[0]
	df = F[1] - F[0]
	N = int((1/dt) * (1/df))
	f_offset = int(F[0] // df)
	X = np.zeros((len(T), len(F)), dtype = 'D')
	for n in range(len(T)):
		Q = min(n, (len(T) - n))
		c1 = [x((n+q-Q)*dt + T[0]) * x((n-q+Q)*dt + T[0]) for q in range(0, 2*Q+1)]
		c1 = np.concatenate((c1, np.zeros(N - 2*Q - 1)))
		C1 = np.fft.fft(c1)
		for m in range(len(F)):
			X[n, m] = 2 * dt * expi((m*df + f_offset) * Q / N) * C1[(m + f_offset) % N]
	return X

def show_image(X, extent = None, C = 500):
	X = X.transpose()
	X = np.abs(X) / np.max(np.abs(X)) * C
	fig = plt.figure(constrained_layout = True)
	if extent:
		plt.imshow(X, cmap='gray', origin='lower', extent = extent)
	else:
		plt.imshow(X, cmap='gray', origin='lower')
	plt.xlabel('Time (Sec)')
	plt.ylabel('Frequency (Hz)')
	plt.show()

if __name__ == '__main__':
	def x(t):
		return np.cos(2 * pi * t)
	dt, df = 0.05, 0.01
	T = np.arange(0, 30, dt)
	F = np.arange(-10, 10, df)
	X = Wigner(x, T, F)
	show_image(X, extent =  (T[0], T[-1], F[0], F[-1]))