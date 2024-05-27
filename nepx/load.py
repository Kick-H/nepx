import os
import numpy as np

def load_thermo(filename: str="thermo.out", directory: str="") -> dict[str, np.ndarray]:
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
    labels = ['temperature', 'K', 'U', 'Px', 'Py', 'Pz']

    if data.shape[1] == 9:  # orthogonal < 3.3.1
        labels += ['Lx', 'Ly', 'Lz']
    elif data.shape[1] == 12:  # orthogonal < 3.3.1
        labels += ['Pyz', 'Pxz', 'Pxy', 'Lx', 'Ly', 'Lz']
    elif data.shape[1] == 15:  # triclinic >= 3.3.1
        labels += ['ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
    elif data.shape[1] == 18:  # triclinic >= 3.3.1
        labels += ['Pyz', 'Pxz', 'Pxy', 'ax', 'ay', 'az', 'bx', 'by', 'bz', 'cx', 'cy', 'cz']
    else:
        raise ValueError(f"The file {filename} is not a valid thermo.out file.")
    out_data = dict()
    for i in range(data.shape[1]):
        out_data[labels[i]] = data[:,i]

    out_data['data_type'] = "thermo"
    return out_data
