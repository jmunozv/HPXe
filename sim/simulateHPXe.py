#!/usr/bin/env python

import sys, os


## READING INPUT VARIABLES
pressure  = sys.argv[1]
eEnergy   = sys.argv[2]
numEvents = sys.argv[3]


## GENERAL SETTING
EXP_NAME = 'HPXe'
MIN_EDEP = 0.0

EXE_PATH   = os.environ['SW_PATH'] + '/nexus_trunk/'
ODST_PATH  = '/data4/NEXT/HPXe/sim/'
DECAY0_PATH = '/data4/NEXT/NEXTNEW/decay0/'


## OUTPUT DST FILE NAME
def get_odst_fname(pressure, eEnergy):
    fname = ODST_PATH + EXP_NAME + '.' + pressure + 'atm.e' + eEnergy + 'KeV.next'
    print "Output file name: ", fname
    return fname


## NEEDED FILES NAMES
INIT_FNAME   = 'HPXe.init.mac'
CONFIG_FNAME = 'HPXe.config.mac'



## CREATING INIT FILE
def make_init_file():

    text = '''
### GEOMETRY
/Geometry/RegisterGeometry MAG_BOX

### GENERATOR
/Generator/RegisterGenerator SINGLE_PARTICLE

### ACTIONS
/Actions/RegisterRunAction DEFAULT
/Actions/RegisterEventAction DEFAULT
/Actions/RegisterTrackingAction DEFAULT

### PHYSICS
/PhysicsList/RegisterPhysics G4EmStandardPhysics_option4
/PhysicsList/RegisterPhysics NexusPhysics
/PhysicsList/RegisterPhysics G4DecayPhysics
/PhysicsList/RegisterPhysics G4RadioactiveDecayPhysics
/PhysicsList/RegisterPhysics G4StepLimiterPhysics
#/PhysicsList/RegisterPhysics G4OpticalPhysics

### EXTRA CONFIGURATION
/nexus/RegisterMacro %s

''' %(CONFIG_FNAME)

    myfile = open(INIT_FNAME, 'w')
    myfile.write(text)
    myfile.close()

    #print "\n*** Init file content:", text



## CREATING CONFIG FILE
def make_config_file(pressure, eEnergy):
    odst_fname = get_odst_fname(pressure, eEnergy)

    text = '''
### GEOMETRY (Xenon, Hydrogen, SeF6)
/Geometry/MagBox/gas_name Xenon
/Geometry/MagBox/pressure %s bar
/Geometry/MagBox/mag_intensity 0.0 tesla
/Geometry/MagBox/max_step_size 1.0 mm

### GENERATOR
/Generator/SingleParticle/region CENTER
/Generator/SingleParticle/particle e-
/Generator/SingleParticle/min_energy %s keV
/Generator/SingleParticle/max_energy %s keV
/Generator/SingleParticle/momentum_X  0.
/Generator/SingleParticle/momentum_Y  1.
/Generator/SingleParticle/momentum_Z  0.

### ACTIONS
/Actions/DefaultEventAction/energy_threshold %.3f MeV

### PHYSICS
/PhysicsList/Nexus/clustering          false
/PhysicsList/Nexus/drift               false
/PhysicsList/Nexus/electroluminescence false


### VERBOSITIES
/run/verbose 0
/event/verbose 0
/tracking/verbose 0


### JOB CONTROL
/nexus/persistency/outputFile %s

''' %(pressure, eEnergy, eEnergy, MIN_EDEP, odst_fname)

    myfile = open(CONFIG_FNAME, 'w')
    myfile.write(text)
    myfile.close()

    #print "\n*** Configuration file content:", text



#############################################################################################
## SIMULATING

# Create parameter file
make_init_file()
make_config_file(pressure, eEnergy)

# Run the simulation
inst = EXE_PATH + 'nexus -b ' + INIT_FNAME + ' -n ' + str(numEvents) 
print "*** EXECUTING: " + inst + "  ...\n"
#raw_input("Press any key to start ...")
os.system(inst)

