#include "hashlib_hasher.h"

#include <stddef.h>
#include <string.h>

#include "hashlib_hasher_cpython_str.h"

extern size_t hashlib_hasher_djb2(const unsigned char s[static const 1], size_t n) {
  size_t h = 5381;
  for (size_t i = 0; i < n; ++i) {
    h = ((h << 5) + h) + (size_t)(s[i]);
  }
  return h;
}

extern size_t hashlib_hasher_strings_pyhash(const unsigned char strings[static const 1],
                                            size_t lengths[static const 1],
                                            size_t n) {
  size_t h = 654321;
  for (size_t i_str = 0, i_buf = 0; i_str < n;) {
    const char *s = (const char *)(strings + i_buf);
    size_t s_len = lengths[i_str];
    // extern func that must be linked from the Cython generated lib!
    size_t s_hash = public_hasher_cpython_bytes_hash(s, s_len);
    h = (h << 7) + s_hash;
    i_buf += s_len;
    i_str += 1;
  }
  return h;
}
