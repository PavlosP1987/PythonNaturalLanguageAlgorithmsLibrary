import numpy as np
from numpy.fft import fft, ifft, ifftshift

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_pdf import PdfPages
plt.rcParams.update({'font.size': 6})

def gen_son(length):
	"Δημιουργήστε ένα συνθετικό πρότυπο «ηχητικό συμβάν» που δεν αντηχεί"
	# (whitenoise -> integrate -> φάκελος -> κανονικοποίηση)
	son = np.cumsum(np.random.randn(length))
	# εφαρμόστε φάκελο
	attacklen = length / 8
	env = np.hstack((np.linspace(0.1, 1, attacklen), np.linspace(1, 0.1, length - attacklen)))
	son *= env
	son /= np.sqrt(np.sum(son * son))
	return son

def gen_ir(length):
	"Δημιουργήστε μια συνθετική απόκριση ώθησης"
	# Αρχικά δημιουργούμε μια ήσυχη ουρά
	son = np.random.randn(length)
	attacklen = length / 2
	env = np.hstack((np.linspace(0.1, 1, attacklen), np.linspace(1, 0.1, length - attacklen)))
	son *= env
	son *= 0.05
	# Εδώ προσθέτουμε το "άμεσο" σήμα
	son[0] = 1
	# Τώρα μερικές πρώιμες κορυφές αντανάκλασης
	for _ in range(10):
		son[ int(length * (np.random.rand()**2))  ] += np.random.randn() * 0.5
	# Κανονικοποιήστε και επιστρέψτε
	son /= np.sqrt(np.sum(son * son))
	return son

def wiener_deconvolution(signal, kernel, lambd):
	"το lambd είναι το SNR"
	kernel = np.hstack((kernel, np.zeros(len(signal) - len(kernel)))) # zero pad the kernel to same length
	H = fft(kernel)
	deconvolved = np.real(ifft(fft(signal)*np.conj(H)/(H*np.conj(H) + lambd**2)))
	return deconvolved

if __name__ == '__main__':
	"απλή δοκιμή: πάρτε έναν ήχο και μία παλμική απάντηση, περιπλέξτε τους, αποσυμπιέστε τους και ελέγξτε το αποτέλεσμα (σχεδιάστε το!)"
	son = gen_son(sonlen)
	ir  = gen_ir(irlen)
	obs = np.convolve(son, ir, mode='full')
	
	obs += np.random.randn(*obs.shape) * lambd_est
	son_est = wiener_deconvolution(obs, ir,  lambd=lambd_est)[:sonlen]
	ir_est  = wiener_deconvolution(obs, son, lambd=lambd_est)[:irlen]
	
	son_err = np.sqrt(np.mean((son - son_est) ** 2))
	ir_err  = np.sqrt(np.mean((ir  -  ir_est) ** 2))
	print("single_example_test(): RMS errors son %g, IR %g" % (son_err, ir_err))
	
	pdf = PdfPages('wiener_deconvolution_example.pdf')
	plt.figure(frameon=False)
	
	plt.subplot(3,2,1)
	plt.plot(son)
	plt.title("son")
	plt.subplot(3,2,3)
	plt.plot(son_est)
	plt.title("son_est")
	plt.subplot(3,2,2)
	plt.plot(ir)
	plt.title("ir")
	plt.subplot(3,2,4)
	plt.plot(ir_est)
	plt.title("ir_est")
	plt.subplot(3,1,3)
	plt.plot(obs)
	plt.title("obs")
	pdf.savefig()
	plt.close()
	pdf.close()
