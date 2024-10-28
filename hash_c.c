#include <stdio.h>

short arkhash(char* str) {
    unsigned int uVar1;
    unsigned int ret = 0;
    unsigned int uVar3 = 0;
    unsigned int shift = 0;
    char c = *str;
    while (c & 0xFFFFu) {
        c = *str;
        uVar1 = uVar3 ^ (+c & 0xFFFFu) << shift;
        uVar3 = uVar1 & 0xFFFF;
        ret = uVar1;
        shift = (shift + 1) & 7;
        str++;
    }
    return ret;
}

int main() {
    printf("arkhash(\"%s\") returned %d, should be 0\n", "", arkhash(""));
    printf("arkhash(\"%s\") returned %d, should be 277\n", "gen", arkhash("gen"));
    printf("arkhash(\"%s\") returned %d, should be 3832\n", "loading.rnd.gz", arkhash("loading.rnd.gz"));
}
