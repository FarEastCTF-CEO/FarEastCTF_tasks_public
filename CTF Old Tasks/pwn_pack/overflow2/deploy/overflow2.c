// overflow2: kiddie overflow with exact value (0x12345678)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

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

    if (s.is_root == 0x12345678u) {
        puts("Access granted!");
        print_flag();
        return 0;
    }

    puts("Nope.");
    return 0;
}
