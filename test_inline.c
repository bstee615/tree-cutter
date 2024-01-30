#include <stdio.h>

int foo(int a, int b) {
    return a + b;
}

int main() {
    // BEGIN INLINE
int FOO;
int a = 1;
int b = 2;
{
    FOO = a + b;
goto inline_end;
}
inline_end:
printf("%d + %d = %d\n", 1, 2, FOO);
// END INLINE
}

