/*
Copyright (c) 2016, Intel Corporation

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Intel Corporation nor the names of its contributors
      may be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define noinline __attribute__((noinline))

unsigned char g_buffer[] = "123";

unsigned int get_rnum(int min, int max)
{
    return (unsigned int)((((double)(max-min+1)/RAND_MAX) * rand()) + min);
}

noinline
static void bad_function(void)
{
    unsigned char buffer[] = "XYZ";
    unsigned idx           = get_rnum(4, 100);
    printf("Bad-Stack[%u]: %c\n", idx, buffer[idx]);
    return;
}

noinline
static void good_function(void)
{
    unsigned char buffer[] = "ABC";
    unsigned int idx       = get_rnum(0, 3);
    printf("Good-Stack[%u]: %c\n", idx, buffer[idx]);
    return;
}

int main(int argc, char **argv)
{
    unsigned int max = 10;
    unsigned int choice;
    unsigned int i;
    unsigned int idx;
    char *ptr;

    if (argc >= 2) {
        max = abs(strtoul(argv[1], &ptr, 10));
        if (*ptr != '\0' || argv[1][0] == '-') {
            printf("Error: Invalid unsigned integer\n");
            return 1;
        }
    }
    srand(time(NULL));
    for (i = 0; i < max; i++) {
        choice = get_rnum(0,2);
        if (!choice) {
            if (!get_rnum(0,1)) {
                idx = get_rnum(0,2);
                printf("Good-Global[%u]: %c\n", idx, g_buffer[idx]);
            } else {
                idx = get_rnum(3,100);
                printf("Bad-Global[%u]: %c\n", idx, g_buffer[idx]);
            }
        } else if (choice == 1) {
            bad_function();
        } else {
            good_function();
        }
    }
    return 0;
}
