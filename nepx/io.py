from ase.io import read
import os

def read_xyz(filename: str = "model.xyz", directory: str = None):
    fxyz = os.path.join(directory, filename)
    atom = read(fxyz)
    return atom

def output_data(ave_data, plist=['temperature'], out_data=True):
    plot_data = {'num':[]}
    for i, pi in enumerate(plist):
        plot_data[pi] = []
        pstd = f"{pi}_std"
        plot_data[pstd] = []
        for di in ave_data:
            plot_data[pi].append(ave_data[di][pi])
            plot_data[pstd].append(ave_data[di][pstd])
            if len(plot_data['num']) < len(plot_data[pi]):
                plot_data['num'].append(di)

    with open(out_data, 'w') as fo:
        out_str = "num"
        for pi in plist:
            pstd = f"{pi}_std"
            out_str += f" {pi} {pstd}"
        out_str += "\n"
        for i, ni in enumerate(plot_data['num']):
            out_str += f"{ni}"
            for pi in plist:
                pstd = f"{pi}_std"
                out_str += f" {round(plot_data[pi][i], 6)} {round(plot_data[pstd][i], 8)}"
            out_str += "\n"
        fo.write(out_str)
