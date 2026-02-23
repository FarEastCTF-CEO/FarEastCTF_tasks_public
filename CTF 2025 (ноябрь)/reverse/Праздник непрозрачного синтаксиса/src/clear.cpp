#include <stdio.h>
#include <string.h>
int main() {
    char f[] = "abdsa\\NHDDDxBIMH^BUZ";
    char ff[] = "nIWRSFAKF@";
    char fff[] = "PUHI@";
    char ffff[] = "TRDDBTT";
    char buf[32] = { 0 };
    for (int i = 0; i < sizeof(ff)-1; i++) buf[i] = (char)(ff[i] ^ 13 ^ 42);
    printf("%s\n", buf);
    for (int i = 0; i < sizeof(buf) - 1; i++) buf[i] = 0;
    fgets(buf, sizeof(f)+1, stdin);
    buf[strcspn(buf, "\n")] = 0;
    for (int i = 0; i < sizeof(f)-1; i++) buf[i] = (char)(buf[i] ^ 42 ^ 13);
    for (int i = 0; i < sizeof(f) - 1; i++) {
        if (buf[i] == f[i]) continue;
        else {
            for (int i = 0; i < sizeof(buf) - 1; i++) buf[i] = 0;
            for (int i = 0; i < sizeof(fff) - 1; i++) buf[i] = (char)(fff[i] ^ 13 ^ 42);
            printf("%s\n", buf);
            return 0;
        }
    }
    for (int i = 0; i < sizeof(buf) - 1; i++) buf[i] = 0;
    for (int i = 0; i < sizeof(ffff) - 1; i++) buf[i] = (char)(ffff[i] ^ 13 ^ 42);
    printf("%s\n", buf);
    return 0;
}