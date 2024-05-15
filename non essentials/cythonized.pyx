cimport cython
from cython.parallel import prange

@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)

cpdef norm(long double[:] a):
    cdef long double total = 0
    cdef int i, j
    cdef int length = len(a)
    for i in range(length):
        total += a[i] ** 2
    return total ** 0.5