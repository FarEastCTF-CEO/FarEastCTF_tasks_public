// ret: 7 bytes of code, need to jump to get_flag()
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>
#include <signal.h>

static void die(const char *msg) {
    perror(msg);
    _exit(1);
}

__attribute__((noinline))
static void get_flag(void) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[!] flag.txt not found");
        _exit(1);
    }
    char buf[128] = {0};
    if (!fgets(buf, sizeof(buf), f)) {
        puts("[!] failed to read flag");
        _exit(1);
    }
    fclose(f);
    puts(buf);
    _exit(0);
}

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    alarm(10);

    puts("Tiny shellcode playground!");
    puts("I'll execute up to 7 bytes you send me.");

    void *code = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                      MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (code == MAP_FAILED) die("mmap");

    ssize_t n = read(0, code, 7);
    if (n <= 0) {
        puts("No input");
        return 0;
    }

    ((void (*)(void))code)();
    puts("Returned. Bye.");
    return 0;
}
