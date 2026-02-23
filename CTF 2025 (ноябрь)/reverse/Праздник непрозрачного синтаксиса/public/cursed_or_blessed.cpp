
#include <stdio.h>
#include <string.h>
#define OMNISSIAH return
#define CANTICLE for
#define SIGIL ;
#define RITE =
#define AUGMENT char
#define REVERENCE printf
#define SCRIBE_INPUT fgets
#define CONTINUE_SERVO continue
#define INVOCATION (
#define BINDING )
#define RITUAL_BEGIN {
#define RITUAL_END }
#define TRANSMUTE_STEP1(x) ((x) ^ 13)
#define TRANSMUTE_STEP2(x) ((TRANSMUTE_STEP1(x)) ^ 42)
#define TRANSMUTE(x) ((char)(TRANSMUTE_STEP2((unsigned char)(x))))
#define REVERSE_STEP1(x) ((x) ^ 42)
#define REVERSE_STEP2(x) ((REVERSE_STEP1(x)) ^ 13)
#define REVERSE(x) ((char)(REVERSE_STEP2((unsigned char)(x))))
AUGMENT f[] RITE "\x61\x62\x64\x73\x61\x5c\x4e\x48\x44\x44\x44\x78\x42\x49\x4d\x48\x5e\x42\x55\x5a" SIGIL
AUGMENT ff[] RITE "\x6e\x49\x57\x52\x53\x07\x46\x07\x41\x4b\x46\x40" SIGIL
AUGMENT fff[] RITE "\x50\x55\x48\x49\x40" SIGIL
AUGMENT ffff[] RITE "\x54\x52\x44\x44\x42\x54\x54" SIGIL
AUGMENT buf[32] RITE{ 0 } SIGIL
int main INVOCATION BINDING RITUAL_BEGIN
CANTICLE INVOCATION int i RITE 0; i < sizeof(ff) - 1; i++ BINDING RITUAL_BEGIN
    buf[i] RITE TRANSMUTE((unsigned char)ff[i]) SIGIL
    RITUAL_END
    REVERENCE INVOCATION "%s\n", buf BINDING SIGIL
    CANTICLE INVOCATION int i RITE 0; i < sizeof(buf) - 1; i++ BINDING RITUAL_BEGIN
    buf[i] RITE 0 SIGIL
    RITUAL_END
    SCRIBE_INPUT INVOCATION buf, sizeof(f) + 1, stdin BINDING SIGIL
    buf[strcspn(buf, "\n")] RITE 0 SIGIL
    CANTICLE INVOCATION int i RITE 0; i < sizeof(f) - 1; i++ BINDING RITUAL_BEGIN
    buf[i] RITE REVERSE((unsigned char)buf[i]) SIGIL
    RITUAL_END
    CANTICLE INVOCATION int i RITE 0; i < sizeof(f) - 1; i++ BINDING RITUAL_BEGIN
    if INVOCATION buf[i] == f[i] BINDING CONTINUE_SERVO SIGIL
    else RITUAL_BEGIN
        CANTICLE INVOCATION int j RITE 0; j < sizeof(buf) - 1; j++ BINDING RITUAL_BEGIN
        buf[j] RITE 0 SIGIL
        RITUAL_END
        CANTICLE INVOCATION int k RITE 0; k < sizeof(fff) - 1; k++ BINDING RITUAL_BEGIN
        buf[k] RITE TRANSMUTE((unsigned char)fff[k]) SIGIL
        RITUAL_END
        REVERENCE INVOCATION "%s\n", buf BINDING SIGIL
        OMNISSIAH 0 SIGIL
        RITUAL_END
        RITUAL_END
        CANTICLE INVOCATION int j RITE 0; j < sizeof(buf) - 1; j++ BINDING RITUAL_BEGIN
        buf[j] RITE 0 SIGIL
        RITUAL_END
        CANTICLE INVOCATION int k RITE 0; k < sizeof(ffff) - 1; k++ BINDING RITUAL_BEGIN
        buf[k] RITE TRANSMUTE((unsigned char)ffff[k]) SIGIL
        RITUAL_END
        REVERENCE INVOCATION "%s\n", buf BINDING SIGIL
        OMNISSIAH 0 SIGIL
        RITUAL_END
