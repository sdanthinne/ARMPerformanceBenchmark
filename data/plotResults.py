
import csv,glob
import matplotlib.pyplot as plt
import numpy as np


def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results

def makePlots(filename="results.csv"):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        rows = []

        for row in csv_reader:
            rows.append(row)
        c1 = np.array([float(row[0]) for row in rows])
        c2 = np.array([round(float(row[1])) for row in rows])
        c3 = np.array([float(row[2]) for row in rows])
        c4 = np.array([round(float(row[3])) for row in rows])
        def plotz(c1,c2,c4,name):
            print(c2)
            fig,host = plt.subplots(figsize=(9,6))
            par1 = host.twinx()

            p1, = host.plot(c1,c2,'rd',label="Cycle Count vs N Iterations")
            res = polyfit(c1,c2,1)
            #m,b = np.polyfit(c1,c2,1)
            m = res['polynomial'][0]
            b = res['polynomial'][1]
            
            #p3, = host.plot(c1,m*c1+b,label=f'y={m:.6f}x+{b:.6f}')
            det = res['determination']
            p3, = host.plot(c1,m*c1+b,label=f'Cycle Count per Iteration Estimation: {m:.6f} $R^2$ = {det}')
            p2, = par1.plot(c1,c4,'bs',label="Instructions vs N Iterations")
        #plt.ylim([1,20000000000])
            host.legend(handles=[p1,p2,p3],loc='best')
            host.set_xlabel('N Iterations')
            par1.set_ylabel('Instructions')
            host.set_ylabel('Cycle Count')

            plt.title(f'{filename[:-4]}_{name}: Cycle Count vs N Iterations')
            #plt.xscale('log')
            #host.set_yscale('log')
            #par1.set_yscale('log')

            #plt.show()
            plt.savefig(f'cyc_vs_n{filename[:-4]}_{name}.png')
            plt.close()
        div = round(len(c1)/2)
        plotz(c1[:div],c2[:div],c4[:div],"first_half")
        plotz(c1[div:],c2[div:],c4[div:],"second_half")
        plt.figure(figsize=(9,6))
        plt.plot(c1,c3,'rd',label="Runtime vs N Iterations")
        m,b = np.polyfit(c1,c3,1)
        plt.plot(c1,m*c1+b,label=f'y={m:.6f}x+{b:.6f}')
        plt.legend()
        plt.title(f'{filename[:-4]}: Runtime vs N Iterations')
        plt.xscale('log')
        plt.yscale('log')
        plt.ylabel('Runtime(s)')
        plt.xlabel('N Iterations')
        plt.savefig(f'runtime_vs_n{filename[:-4]}.png')
        plt.close()

if __name__=="__main__":
    for fname in [x[2:] for x in glob.glob('./*.csv')]:
        print(fname[:-4])
        makePlots(fname)

