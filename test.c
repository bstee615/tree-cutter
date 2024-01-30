#include <stdio.h>

int foo(int a, int b) {
    return a + b;
}

int main() {
    printf("%d + %d = %d\n", 1, 2, foo(1, 2));
}
