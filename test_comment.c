#include "stdlib.h"

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
