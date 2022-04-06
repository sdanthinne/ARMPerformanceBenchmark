
.global simple_data_hazard_no_count
simple_data_hazard_no_count:
//no arguments
mov x2, 4
mov x3, 5
add x4, x3, x2
add x3, x4, x2
ret

.global simple_data_hazard
simple_data_hazard:
//argument 0 should be a pointer
mrs x1, PMCCNTR_EL0
mov x2, 4
mov x3, 5
add x4, x3, x2
add x3, x4, x2
mrs x5, PMCCNTR_EL0
sub x1, x5, x1
str x1, [x0]
ret
