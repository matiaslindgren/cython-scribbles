#include "hasher.h"
#include <stddef.h>

extern size_t hasher_djb2(unsigned char *s, size_t n) {
  size_t h = 5381;
  for (size_t i = 0; i < n; ++i) {
    h = ((h << 5) + h) + (size_t)(s[i]);
  }
  return h;
}
