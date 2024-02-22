#include <stdio.h>

int GLOBAL_1 = 0;

int foo(int a, int b) {
    return a + b;
}

struct foo {
    int x;
    char y;
};

int GLOBAL_2 = 5;

int main() {
    printf("%d + %d = %d\n", 1, 2, foo(1, 2));
}
