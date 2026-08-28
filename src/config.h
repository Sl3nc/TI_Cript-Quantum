#ifndef CONFIG_H
#define CONFIG_H

#include <stddef.h>

#include "workload.h"

typedef struct {
    const char *name;
    workload_fn run;
} algorithm_entry;

extern const algorithm_entry ALGORITHMS[];
extern const size_t ALGORITHMS_COUNT;

workload_fn workload_lookup(const char *name);

#endif
