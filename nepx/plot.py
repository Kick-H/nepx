import matplotlib
import matplotlib.pyplot as plt
import os
import re
from typing import List, Dict, Union, Any
import numpy as np

#plt.rcParams = {"axes.linewidth": 3, "xtick.major.width": 3, "ytick.major.width": 3,
#                       "axes.labelsize": 16.0, "xtick.labelsize": 16.0, "ytick.labelsize": 16.0,
#                       "legend.fontsize": 16.0}

class Plot_File():

    # nep support filename list:
    # refer from: https://gpumd.org/nep/index.html [Output files]

    nepx_support_filename_list = ["loss.out","nep.txt","nep.restart",
            "energy_.*.out","force_.*.out","virial_.*.out","stress_.*.out",
            "dipole_.*.out","polarizability_.*.out"]
    nepx_support_plottype_list = ["loss","neptxt","neprestart",
            "energy","force","virial","stress",
            "dipole","polarizability"]
    nepx_support_plotfunction_list = {"loss":"plot_loss",
            "neptxt":"plot_neptxt",
            "neprestart":"plot_neprestart",
            "energy":"plot_out",
            "force":"plot_out",
            "virial":"plot_out",
            "stress":"plot_out",
            "dipole":"plot_dipole",
            "polarizability":"plot_polarizability"}

    def __init__(self, filename: str="", directory: str=".", plottype: str=None):

        self.filename = filename
        self.directory = directory

        if os.path.exists(os.path.join(directory, filename)):
            self.relative_path = os.path.join(directory, filename)
            self.absolute_path = os.path.abspath(self.relative_path)
            self.filepath = self.relative_path
        else:
            raise FileNotFoundError

        if plottype is None:
            self.plottype = None
            for ni, nepx_support_filename in enumerate(self.nepx_support_filename_list):
                if re.match(nepx_support_filename, filename):
                    self.plottype = self.nepx_support_plottype_list[ni]
        else:
            self.plottype = plottype

    def get_absolute_path(self):
        return self.absolute_path

    def get_relative_path(self):
        return self.relative_path

    def get_filename(self):
        return self.filename

    def get_directory(self):
        return self.directory

    def get_plottype(self):
        return self.plottype

    @staticmethod
    def plot_neptxt(self, **kwargs):
        try: kwargs.get('label')
        except: kwargs['label'] = "neptxt"
        try: kwargs.get('pngpath')
        except: kwargs['pngpath'] = "neptxt.png"
        nep = np.loadtxt(self.filepath, skiprows=6)
        plt.figure(figsize=(9,3))
        plt.subplot(1,2,1)
        plt.hist(np.log(np.abs(nep)), bins=50, label=kwargs.get("label"))
        plt.subplot(1,2,2)
        plt.scatter(range(len(nep)), nep, s=0.5)
        plt.savefig(kwargs.get("pngpath"), dpi=300)

    @staticmethod
    def plot_neprestart(self, **kwargs):
        try: kwargs.get('label')
        except: kwargs['label'] = "neprestart"
        try: kwargs.get('pngpath')
        except: kwargs['pngpath'] = "restart.png"
        restart = np.loadtxt(self.filepath, skiprows=6)
        norm_rs = np.linalg.norm(restart, axis=0)
        plt.figure(figsize=(9,8))
        plt.subplot(2,2,1)
        plt.hist(np.log(np.abs(restart[:,0])), bins=50, label=f"{kwargs.get('label')} norm={norm_rs[0]:3.3f}")
        plt.legend()
        plt.subplot(2,2,2)
        plt.scatter(range(len(restart[:,0])), restart[:,0], s=0.5, label=f"{kwargs.get('label')} norm={norm_rs[0]:3.3f}")
        plt.legend()
        plt.subplot(2,2,3)
        plt.hist(np.log(np.abs(restart[:,1])), bins=50, label=f"{kwargs.get('label')} norm={norm_rs[0]:3.3f}")
        plt.legend()
        plt.subplot(2,2,4)
        plt.scatter(range(len(restart[:,1])), restart[:,1], s=0.5, label=f"{kwargs.get('label')} norm={norm_rs[1]:3.3f}")
        plt.legend()
        plt.savefig(kwargs.get("pngpath"), dpi=300)

    @staticmethod
    def plot_loss(self, **kwargs):
        try: kwargs.get('label')
        except: kwargs['label'] = "loss"
        try: kwargs.get('test')
        except: kwargs['test'] = False
        try: kwargs.get('use_cloumn')
        except: kwargs['use_cloumn'] = None
        try: kwargs.get('ls')
        except: kwargs['ls'] = "-"
        loss_title = "gen total l1 l2 e_train f_train v_train e_test f_test v_test".split(' ')
        loss = np.loadtxt(self.filepath)
        loss[:,0] = np.arange(1, len(loss)+1)
        if kwargs.get('use_cloumn') == None:
            for i in range(1, 7):
                plt.loglog(loss[:, 0], loss[:, i], ls=kwargs.get('ls'), lw=3, label=f"{loss_title[i]} ({kwargs.get('label')})")
            if kwargs.get('test'):
                for i in range(7, 10):
                    plt.loglog(loss[:, 0], loss[:, i], ls=kwargs.get('ls'), lw=3, label=f"{loss_title[i]} ({kwargs.get('label')})")
        else:
            for i in kwargs.get('use_cloumn'):
                plt.loglog(loss[:, 0], loss[:, i], ls=kwargs.get('ls'), lw=3, label=f"{loss_title[i]} ({kwargs.get('label')})")
        plt.xlabel('Generation/100')
        plt.ylabel(f"Loss")
        plt.legend(loc="lower left", ncol=2, fontsize=14, frameon=False, columnspacing=0.2)

    @staticmethod
    def find_units(name):
        if name == "force": return ['eV/A/atom', 'meV/A/atom', 4]
        elif name == "energy": return ['eV/atom', 'meV/atom', 3]
        elif name == "virial": return ['eV/atom', 'meV/atom', 5]
        elif name == "stress": return ['GPa', 'MPa', 6]

    @staticmethod
    def plot_out(self, **kwargs):
        try: kwargs.get('label')
        except: kwargs['label'] = "out"
        data = np.loadtxt(self.filepath)
        nclo = int(data.shape[1]/2)
        targe = data[:, :nclo].reshape(-1)
        predi = data[:, nclo:].reshape(-1)
        pids = np.abs(targe - predi) < 10
        if np.sum(pids) != len(targe):
            print(f"WARNING: There are {len(targe)-np.sum(pids)} frams mismatch in {title[0]} {title[1]}")
        targe = targe[pids]
        predi = predi[pids]
        units = self.find_units(self.plottype)

        data_min = np.min([np.min(targe),np.min(predi)])
        data_max = np.max([np.max(targe),np.max(predi)])
        data_min -= (data_max-data_min)*0.1
        data_max += (data_max-data_min)*0.1
        RMSE = np.sqrt(((predi - targe) ** 2).mean())
        plt.plot([data_min, data_max], [data_min, data_max], c="grey", lw=2,
                 label=f"{kwargs.get('label')}-{self.plottype} RMSE:{1000*RMSE:.4f} {units[1]}")
        plt.xlim([data_min, data_max])
        plt.ylim([data_min, data_max])
        color = f"C{units[2]}"
        plt.plot(targe, predi, '.', color=color, ms=5)
        plt.xlabel(f'DFT {self.plottype} ({units[0]})')
        plt.ylabel(f'NEP {self.plottype} ({units[0]})')
        if kwargs.get('print_rmse'):
            print(" >>", self.plottype, f'{1000*RMSE:.4f}', units[1])

    def plot(self, pngname: str="out.png", directory: str=".", label: str="", use_cloumn: List=None, ls: str="-"):

        if self.plottype is None:
            raise "Please specify a plottype for your plotfile."

        plottype = self.plottype
        # print("Plot_File." + Plot_File.nepx_support_plotfunction_list[plottype])
        # print(label, os.path.join(directory, pngname))
        eval("self." + Plot_File.nepx_support_plotfunction_list[plottype])(
            self, label=label, pngpath=os.path.join(directory, pngname), use_cloumn=use_cloumn, ls=ls)
        # pngpath = os.path.join(directory, pngname)


if __name__ == "__main__":

    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="train", use_cloumn=[4,5], ls="-")
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="test", use_cloumn=[7,8], ls="--")
    plt.savefig("compare-loss.png", dpi=300)

    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("nep.restart", "../test/openlam-nep4")
    nepxplot.plot(pngname="restart.png", label="restart")

    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("nep.txt", "../test/openlam-nep4")
    nepxplot.plot("txt.png", label="txt")

    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="loss")
    plt.savefig("loss.png", dpi=300)

    plt.figure(figsize=(9,8))
    plt.subplot(2,2,1)
    nepxplot = Plot_File("energy_train.out", "../test/openlam-nep4")
    nepxplot.plot(label="loss")
    plt.subplot(2,2,2)
    nepxplot = Plot_File("force_train.out", "../test/openlam-nep4")
    nepxplot.plot(label="loss")
    plt.subplot(2,2,3)
    nepxplot = Plot_File("virial_train.out", "../test/openlam-nep4")
    nepxplot.plot(label="loss")
    plt.subplot(2,2,4)
    nepxplot = Plot_File("stress_train.out", "../test/openlam-nep4")
    nepxplot.plot(label="loss")
    plt.tight_layout()
    plt.savefig("train.png", dpi=300)
