CC=gcc
CFLAGS=-ggdb -Og

ifeq ($(GPROF),1)
	CFLAGS += -pg
endif

all: main

main: mainTest.c test_asm.o
	$(CC) $^ -o $@ $(CFLAGS)

testNoSyscall: testNoSyscall.c test_asm.o
	$(CC) $^ -o $@ $(CFLAGS)

testTimer: testTimer.c test_asm.o
	$(CC) $^ -o $@ $(CFLAGS)

test_asm.o: test_asm.S
	$(CC) -c $^ -o $@ $(CFLAGS) 

clean:
	rm -f *.o main
