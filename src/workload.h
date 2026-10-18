#ifndef WORKLOAD_H
#define WORKLOAD_H

typedef enum {
    WORKLOAD_OK = 0,
    WORKLOAD_INVALID_VOLUME,
    WORKLOAD_INVALID_EFFORT,
    WORKLOAD_ERROR
} workload_status;

typedef workload_status (*workload_fn)(long volume, int effort);

#endif
