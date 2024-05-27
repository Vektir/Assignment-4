import marsatm
import numpy as np
import matplotlib.pyplot as plt

marstable = marsatm.marsinit()
CdS = 4.92
ve = 4400
kv=.05
mzfw = 699.0
dt = 0.01
g = np.array([0,-3.71])
gamma = -20 * np.pi / 180
vinit = 260


vinit = np.array([np.cos(gamma) * vinit, np.sin(gamma) * vinit])
posinit = np.array([0, 20000])


def CalcMdot(m, vy):
	deltav = -2 - vy
	if deltav < 0:
		deltav = 0
	mdott = m*-g[1]/ve + kv * deltav
	if mdott > 5:
		return 5
	return mdott

	
def CalcThrust(mdot,v):
	return mdot * ve * -v/np.linalg.norm(v)


def CalcForce(v, h, m, mdot):
	# print(h)
	# print(marstable)
	p, rho, temp = marsatm.marsatm(h, marstable)
	drag = 0.5 * CdS * (np.linalg.norm(v)) ** 2 * rho * -v/np.linalg.norm(v)
	gravity = g * m
	thrust = CalcThrust(mdot, v)

	return drag + gravity + thrust

def CalcAccel(Force, m):
	return Force / m

def CalcVel(v, a):
	return v + a * dt

def CalcPos(h, v):
	return h + v * dt

#def FindOptThrustandmFuel():



def Update(pos, v, mfuel, thrustheight):
	
	if pos[1] > thrustheight:
		mdot=0
	else:
		mdot = CalcMdot(mfuel + mzfw, v[1])
	if mfuel < 0:
		mdot = 0

	if pos[1] < 0.3:
		mdot = 0

	force = CalcForce(v, pos[1], mfuel + mzfw, mdot )
	accel = CalcAccel(force, mfuel + mzfw)
	v_new = CalcVel(v, accel)
	pos_new = CalcPos(pos, v)


	return pos_new, v_new, mfuel-mdot * dt, mdot

def plot(positions, velocities, gammas, times, mdots):
	plt.subplot(2,3,1)
	plt.plot(positions[:,0], positions[:,1])
	plt.title("Trajectory")

	plt.subplot(2,3,2)
	plt.plot([np.linalg.norm(i) for i in velocities], positions[:,1])
	plt.title("speeds vs altitude")

	plt.subplot(2,3,3)
	plt.plot(times, mdots)
	plt.title("mdot vs time")

	plt.subplot(2,3,4)
	plt.plot(times, positions[:,1])	
	plt.title("altitude vs time")

	plt.subplot(2,3,5)
	plt.plot( times,[np.linalg.norm(i) for i in velocities])
	plt.title("speed vs time")

	plt.subplot(2,3,6)
	plt.plot(times,gammas)
	plt.title("gamma vs time")

	plt.show()

#print("mdot", CalcMdot(1000, -4))

#finalvelocities = []
# for mfuel in reversed(range(120)):
# 	for  thrustheught in reversed(range(2000)):
		

def getresults(mfuel, thrustheight):
	velocities = np.array([vinit])
	positions = np.array([posinit])
	gammas = np.array([-20])
	mdots = np.array([0])


	while positions[-1][1] > 0 and velocities[-1][1] < 0:
		pos, v, mfuel, mdot = Update(positions[-1], velocities[-1], mfuel, thrustheight)

		#if pos[1] < 0.3:
		#	finalvelocities.append(v)

		mdots = np.append(mdots, [mdot], axis=0)
		positions = np.append(positions, [pos], axis=0)
		velocities = np.append(velocities, [v], axis=0)
		gammas = np.append(gammas, [np.arctan(v[1]/v[0])*180/np.pi], axis=0)
	times = np.arange(0, (len(positions)-.5) * dt, dt)
	return positions, velocities, gammas, times, mdots

def FindOptHeightandMass():
	lastheight = 1738
	optheight = 0
	optmass = 0
	counts = False
	counter=0
	for fmass in reversed(range(66)):
		#print(fmass)
		counter = 0
		counts = False
		for thrustheight in reversed(range(lastheight)):
			#print(thrustheight)
			
			positions, velocities, gammas, times, mdots = getresults(fmass, thrustheight)
			if abs(velocities[-1][1]) < 3:
				counts = True
				counter+=1
			if abs(velocities[-1][1]) > 3:
				if counts:
					optheight = thrustheight+1
				
				lastheight = optheight
				break
		if counts:
			optmass=fmass
		if counter == 0:
			break
	return optheight, optmass

#print(FindOptHeightandMass())
positions, velocities, gammas, times, mdots = getresults(64, 1731)


#positions2, velocities2, gammas2, times2, mdots2 = getresults(120, 2000)
#print(np.linalg.norm(finalvelocities[1]))
#print(velocities[-50:-1])
# print(velocities[-1])
# print(velocities[0])

#print(len(positions), len(velocities), len(gammas), len(times), len(mdots))
# print("gammas",gammas[0])
print(velocities[-1][1])
#print(positions[-1][1])
plot(positions, velocities, gammas, times, mdots)
#print(positions[-1])
#print(velocities[-1])
#print(len(positions) - 1)