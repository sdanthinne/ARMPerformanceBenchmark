#include <stdio.h>
#include <linux/perf_event.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <stdint.h>

#define NUM_TESTS 1000000
#define SIZE_L1_CACHE 32000 //a little smaller than the actual size
#define INS_COUNT_RUN_TEST 5.0
#define RAND_SEED 1
#define USAGE_N_EXIT do{fprintf(stderr,"Usage incorrect, needs 1 arg\n");}while(0);

extern int test_load_use_chain_l1(int *, int *, int);
/**
 * Returns a pointer to the head of the array of random ints.
 *
 */
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
   return arr-size;
}


int main(int argc, char * argv[])
{
   int * rand_array = gen_rand_arr(SIZE_L1_CACHE/sizeof(int));
   if(argc!=2)
   {
      USAGE_N_EXIT
      return -1;
   }
   return test_load_use_chain_l1(rand_array,rand_array+SIZE_L1_CACHE/sizeof(int),
      atoi(argv[1])); 
   //return test_load_use(NUM_TESTS,rand_array);
}
