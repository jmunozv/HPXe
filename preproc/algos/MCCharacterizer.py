from Centella.AAlgo import AAlgo
from Centella.physical_constants import *

"""
This algorithm generates different Histograms based on Montecarlo Irene Files
"""


class MCCharacterizer(AAlgo):

	############################################################
	def __init__(self, param=False, level=1, label="", **kargs):

		"""
		MC Info Characterizer Algorithm
		"""
		#self.m.log(1, 'Constructor()')

		### GENERAL STUFF
		self.name = 'MCCharacterizer'
		#self.level = level
		AAlgo.__init__(self, param, level, self.name, 0, label, kargs)

    ### PARAMETERS
		


	############################################################		
	def initialize(self):

		self.m.log(1, 'Initialize()')
		
		### Defining histos

		# Histogram of Event Edep
		histo_name = self.alabel("evtEdep")
		histo_desc = "Event Energy"
		self.m.log(2, "Booking ", histo_name)
		self.m.log(3, "   Description: ", histo_desc)
		self.hman.h1(histo_name, histo_desc, 100, 0., 3.0)
		
		# Histogram of Partt Edep
		histo_name = self.alabel("partEdep")
		histo_desc = "Particle Energy"
		self.m.log(2, "Booking ", histo_name)
		self.m.log(3, "   Description: ", histo_desc)
		self.hman.h1(histo_name, histo_desc, 50, 0., 0.5)
		
		# Histogram of Hit Edep
		histo_name = self.alabel("hitEdep")
		histo_desc = "Hit Energy"
		self.m.log(2, "Booking ", histo_name)
		self.m.log(3, "   Description: ", histo_desc)
		self.hman.h1(histo_name, histo_desc, 30, 0., 0.03)
		
		# Histogram of Number of Particles per event
		histo_name = self.alabel("numParts")
		histo_desc = "Number of Particles per Event"
		self.m.log(2, "Booking ", histo_name)
		self.m.log(3, "   Description: ", histo_desc)
		self.hman.h1(histo_name, histo_desc, 30, 0, 30)

		# Histogram of Number of Hits per Particle
		histo_name = self.alabel("numHits")
		histo_desc = "Number of Hits per Particle"
		self.m.log(2, "Booking ", histo_name)
		self.m.log(3, "   Description: ", histo_desc)
		self.hman.h1(histo_name, histo_desc, 50, 0, 50)

		return



	############################################################
	def execute(self, event=""):

		self.m.log(2, 'Execute()')		
	
		evtEdep = 0.

		iParts = self.event.GetParticles()
		self.m.log(2, 'Num Particles in the Event:', len(iParts))
		self.hman.fill(self.alabel("numParts"), len(iParts))
		
		for iPart in iParts:
			for trkIdx in range(iPart.GetTracks().GetEntriesFast()): 
				iTrack = iPart.GetTracks()[trkIdx]
				iHits = iTrack.GetHits()
				self.m.log(2, 'Num Hits in Particle', iPart.GetParticleID(), ':', len(iHits))
				self.hman.fill(self.alabel("numHits"), len(iHits))

				partEdep = 0.

				for iHit in iHits:
					hitEdep = iHit[1]
					self.m.log(3, 'Hit Energy:', hitEdep)
					self.hman.fill(self.alabel("hitEdep"), hitEdep)
					partEdep += hitEdep 
					evtEdep += hitEdep

				self.m.log(2, 'Particle', iPart.GetParticleID(), 'Energy:', partEdep)
				self.hman.fill(self.alabel("partEdep"), partEdep)


		self.m.log(2, 'Event Energy:', evtEdep)
		self.hman.fill(self.alabel("evtEdep"), evtEdep)


		return True

		

	############################################################
	def finalize(self):

		self.m.log(1, 'Finalize()')

		return
