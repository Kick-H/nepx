from ase.io import read
import os
import numpy as np
import matplotlib.pyplot as plt


def load_thermo(filename: str = "thermo.out", directory: str = None) -> dict[str, np.ndarray]:
    """
    Loads data from thermo.out GPUMD output file.
    Args:
        filename: Name of thermal data file
        directory: Directory to load thermal data file from
    Returns:
        Dict containing the data from thermo.out. Units are [temperature
         -> K], [K, U -> eV], [Px, Py, Pz, Pyz, Pxz, Pxy -> GPa],
         [Lx, Ly, Lz, ax, ay, az, bx, by, bz, cx, cy, cz -> A]
    """
    thermo_path = os.path.join(directory, filename)
    data = np.loadtxt(thermo_path)
    labels = ['temperature', 'K', 'U', 'Px', 'Py', 'Pz', 'Pyz', 'Pxz', 'Pxy']
    if data.shape[1] == 12:  # orthogonal
        labels += ['Lx', 'Ly', 'Lz']
    elif data.shape[1] == 18:  # triclinic
        labels += ['ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
    else:
        raise ValueError(f"The file {filename} is not a valid thermo.out file.")

    out_data = dict()
    for i in range(data.shape[1]):
        out_data[labels[i]] = data[:,i]

    return out_data
