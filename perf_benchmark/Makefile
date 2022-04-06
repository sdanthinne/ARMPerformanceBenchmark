CC=gcc
CFLAGS=-ggdb -O2

all: main

main: mainTest.c test_asm.o
	$(CC) $^ -o $@ $(CFLAGS)

testNoSyscall: testNoSyscall.c test_asm.o
	$(CC) $^ -o $@ $(CFLAGS)

test_asm.o: test_asm.S
	$(CC) -c $^ -o $@ $(CFLAGS) 

clean:
	rm -f *.o main
