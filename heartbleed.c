#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main(int argc, char const *argv[]) {
    // 0x0f, 0xa0 = 4000 (payload_length)
    // 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64 = "payload" (payload)
    uint8_t request[9] = {0x0f, 0xa0, 0x70, 0x61, 0x79, 0x6c, 0x6f, 0x61, 0x64};
    // uint8_t *request = (uint8_t *)malloc(sizeof(uint8_t) * 9);
    // request[0] = 0x0f, request[1] = 0xa0, request[2] = 0x70, request[3] = 0x61, request[4] = 0x79, request[5] = 0x6c, request[6] = 0x6f, request[7] = 0x61, request[8] = 0x64;
    size_t request_size = sizeof(request) / sizeof (uint8_t);
    if (request_size < 3 || request_size > 65535 + 2) {
        printf("request_size is invalid.\nrequest_size = %zu\n", request_size);
        return 1;
    }

    uint8_t *response = (uint8_t *)malloc(sizeof(uint8_t) * (request_size - 2));
    if (response == NULL) {
        puts("response-malloc is failed.");
        return 1;
    }
    uint32_t payload_length = ((uint32_t)request[0] << 8) | (uint32_t)request[1];
    memcpy(response, request + 2, payload_length);

    for (uint32_t i = 0; i < payload_length; i++)
        printf("%c", response[i]);
    free(response);
    return 0;
}
