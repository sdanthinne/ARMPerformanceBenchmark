.global main
   #define min_ptr x0
   #define max_ptr x1
   #define iterations x2 //how many times over l1 cache
   #define temp_reg_1 x3
   #define min_ptr_t x4
   #define n_iterations 1
.extern malloc
main:
//stm SP!,{x4-x11,lr}
mov x0,8000
bl malloc
add x5, x0, 0
add min_ptr, x5, 0

mov temp_reg_1, 28672
add temp_reg_1, temp_reg_1, 3328

add max_ptr, x5,temp_reg_1
mov temp_reg_1, 0

mov iterations, n_iterations

bl test_load_use_chain_l1_2
b exit
.global test_load_use_chain_l1_1
test_load_use_chain_l1_1:
   /**
    * This test uses a complete dependency chain, and only iterates over the L1
    * cache size. x0 is the array location in memory, which should be less than
    * the size of the L1 cache. x1 is a dummy register, and x2 is the max 
    * number of iterations.
    * 8 cycles per 6 instructions for the PI CPI of ~1.3
    * load use of 4 for raspberry pi
    */
   
test_load_use_chain_l1_1_loop_2:
   mov min_ptr_t, min_ptr

test_load_use_chain_l1_1_loop_1:
   ldr temp_reg_1,[min_ptr_t]
   sub temp_reg_1, temp_reg_1, #1
   str temp_reg_1,[min_ptr_t]
   add min_ptr_t, min_ptr_t, #4
   cmp min_ptr_t,max_ptr
   bne test_load_use_chain_l1_1_loop_1

   sub iterations, iterations, #1
   cmp iterations, 0
   bne test_load_use_chain_l1_1_loop_2
   ret

.global test_load_use_chain_l1_2
test_load_use_chain_l1_2:
/** load, add cmp negate, str, bne
 * This test uses a different dependency chain that should lower the cpi to about 1?
 */
test_load_use_chain_l1_2_loop_2:
   mov min_ptr_t, min_ptr

test_load_use_chain_l1_2_loop_1:
   ldr temp_reg_1,[min_ptr_t]
   add min_ptr_t, min_ptr_t, #4
   cmp min_ptr_t,max_ptr
   sub temp_reg_1, temp_reg_1, 1 //does update the condition flags, and also is pseudo instruction?
   str temp_reg_1,[min_ptr_t,#-4 ]
   bne test_load_use_chain_l1_2_loop_1

   sub iterations, iterations, #1
   cmp iterations, 0
   bne test_load_use_chain_l1_2_loop_2
   b exit

.global test_load_use
/**
 * Input: x0 is number of iterations, x1 is address of array
 * Returns: sum in x0
 */
test_load_use:
   mov x2, #4
   mul x4,x0,x2//get the number of addresses
   add x4,x4,x1//add the number of addresses to base addr
   mov x2, #0
   mov x3, #1

   test_load_use_loop:
   //load and then use
   ldr x5, [x1]
   add x3,x3,x5

   add x1,x1,#4
   cmp x1,x4
   bne test_load_use_loop
   mov x0,x3

   ret

/**
 * This tests the delay with an early register
 * Input: x0 is the number of iterations, x1 is address of an array
 * Returns: sum in x0
 */
test_early:
   mov x2, #4
   mul x4,x0,x2 //get # of addrs
   add x4,x4,x1//add the offset to get to the array
   mov x2, #0
   mov x3, #1
   test_early_loop:
   //early register use
   add x5,x6,x7
   str x5, [x1]

   add x1, x1, #4
   cmp x4,x1
   bne test_early_loop
   ret

/**
 * This tests the delay with a load use hazard and use of an early register
 * Input: x0 is the number of iterations, x1 is address of an array
 * Returns: sum in x0
 */
test_load_use_early:
   mov x2, #4
   mul x4,x0,x2 //get # of addrs
   add x4,x4,x1//add the offset to get to the array
   mov x2, #0
   mov x3, #1
   test_load_use_early_loop:
   //early register use
   add x5,x6,x7
   str x5, [x1]

   add x1, x1, #4
   cmp x4,x1
   bne test_load_use_early_loop
   ret

exit:
//ldm sp!, {x4-x11,pc}
