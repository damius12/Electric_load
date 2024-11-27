import numpy as np
import cantera as ct
import matplotlib.pyplot as plt

gas = ct.Solution('gri30.yaml')

# Initial conditions
P = ct.one_atm 
Tmin = 200 + 273.15
Tmax = 1200 + 273.15
dT = 5
T = np.arange(Tmin, Tmax +dT, dT)
CO2, H2, CO, CH4, N2, O2, H2O= 0, 0, 0, 1, 0, 1, 0
comp = f'CH4:{CH4}, H2:{H2}, O2:{O2}, N2:{N2}, CO:{CO}, H2O:{H2O}, N2:{N2}'

# Chemical species
species_of_interest = ['CO','CO2','H2','H2O']
nsp = gas.n_species
names = gas.species_names   #retrieves species involved in chemical reaction (only for curiosity)


# Equilibrium
X = np.zeros((len(T),len(species_of_interest)))
Y = np.zeros((len(T),len(species_of_interest)))
mw = np.zeros(len(T))
species_indeces = [gas.species_index(species) for species in species_of_interest]

for i, temp in enumerate(T):
    gas.TPX = temp, P, comp
    gas.equilibrate('TP')
    X[i,:] = gas.X[species_indeces]
    Y[i,:] = gas.Y[species_indeces]
    mw[i] = gas.mean_molecular_weight


# ==== PLOT ====

plt.figure(figsize=(6,7))

plt.subplot(2,1,1)
for j, species in enumerate(species_of_interest):
    plt.plot(T-273.15, X[:,j], label=species, linewidth=2)
plt.ylabel('Molar fraction X [-]')
plt.legend()

plt.subplot(2,1,2)
for j, species in enumerate(species_of_interest):
    plt.plot(T-273.15, Y[:,j], label=species, linewidth=2)
plt.xlabel('Temperature T [°C]')
plt.ylabel('Mass fraction Y [-]')
plt.legend()

plt.show()