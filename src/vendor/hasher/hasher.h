#ifndef INCLUDED_HASHER_H
#define INCLUDED_HASHER_H
#include <stddef.h>

// http://www.cse.yorku.ca/~oz/hash.html
extern size_t hasher_djb2(unsigned char *s, size_t n);

#endif // INCLUDED_HASHER_H
