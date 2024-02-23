#include "stdlib.h"

/*
Multiline comment
*/
int main()
{
    /*foo*/
    foo();
    //__TREECUTTER_MARKER__: single-line comment which should be kept -- with whitespace!
    #ifdef BAR
    bar();
    #else
    baz();
    #endif
    /*__TREECUTTER_MARKER__:
    Here's multiline text which should be kept
    */
}
