#include <stdio.h>
#include "hex_printer.h"

void print_hex(const char *label, const uint8_t *data, size_t len) {
    printf("%s: ", label);
    for (size_t i = 0; i < len; ++i) {
        printf("%02x ", data[i]);
    }
    printf("\n");
}