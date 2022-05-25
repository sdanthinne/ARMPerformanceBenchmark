#!/home/sdanthin/bin/python3
import sys
from subprocess import PIPE, run

exec_name = "testTimer"
iterations = 1000
perf=1
def run_collect_print_perf(iterations):
   print(f'beginning test using {exec_name} with {iterations} iterations\n')
   cycles = []
   times = []
   l1_loop_total = [1,1000]
   for loop_total in l1_loop_total:
      for i in range(iterations):
         if perf:
            output = run(f'perf stat -d ./{exec_name} {loop_total}', capture_output=True, shell=True, text=True)
            times.append(float(output.stdout))
            output_str = output.stderr
            out_arr = output_str.split('\n')
            cycle = int(out_arr[7].split()[0].replace(',',''))
            cycles.append(cycle)
         else:
            output = run(f'./{exec_name} {loop_total}', capture_output=True, shell=True, text=True)
            times.append(float(output.stdout))
            cycles.append(0)
      print(f'{loop_total}: Avg Cycles: {sum(cycles)/len(cycles)} Avg Time:{sum(times)/len(times)}')
   


def main():
   run_collect_print_perf(iterations)

         
if __name__=="__main__":
   main()
