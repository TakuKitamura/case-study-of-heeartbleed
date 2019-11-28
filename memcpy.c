#include "Heartbleed.h"
#include <string.h>

void Heartbleed_memcpy(void *dst, void *src, uint32_t len) {
    memcpy(dst, src, len);
}