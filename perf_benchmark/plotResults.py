
import csv
import matplotlib.pyplot as plt

filename = "results.csv"

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file,delimiter=',')
    rows = []

    for row in csv_reader:
        rows.append(row)
    c1 = [row[0] for row in rows]
    c2 = [round(float(row[1])) for row in rows]
    c3 = [float(row[2]) for row in rows]
    print(c2)
    plt.plot(c1,c2,label="Cycle Count vs N Iterations")
    plt.ylabel('Cycle Count')
    plt.xlabel('N Iterations')

    plt.yscale('log')
    plt.ylim([1,1000000000])
    #plt.show()
    plt.savefig('cyc_vs_n.png')
    plt.close()
    plt.plot(c1,c3,label="Runtime vs N Iterations")
    plt.yscale('log')
    plt.ylabel('Runtime')
    plt.xlabel('N Iterations')
    plt.savefig('runtime_vs_n.png')
    plt.close()


