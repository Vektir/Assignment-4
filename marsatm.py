import numpy as np


def marsinit():
	with open("marsatm.txt", "r") as f:
		lines=f.read().splitlines()
		#print(lines)
		lines=lines[2:]
		lines=[i.split() for i in lines]
		lines=np.array(lines)

		return lines.astype(np.float16)

def marsatm(h, marstable):
	R = 191.84

	if h < 0:
		print("Error in altitude")
		h=0
	if h > 80000:
		print("Error in altitude")
		h=80000
	h1 = int(h // 10000)
	h2 = int(h1 + 1)

	k = (h-h1*10000)/(h2*10000-h1*10000)

	temp = (1-k)*marstable[h1, 1] + k*marstable[h2, 1]

	rho = (1-k)*marstable[h1, 2] + k*marstable[h2, 2]

	p = rho*temp*R


	return p, rho, temp

#print(marsatm(20000,marsinit()))
#p,rho,temp=marsatm(20000,marsinit())
#print(p)
#print(marsatm(20000,marsinit()))