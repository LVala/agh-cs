CC = gcc
CFLAGS = -Wall

all: main

main: main.c
	$(CC) $(CFLAGS) -o main -lm main.c

run: main
	./main

clean:
	rm -f *.o main