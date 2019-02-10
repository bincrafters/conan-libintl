#include <iostream>
#include <libintl.h>

int main()
{
    std::cout << g_libintl_gettext("message") << std::endl;
    return 0;
}
