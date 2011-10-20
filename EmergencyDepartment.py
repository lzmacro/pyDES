"""
bank08: one counter with random service time, random arrival
http://simpy.sourceforge.net/SimPyDocs/TheBank.html
"""

#from SimPy.Simulation import *
import SimPy.Simulation as Sim
import random


## Model components ##
class Source(Sim.Process):
	""" Source generates customers at random """

	def generate(self, number, meanTBA, resource):
		for i in range(number):
			p = Patients(name = "Patient%02d" % (i,))
			Sim.activate(p, p.visit(res=resource))
			t = random.expovariate(1.0/meanTBA)
			yield Sim.hold, self, t


class Patients(Sim.Process):
	""" Customer arrives is served and leaves """

	def visit(self, res):
		arrive = Sim.now() 	#arrival time
		print "%.3f: %s Arrived" % (Sim.now(), self.name)

		yield Sim.request, self, res
		wait = Sim.now()-arrive	#waiting time
		print "%.3f: %s Waited for %6.3f" % (Sim.now(), self.name, wait)

		tib = random.expovariate(1.0/timeInBank)
		yield Sim.hold, self, tib 
		yield Sim.release, self, res
		print "%.3f: %s took %.3f minutes to complete. Done." \
				% (Sim.now(), self.name, tib)


## Experiment data ##
maxNumber = 5 #max number of customers
maxTime = 400.0 #minutes
timeInBank = 12.0 #minutes
ARRint = 10.0 #mean arrival interval, minutes
theseed = 12345

## Model/Experiment ##
random.seed()
k = Sim.Resource(name="Counter", unitName="Clerk")
Sim.initialize()
s = Source(name="Source")
Sim.activate(s, s.generate(number=maxNumber, meanTBA=ARRint, resource=k), at=0.0)
Sim.simulate(until=maxTime)
