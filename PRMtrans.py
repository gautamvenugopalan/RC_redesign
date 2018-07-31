'''
Python script to figure out the optimal PRM transmission
as a function of expected arm loss
'''
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/Users/gautamvenugopalan/Documents/physics/Caltech/40m Stuff/GIT/software/labutils/python_40mutils')
import generalUtils as genUtil
from matplotlib.ticker import FormatStrFormatter
try:
	plt.style.use('gvELOG')
except:
	pass

def armRefl(Ti=1.384e-2, Te=13e-6, etai=20e-6, etae=20e-6, printInfo=False):
	'''
	Function to calculate the reflectivity of a (lossy) two mirror
	Fabry Perot cavity. Takes as input the (power) transmissivity
	and loss of the input and output couplers.
	'''
	ti = np.sqrt(Ti)
	te = np.sqrt(Te)
	ri = np.sqrt(1 - Ti - etai)
	re = np.sqrt(1 - Te - etae)
	refl = (re*(ti**2 + ri**2) - ri)/(1 - ri*re)
	if printInfo:
		print('Ri={} %, Ti={} %, Re={} %, Te={} ppm, loss_i={} ppm, loss_e={} ppm'.format(round(100*(ri**2),3),round(100*Ti,3), 
			round(100*(re**2),3), round(1e6*Te,3), 1e6*etai, 1e6*etae))
		print('Amplitude reflectivity is {}'.format(refl))
	return refl

def PRG(rarm=0.992163515534, Tp=5.5e-2, etap=200e-6,  printInfo=False):
	'''
	Function to calculate the RPG for a given arm reflectivity
	and PRM (power) transmissivity.
	'''
	tp = np.sqrt(Tp)
	rp = np.sqrt(1 - Tp - etap)
	gp = tp / (1-rp*rarm)
	if printInfo:
		print('PRG is {} for Tp= {} %, Rarm = {} %'.format(round(gp**2, 3), round(100*Tp,3), round(100*rarm**2,3)))
	return gp**2

def optTp(Ti=1.384e-2, eta=40e-6):
	'''
	Function to evaluate the (approximate) optimal PRM power transmissivity
	for a given arm loss, to achieve maximum PRG (critical coupling).
	In practise, we would choose slightly higher Tp so as to still have
	some PDH signals for locking.
	'''
	return 4*eta/Ti

loss = 1e-6*np.linspace(5,40,100)
Tp = optTp(eta=2*loss)

# Explicitly calculate the PRG as a function of Tp and arm loss
tt = 1e-2*np.linspace(0.25, 2.25,100)
ll, TT = np.meshgrid(loss,tt)
rr = armRefl(etai=ll, etae=ll)
prg = PRG(rr, TT)
# Make the plot
fig, ax = plt.subplots(1,1,figsize=(12,8))
heatmap = ax.pcolormesh(1e6*ll, 1e2*tt, prg,cmap='inferno', rasterized=True, vmin=0.9*np.min(prg), vmax=1.1*np.max(prg))
c1=fig.colorbar(heatmap, format='%2d', pad=0.01)
# Add the line of critical coupling
ax.plot(1e6*loss, 100*Tp, linestyle='--', linewidth=3, color='xkcd:bright teal', alpha=0.7)
# Add some contours
levels = [20, 40, 60, 80, 100, 120]
C1 = ax.contour(1e6*ll,1e2*TT,prg,levels,colors='k',linewidths=3)
ax.clabel(C1, colors = 'k', fmt = '%2d', fontsize = 18)
#Indicate undercoupled and overcoupled regions
ax.text(0.55, 0.8, 'Overcoupled', color='xkcd:bright teal', transform=ax.transAxes)
ax.text(0.55, 0.5, 'Undercoupled', color='xkcd:bright teal', transform=ax.transAxes)
# Formatting
ax.set_xlabel('Loss $\mathcal{L}$ per arm optic [ppm]')
ax.set_ylabel('$\mathrm{T_{PRM}}$ [\%]')
c1.set_label('PRG',rotation=270, labelpad=15)
ax.set_ylim([0.25,2.25])
fig.suptitle('PRG($\mathrm{T_{PRM}}$, $\mathcal{L}$), for 200 ppm (RT) loss in the PRC')
fig.subplots_adjust(left=0.07, right=0.99999, top=0.92)
fig.savefig('PRGmap.pdf')
