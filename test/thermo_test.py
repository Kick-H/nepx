import sys
sys.path.append('../nepx')
from nepx.load import load_thermo
from nepx.proc import proc_data, mean_data
from nepx.io import read_xyz

data = load_thermo(filename="thermo.out", directory="03_Carbon_thermal_transport_emd")
atom = read_xyz(filename="model.xyz", directory="03_Carbon_thermal_transport_emd")
proc_data(data, atom)
ave_data = mean_data(data, percent=[0.5, 1.0], delt_block=10000, jump_line=100, temp_list=['temperature'])

print("Keywords that can be used are printed below:")
print(data.keys())
print(ave_data)
