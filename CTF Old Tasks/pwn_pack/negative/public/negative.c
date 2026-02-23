// negative: signed int overflow (find positive x s.t. (int)(a + x) == b)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

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

    srand((unsigned)time(NULL));

    int32_t a;
    int32_t b;
    uint32_t x_should;

    // Generate until x_should != 0 (so user can input a positive number)
    do {
        a = (int32_t)(1000000000 + (rand() % 900000000)); // positive
        b = (int32_t)(-(1 + (rand() % 1000000)));         // negative small-ish
        x_should = (uint32_t)((uint32_t)b - (uint32_t)a);  // modulo 2^32
    } while (x_should == 0);

    puts("Can you do math in C?");
    printf("a = %d\n", a);
    printf("b = %d\n", b);
    puts("Enter a POSITIVE integer x such that (int32_t)(a + x) == b");
    printf("x = ");

    uint32_t x = 0;
    if (scanf("%u", &x) != 1) {
        puts("Bad input");
        return 1;
    }

    int32_t res = (int32_t)((uint32_t)a + x);
    if (x > 0 && res == b) {
        puts("Correct!");
        print_flag();
        return 0;
    }

    puts("Wrong.");
    return 0;
}
