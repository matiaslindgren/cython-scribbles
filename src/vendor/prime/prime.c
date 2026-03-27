#include "prime.h"
#include <math.h>

extern int is_prime(int x) {
  if (x < 2) {
    return 0;
  }
  if (x < 4) {
    return 1;
  }
  int end = 1 + (int)sqrt((double)x);
  for (int d = 2; d < end; ++d) {
    if (x % d == 0) {
      return 0;
    }
  }
  return 1;
}
