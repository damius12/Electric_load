import numpy as np
import cantera as ct

gas = ct.Solution('gri30.yaml')
carbon = ct.Solution('graphite.yaml')

# Initial conditions
T = 500 + 273.15 
P = ct.one_atm

# Composition of syngas
C = 1.0
H = 1.52
O = 0.67
N = 0.01
H20 = 0.3









