#!/home/sdanthin/bin/python3
import sys
from subprocess import PIPE, run

exec_name = "testNoSyscall"
gprof = 1

def compile(exec_name, gprof_flag=0):
   output = run(f'make {exec_name} {"GPROF=1" if gprof_flag else ""}', capture_output=True, shell=True, text=True)
   print(f'Compiler output: \n {output.stdout}\n err:\n{output.stderr}')
   return output.returncode

def run_collect_print_perf(iterations):
   print(f'beginning test using {exec_name} with {sys.argv[1]} iterations\n')
   cpis = []
   cycles = []
   l1_loop_total = 100000
   for i in range(iterations):
      output = run(f'perf stat -d ./{exec_name} {l1_loop_total}', capture_output=True, shell=True, text=True)
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

def process_gprof():
   output = run(f'gprof {exec_name} gmon.out', capture_output=True, shell=True, text=True)
   print(output.stdout)

def main():
   if compile(exec_name,gprof) != 0:
      exit(-1)

   iterations = 1 if not sys.argv[1] else int(sys.argv[1])
   run_collect_print_perf(iterations)

   if gprof:
      process_gprof()

         
if __name__=="__main__":
   main()
