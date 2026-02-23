// shellcode: 40 bytes of code, no get_flag(); read flag.txt yourself.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>

static void die(const char *msg) {
    perror(msg);
    _exit(1);
}

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    alarm(10);

    puts("Send up to 40 bytes. I'll execute it.");
    puts("Hint: flag is in ./flag.txt");

    void *code = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (code == MAP_FAILED) die("mmap");

    ssize_t n = read(0, code, 40);
    if (n <= 0) {
        puts("No input");
        return 0;
    }

    ((void (*)(void))code)();
    puts("Returned. Bye.");
    return 0;
}
