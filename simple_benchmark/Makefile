CC=gcc
CFLAGS=-ggdb

all: main

main: main.c perf_bmark.o
	$(CC) $^ -o $@ $(CFLAGS)

perf_bmark.o: init_arm.S
	$(CC) -c $^ -o $@ $(CFLAGS)

perf_bmark: perf_bmark.o
	$(CC) $^ -o $@ $(CFLAGS)

clean:
	rm -f *.o main
