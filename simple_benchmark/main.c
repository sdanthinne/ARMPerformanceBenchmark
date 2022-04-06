#include <stdio.h>

int main(int argc, char * argv[])
{
   extern simple_data_hazard_no_count(int * retval);
   int cycleCount = 0,tBegin,tEnd,i;
   //asm ( " \
   mov x3, 1; \
   msr PMCR_EL0, x3 " );
   tBegin = time(NULL);
   
   for(i=0; i<1000000; i++)
      simple_data_hazard_no_count(&cycleCount);

   tEnd = time(NULL);
   printf("time: %d\n",tEnd-tBegin);
   return 0;
}
