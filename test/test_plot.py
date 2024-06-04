import sys
sys.path.append('../nepx')
from nepx.plot import Plot_File
import matplotlib.pyplot as plt

if __name__ == "__main__":


    # plot restart.png
    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("nep.restart", "../test/openlam-nep4")
    nepxplot.plot(pngname="restart.png", label="restart")


    # plot neptxt.png
    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("nep.txt", "../test/openlam-nep4")
    nepxplot.plot("txt.png", label="txt")


    # plot loss.png
    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="")
    plt.savefig("loss.png", dpi=300)


    # plot compare-loss.png
    plt.figure(figsize=(6,5))
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="train", use_cloumn=[4,5], ls="-")
    nepxplot = Plot_File("loss.out", "../test/openlam-nep4")
    nepxplot.plot(label="test", use_cloumn=[7,8], ls="--")
    plt.savefig("compare-loss.png", dpi=300)


    # plot train.png with energy, force, virial, stress
    plt.figure(figsize=(9,8))
    file_list = ["energy_train.out","force_train.out","virial_train.out","stress_train.out"]
    label_list = ["energy_train","force_train","virial_train","stress_train"]
    for i in range(4):
        plt.subplot(2,2,i+1)
        nepxplot = Plot_File(file_list[i], "../test/openlam-nep4")
        nepxplot.plot(label=label_list[i])
    plt.tight_layout()
    plt.savefig("train.png", dpi=300)


    # plot loss-train.png with loss, energy, force, virial
    plt.figure(figsize=(9,8))
    file_list = ["loss.out","energy_train.out","force_train.out","virial_train.out"] # ,"stress_train.out"]
    label_list = ["loss","energy_train","force_train","virial_train"] # ,"stress_train"]
    for i in range(4):
        plt.subplot(2,2,i+1)
        nepxplot = Plot_File(file_list[i], "../test/openlam-nep4")
        nepxplot.plot(label=label_list[i])
    plt.tight_layout()
    plt.savefig("loss-train.png", dpi=300)


    # plot train-test.png with loss, energy, force, virial
    plt.figure(figsize=(12,8))
    file_list = ["energy_train.out","force_train.out","virial_train.out"] # ,"stress_train.out"]
    label_list = ["energy_train","force_train","virial_train"] # ,"stress_train"]
    for i in range(3):
        plt.subplot(2,3,i+1)
        nepxplot = Plot_File(file_list[i], "../test/openlam-nep4")
        nepxplot.plot(label=label_list[i])
    file_list = ["energy_test.out","force_test.out","virial_test.out"] # ,"stress_test.out"]
    label_list = ["energy_test","force_test","virial_test"] # ,"stress_test"]
    for i in range(3):
        plt.subplot(2,3,i+4)
        nepxplot = Plot_File(file_list[i], "../test/openlam-nep4")
        nepxplot.plot(label=label_list[i])
    plt.tight_layout()
    plt.savefig("train-test.png", dpi=300)

