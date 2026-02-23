// arbitrary_write: write arbitrary 32-bit value to arbitrary address.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint32_t VAR = 0;

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

    puts("One write to rule them all.");
    puts("If VAR == 0x00defaced -> flag");

    unsigned long long addr = 0;
    unsigned int value = 0;

    printf("addr (hex, e.g. 0x404050): ");
    if (scanf("%llx", &addr) != 1) {
        puts("Bad input");
        return 1;
    }

    printf("value (hex, e.g. 0x00defaced): ");
    if (scanf("%x", &value) != 1) {
        puts("Bad input");
        return 1;
    }

    uint32_t *p = (uint32_t *)(uintptr_t)addr;
    *p = value;

    printf("VAR = 0x%08x\n", VAR);
    if (VAR == 0x00defacedu) {
        puts("Nice!" );
        print_flag();
        return 0;
    }

    puts("Nope.");
    return 0;
}
