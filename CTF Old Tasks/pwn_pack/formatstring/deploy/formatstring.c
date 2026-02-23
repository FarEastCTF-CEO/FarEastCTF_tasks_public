// formatstring: printf(user_input, ...) leak secret (8th argument)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

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
    uint32_t secret = (uint32_t)rand();

    char name[256];
    memset(name, 0, sizeof(name));

    puts("I picked a secret number. Guess it!");
    printf("What is your name? ");
    if (!fgets(name, sizeof(name), stdin)) {
        return 1;
    }
    name[strcspn(name, "\n")] = 0;

    printf("Hello, ");
    // Intentional vuln: user controls format string.
    // We also pass 7 dummy values so 'secret' becomes the 8th argument.
    printf(name,
           0x11111111u,
           0x22222222u,
           0x33333333u,
           0x44444444u,
           0x55555555u,
           0x66666666u,
           0x77777777u,
           secret);
    puts("!");

    unsigned int guess = 0;
    printf("Now guess the secret (hex, without 0x): ");
    if (scanf("%x", &guess) != 1) {
        puts("Bad input");
        return 1;
    }

    if (guess == secret) {
        puts("Correct!");
        print_flag();
        return 0;
    }

    puts("Wrong.");
    return 0;
}
