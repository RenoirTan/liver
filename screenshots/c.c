#include <stdio.h>
#include <stdint.h>
#define MAX(x, y) (x > y ? x : y)

typedef int i32;

struct Vector {
    char *buffer;
    size_t capacity;
    size_t length;
};

int main(int argc, char **argv) {
    int a, b;
    printf("Weighing scale! Enter 2 numbers: ");
    scanf("%d %d", &a, &b);
    printf("%d is bigger.\n", MAX(a, b));
    return 0;
}