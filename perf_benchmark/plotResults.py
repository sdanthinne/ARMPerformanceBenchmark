
import csv,glob
import matplotlib.pyplot as plt
import numpy as np


def makePlots(filename="results.csv"):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        rows = []

        for row in csv_reader:
            rows.append(row)
        c1 = np.array([float(row[0]) for row in rows])
        c2 = np.array([round(float(row[1])) for row in rows])
        c3 = np.array([float(row[2]) for row in rows])
        print(c2)
        plt.plot(c1,c2,'rd',label="Cycle Count vs N Iterations")
        m,b = np.polyfit(c1,c2,1)
        plt.plot(c1,m*c1+b,label=f'y={m:.6f}x+{b:.6f}')
        plt.legend()
        #plt.ylim([1,20000000000])
        plt.ylabel('Cycle Count')
        plt.xlabel('N Iterations')
        plt.title(f'{filename[:-4]}: Cycle Count vs N Iterations')
        plt.xscale('log')
        #plt.show()
        plt.savefig(f'cyc_vs_n{filename[:-4]}.png')
        plt.close()
        plt.plot(c1,c3,'rd',label="Runtime vs N Iterations")
        m,b = np.polyfit(c1,c3,1)
        plt.plot(c1,m*c1+b,label=f'y={m:.6f}x+{b:.6f}')
        plt.legend()
        plt.title(f'{filename[:-4]}: Runtime vs N Iterations')
        plt.xscale('log')
        #plt.yscale('log')
        plt.ylabel('Runtime(s)')
        plt.xlabel('N Iterations')
        plt.savefig(f'runtime_vs_n{filename[:-4]}.png')
        plt.close()

if __name__=="__main__":
    for fname in [x[2:] for x in glob.glob('./*.csv')]:
        print(fname[:-4])
        makePlots(fname)

