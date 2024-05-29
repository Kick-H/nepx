import os
import sys

# def proc_data(data, atom=None) -> dict[str, np.ndarray]:
def get_nepin_from_neptxt(neptxt: str="nep.txt", dirtxt: str=".",
    nepin: str="nep.in", dirin: str=".", rwmodel: bool=False) -> bool:

    ftxt = os.path.join(dirtxt, neptxt)
    fin = os.path.join(dirin, nepin)

    if os.path.exists(fin) and not rwmodel:
        print(f"Errors: {fin} is exist.")
        print(f"        If you are sure to overwrite, please enable forced read-write mode:")
        print(f"        'rwmodel=True'")
        return False
    else:
        # ["nep", "zbl","cutoff","n_max","basis_size","l_max","ANN"   ]
        # ["type","zbl","cutoff","n_max","basis_size","l_max","neuron"]
        with open(ftxt, "r") as fi, open(fin, "w") as fo:
            flines = fi.readlines()
            outstr = ""
            for i in range(20):  # 20 is a enough large number.
                line = flines[i]
                if str.isdigit(line): continue
                sl = line.split(" ")
                if 'nep' in line:
                    if 'zbl' in line:
                        outstr += f"version {line[3]}" + "\n"
                        outstr += "type " + line[9:]
                    else:
                        outstr += f"version {line[3]}" + "\n"
                        outstr += "type " + line[5:]
                if 'zbl' in line:
                    outstr += f"zbl {sl[2]}\n"
                if 'cutoff' in line:
                    outstr += f"cutoff {sl[1]} {sl[2]}\n"
                if 'n_max' in line:
                    outstr += f"n_max {sl[1]} {sl[2]}\n"
                if 'basis_size' in line:
                    outstr += f"basis_size {sl[1]} {sl[2]}\n"
                if 'l_max' in line:
                    outstr += f"l_max {sl[1]} {sl[2]} {sl[3]}\n"
                if 'ANN' in line:
                    outstr += f"neuron {sl[1]}\n"
            outstr += "prediction 1\n"
            fo.write(outstr)
            fo.close()
            return True


if __name__ == "__main__":
    get_nepin_from_neptxt(neptxt="nep.txt", dirtxt="../",
    nepin="nep.in", dirin=".", rwmodel=True)

