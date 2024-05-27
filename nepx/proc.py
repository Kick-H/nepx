

def get_dens(vol, mol_mass):
    N_A = 6.02214076e23
    nm_cm_3 = 1e-7**3            # nm to cm
    #      _________g_________   _____cm^3____
    dens = mol_mass/N_A / (vol*nm_cm_3)
    return dens     # g/nm^3


def read_thermo(dirs, delt_block=1, fin='thermo.out', jump_line=100):

    data = load_thermo(filename=fin, directory=dirs)
    try:
        atom = read(f'{dirs}/model.xyz', format='extxyz')
        natoms = atom.get_global_number_of_atoms()
        data['Volume'] = data['Lx']*data['Ly']*data['Lz']/1000
        data['Masses'] = np.array([np.sum(atom.get_masses())] * len(data['Volume']))
        data['Density'] = get_dens(data['Volume'], data['Masses'])
    except:
        print(" WARNING: The necessary information is missing to obtain physical quantities related to system quality.")
    data['Total_Energy'] = data['U'] + data['K']
    for ndir in data:
        data[ndir] = data[ndir][jump_line:]

    # display keys of the data.
    print("Keywords that can be used are printed below:")
    print(data.keys())

    db = delt_block
    nb = round(len(data['U'])/db)

    out_data = {}
    for i in range(nb):
        sta = i * db
        end = (i+1) * db
        if i == nb-1:
            end = len(data['U'])
        out_data[i] = {}
        for ks in data:
            out_data[i][ks] = data[ks][sta:end]

    return out_data


def get_ave_data(data):
    out_data = dict()
    for ti in data:
        out_data[ti] = {}
        for dn in data[ti].keys():
            data_dn = data[ti][dn]
            sta = int(len(data_dn)/2)
            end = len(data_dn)
            out_data[ti][dn] = np.mean(data_dn[sta:end])
            out_data[ti][f"{dn}_std"] = np.std(data_dn[sta:end])
    return out_data
