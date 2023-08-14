#ifndef HEX_PRINTER_H
#define HEX_PRINTER_H

#include <stdint.h>
#include <stddef.h>

void print_hex(const char *label, const uint8_t *data, size_t len);

#endif // HEX_PRINTER_H