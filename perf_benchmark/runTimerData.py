#!/home/sdanthin/bin/python3
import sys
from subprocess import PIPE, run
import csv

exec_name = "testTimer"
iterations = 1000
csv_name = "results.csv"

def run_collect_print_perf(iterations):
   f = open(csv_name,'w')
   writer = csv.writer(f)
   
   print(f'beginning test using {exec_name} with {iterations} iterations\n')
   cycles = []
   times = []
   l1_loop_total = [1,50,100,500,1000,5000,10000,50000,100000]
   for loop_total in l1_loop_total:
      for i in range(iterations):
         output = run(f'perf_4.9 stat -d ./{exec_name} {loop_total}', capture_output=True, shell=True, text=True)
         times.append(float(output.stdout))
         output_str = output.stderr
         out_arr = output_str.split('\n')
         cycle = int(out_arr[7].split()[0].replace(',',''))
         cycles.append(cycle)
      print(f'{loop_total}: Avg Cycles: {sum(cycles)/len(cycles)} Avg Time:{sum(times)/len(times)}')
      writer.writerow([loop_total,sum(cycles)/len(cycles),sum(times)/len(times)])
      
   f.close()


def main():
   run_collect_print_perf(iterations)

         
if __name__=="__main__":
   main()
