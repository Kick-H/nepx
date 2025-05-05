import numpy as np


def get_dens(vol, mol_mass):
    N_A = 6.02214076e23
    nm_cm_3 = 1e-7**3            # nm to cm
    #      _________g_________   _____cm^3____
    dens = mol_mass/N_A / (vol*nm_cm_3)
    return dens     # g/nm^3


def proc_data(data, atom=None) -> dict[str, np.ndarray]:

    if data['data_type'] == "thermo":
        if atom != None:
            if 'Lx' in data:
                volumes = data['Lx']*data['Ly']*data['Lz']
            elif 'ax' in data:
                cm = np.array([
                    [data['ax'], data['ay'], data['az']],
                    [data['bx'], data['by'], data['bz']],
                    [data['cx'], data['cy'], data['cz']] ])
                cm = np.transpose(cm, (2, 0, 1))
                volumes = np.abs(np.einsum('ij,ij->i',cm[:, 0],np.cross(cm[:, 1], cm[:, 2])))
            data['Volume'] = volumes / 1000
            data['Masses'] = np.array([np.sum(atom.get_masses())] * len(data['Volume']))
            data['Density'] = get_dens(data['Volume'], data['Masses'])
        data['Total_Energy'] = data['U'] + data['K']


def mean_data(data, percent: float=[0.5, 1.0], delt_block: int=2,
              jump_line: int=0, temp_list: str=None) -> dict[str, np.ndarray]:

    for ndir in data:
        data[ndir] = data[ndir][jump_line:]

    if delt_block > 1:
        db = delt_block
        nb = round(len(data[list(data.keys())[0]])/db)

        temp_data = {}
        for i in range(nb):
            sta = i * db
            end = (i+1) * db
            if i == nb-1:
                end = len(data[list(data.keys())[0]])
            temp_data[i] = {}
            for ks in data:
                temp_data[i][ks] = data[ks][sta:end]

    out_data = dict()
    if temp_list == None:
        temp_list = temp_data[ti].keys()
    for ti in temp_data:
        out_data[ti] = {}
        for dn in temp_list:
            if dn == 'data_type': continue
            data_dn = temp_data[ti][dn]
            sta = int(len(data_dn)*percent[0])
            end = int(len(data_dn)*percent[1])
            out_data[ti][dn] = np.mean(data_dn[sta:end])
            out_data[ti][f"{dn}_std"] = np.std(data_dn[sta:end])

    return out_data
