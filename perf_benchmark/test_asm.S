.global test_load_use_chain_l1
test_load_use_chain_l1:
   /**
    * This test uses a complete dependency chain, and only iterates over the L1
    * cache size. r0 is the array location in memory, which should be less than
    * the size of the L1 cache. r1 is a dummy register, and r2 is the mar 
    * number of iterations.
    */
   //setup
   #define min_ptr r0
   #define mar_ptr r1
   #define iterations r2 //how many times over l1 cache
   #define temp_reg_1 r3
   #define min_ptr_t r4
   
test_load_use_chain_l1_loop_2:
   mov min_ptr_t, min_ptr

test_load_use_chain_l1_loop_1:
   ldr temp_reg_1,[min_ptr_t]
   neg temp_reg_1, temp_reg_1
   str temp_reg_1,[min_ptr_t]
   add min_ptr_t, min_ptr_t, #4
   cmp min_ptr_t,mar_ptr
   bne test_load_use_chain_l1_loop_1

   sub iterations, iterations, #1
   cmp iterations, #0
   bne test_load_use_chain_l1_loop_2
   bx lr

.global test_load_use
/**
 * Input: r0 is number of iterations, r1 is address of array
 * Returns: sum in r0
 */
test_load_use:
   mov r2, #4
   mul r4,r0,r2//get the number of addresses
   add r4,r4,r1//add the number of addresses to base addr
   mov r2, #0
   mov r3, #1

   test_load_use_loop:
   //load and then use
   ldr r5, [r1]
   add r3,r3,r5

   add r1,r1,#4
   cmp r1,r4
   bne test_load_use_loop
   mov r0,r3

   bx lr

/**
 * This tests the delay with an early register
 * Input: r0 is the number of iterations, r1 is address of an array
 * Returns: sum in r0
 */
test_early:
   mov r2, #4
   mul r4,r0,r2 //get # of addrs
   add r4,r4,r1//add the offset to get to the array
   mov r2, #0
   mov r3, #1
   test_early_loop:
   //early register use
   add r5,r6,r7
   str r5, [r1]

   add r1, r1, #4
   cmp r4,r1
   bne test_early_loop
   bx lr

/**
 * This tests the delay with a load use hazard and use of an early register
 * Input: r0 is the number of iterations, r1 is address of an array
 * Returns: sum in r0
 */
test_load_use_early:
   mov r2, #4
   mul r4,r0,r2 //get # of addrs
   add r4,r4,r1//add the offset to get to the array
   mov r2, #0
   mov r3, #1
   test_load_use_early_loop:
   //early register use
   add r5,r6,r7
   str r5, [r1]

   add r1, r1, #4
   cmp r4,r1
   bne test_load_use_early_loop
   bx lr
