#ifndef INCLUDED_HASHLIB_HASHER_H
#define INCLUDED_HASHLIB_HASHER_H
#include <stddef.h>

// http://www.cse.yorku.ca/~oz/hash.html
extern size_t hashlib_hasher_djb2(const unsigned char s[static const 1], size_t n);

// sillyness
extern size_t hashlib_hasher_strings_pyhash(
    const unsigned char strings[static const 1],
    size_t lengths[static const 1],
    size_t n
);

#endif  // INCLUDED_HASHLIB_HASHER_H
