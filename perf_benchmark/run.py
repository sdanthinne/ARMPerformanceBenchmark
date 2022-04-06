#!/home/sdanthin/bin/python3
import sys
from subprocess import PIPE, run

def main():
   if len(sys.argv)==2:
      print(f'beginning test using testNoSyscall with {sys.argv[1]}\n')
      iterations = int(sys.argv[1])
      cpis = []
      cycles = []
      l1_loop_total = 100000
      for i in range(iterations):
         output = run(f'perf stat -d ./testNoSyscall {l1_loop_total}', capture_output=True, shell=True, text=True)
         output_str = output.stderr
         out_arr = output_str.split('\n')
         cycle = int(out_arr[7].split()[0].replace(',',''))
         instr = int(out_arr[8].split()[0].replace(',',''))
         cycles.append(cycle)
         cpis.append(cycle/instr)
         #print(f'Cycles per ins: {cycles/instr}')
      avg_cpi = sum(cpis)/len(cpis)
      avg_cycle = sum(cycles)/len(cycles)
      
      print(f'average CPI over {len(cpis)} samples is {avg_cpi}\n');
         
if __name__=="__main__":
   main()
