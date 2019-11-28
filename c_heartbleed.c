#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

int main(int argc, char const *argv[]) {
    uint8_t request[XXXXX] = {YYYYY};
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
    puts("\ndone");
    return 0;
}
