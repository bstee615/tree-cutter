#include "stdlib.h"

/*
Multiline comment
*/
int main()
{
    /*foo*/
    foo();
    //bar or baz
    #ifdef BAR
    bar();
    #else
    baz();
    #endif
}
