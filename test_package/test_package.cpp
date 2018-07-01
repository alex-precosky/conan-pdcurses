#include <cstdlib>
#include <iostream>
#include "curses.h"

int main()
{
  const char* version_str = curses_version();
  std::cout << "PDCurses\n";
  return EXIT_SUCCESS;
}
