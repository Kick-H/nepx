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




class pygpumd(object):

  def __init__(self):
    self.cmd = {}
    self._enablecmd = True

  def __dir__(self):
    return sorted(set(["replicate","velocity","correct_velocity","potential","dftd3",
      "change_box","deform","ensemble","fix","time_step","run","minimize",
      "electron_stop","mc","plumed","active",
      "compute","compute_cohesive","compute_dos","compute_elastic","compute_gkma",
      "compute_hac","compute_hnema","compute_hnemd","compute_hnemdec","compute_phonon",
      "compute_rdf","compute_sdc","compute_msd","compute_shc","compute_viscosity",
      "compute_lsqt","dump_exyz","dump_beads","dump_observer","dump_dipole",
      "dump_polarizability","dump_force","dump_netcdf","dump_position",
      "dump_restart","dump_thermo","dump_velocity","dump_piston"]))

  def read_file(self, filename: str="run.in",directory: str=""):
    """
    Read GPUMD commands from a file.
    """
    self.from_file(os.path.join(directory, filename))

  def norm_cmd_str2dict(self, lc):
    self.cmd[lc[0]] = lc[1:]

  def complex_cmd_str2dict(self, lc):
    if lc[0] not in self.cmd:
      self.cmd[lc[0]] = {}
      self.cmd[lc[0]][lc[1]] = lc[2:]
    else:
      self.cmd[lc[0]][lc[1]] = lc[2:]

  def cmd_dict2str(self, k, lc):
    outstr = k
    for l in lc:
      outstr += f" {l}"
    return outstr

  def from_file(self, fname):

    # read run.in file command.
    with open(fname, 'r') as fin:

      flines = fin.readlines()
      for lines in flines:
        lins = lines.expandtabs().split()

        # jump the '#' line.
        if lins == [] or lins[0] == '' or lins[0].startswith('#') :
          continue

        lin_key = lins[0].split('_')
        if lin_key[0] in ['compute', 'dump', 'ensemble']:
          if len(lin_key) == 1:
            lin_key.append(lin_key[0])
          lin = lin_key + lins[1:]
          self.complex_cmd_str2dict(lin)
        else:
          self.norm_cmd_str2dict(lins)

  def write_file(self, filename: str="run.in",directory: str=""):
    """
    Write GPUMD script file containing all commands executed up until now
    """
    fout = open(os.path.join(directory, filename), "w")
    out_str = ""
    for cmd in self.cmd:
      if cmd in ['compute', 'dump', 'ensemble']:
        sub_cmd = list(self.cmd[cmd].keys())
        if cmd == sub_cmd[0]:
          out_str += self.cmd_dict2str(cmd, self.cmd[cmd][sub_cmd[0]])
        else:
          out_str += self.cmd_dict2str(f"{cmd}_{sub_cmd[0]}", self.cmd[cmd][sub_cmd[0]])
      else:
        out_str += self.cmd_dict2str(cmd, self.cmd[cmd])
      out_str += "\n"
    fout.write(out_str)
    fout.close()


if __name__ == "__main__":
    get_nepin_from_neptxt(neptxt="nep.txt", dirtxt="../",
    nepin="nep.in", dirin=".", rwmodel=True)

