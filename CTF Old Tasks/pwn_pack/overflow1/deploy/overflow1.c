// overflow1: kiddie overflow (stack struct overflow flips is_root)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

// gets() is removed from modern headers, but still present in libc.
char *gets(char *s);

static void print_flag(void) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[!] flag.txt not found (this is normal on your machine)");
        exit(1);
    }
    char buf[128] = {0};
    if (!fgets(buf, sizeof(buf), f)) {
        puts("[!] failed to read flag");
        exit(1);
    }
    fclose(f);
    printf("%s", buf);
}

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    struct {
        char buffer[64];
        uint32_t is_root;
    } s;

    memset(&s, 0, sizeof(s));

    puts("Welcome!");
    printf("What is your name? ");
    gets(s.buffer); // NOLINT: intentionally unsafe

    if (s.is_root) {
        puts("Access granted!");
        print_flag();
        return 0;
    }

    puts("Nope.");
    return 0;
}
