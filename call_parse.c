#include "Heartbleed.h"
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main(int argc, char const *argv[])
{
    // 0x0f, 0xa0 = 4000 (payload_length)
    // 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64 = "payload" (payload)
    uint8_t request[] = {0x00, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
    // uint8_t request[] = {0x00, 0x07, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
    size_t request_size = sizeof(request) / sizeof (uint8_t);
    if (request_size < 3 || request_size > 65535 + 2) {
        printf("request_size is invalid.\nrequest_size = %zu\n",request_size);
        return 1;
    }
    uint8_t error_code = 0;
    uint32_t payload_length = 0;
    uint8_t *response = parse(request, request_size, &payload_length, &error_code);
    if (error_code != 0) {
        if (error_code == 1)
            puts("response-malloc is failed.");
        else if (error_code == 2)
            puts("packet-parse is failed.");
        else
            puts("unexpected error.");
        return 1;
    }
    for (uint32_t i = 0; i < payload_length; i++)
        printf("%c", response[i]);
    free(response);
    return 0;
}
