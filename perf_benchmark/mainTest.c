#include <stdio.h>
#include <linux/perf_event.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <stdint.h>

#define NUM_TESTS 1000000
#define INS_COUNT_RUN_TEST 5.0
#define RAND_SEED 1

long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
   int cpu, int group_fd, unsigned long flags)
{
   int ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
   return ret;
}
typedef struct read_format {
   uint64_t value;
   uint64_t time_enabled;
   uint64_t time_running;
   uint64_t id;
}read_format;

int * gen_rand_arr(int size)
{
   int * arr = malloc(size*sizeof(int));
   if(arr == NULL)
   {
      fprintf(stderr, "err with malloc\n");
      return NULL;
   }
   int i;
   srand(RAND_SEED);
   for(i=0;i<size;i++)
   {
      *arr = rand();
      arr++;
   }
   return arr;
}


int main(int argc, char * argv[])
{
   struct perf_event_attr attr;
   attr.type = PERF_TYPE_HARDWARE;
   attr.size = sizeof(struct perf_event_attr);
   attr.config = PERF_COUNT_HW_CPU_CYCLES;
   attr.read_format = PERF_FORMAT_TOTAL_TIME_RUNNING;
   attr.disabled = 1;
   attr.exclude_kernel = 1;
   attr.exclude_hv = 1;

   int * rand_array = gen_rand_arr(NUM_TESTS);

   int fd_cpu_cycles = perf_event_open(&attr,0,-1,-1,0);
   attr.config = PERF_COUNT_HW_INSTRUCTIONS;
   int fd_instructions = perf_event_open(&attr,0,-1,-1,0);

   read_format format_cpu_cycles;
   read_format format_instructions;
   int value = 10;
   //call perf start
   ioctl(fd_cpu_cycles, PERF_EVENT_IOC_RESET,0);
   ioctl(fd_instructions, PERF_EVENT_IOC_RESET,0);
   ioctl(fd_cpu_cycles, PERF_EVENT_IOC_ENABLE, 0);
   ioctl(fd_instructions, PERF_EVENT_IOC_ENABLE, 0);
   test_load_use(NUM_TESTS,rand_array);
   ioctl(fd_instructions, PERF_EVENT_IOC_DISABLE,0);
   ioctl(fd_cpu_cycles, PERF_EVENT_IOC_DISABLE,0);
   read(fd_instructions, &format_instructions,sizeof(read_format));
   read(fd_cpu_cycles, &format_cpu_cycles,sizeof(read_format));
   //call perf end and print results
   printf("Results:\n\tTime: %llu\n\tCycles: %llu\n\tInstructions: %llu\n\t\
      IPC: %f\n",format_instructions.time_running,
      format_cpu_cycles.value,
      format_instructions.value,
      format_instructions.value/format_cpu_cycles.value
      );



   return 0;
}
