import multiprocessing as mp
import numpy as np
from numba import jit

@jit(nopython=True)
def mandelbrot_chunk(c, M, I, T):
    if c.shape != M.shape:
        raise ValueError('c and M must have the same shape')
    
    X_RES, Y_RES = c.shape
    
    for x in range(X_RES):
        for y in range(Y_RES):
            z = 0 + 0j
            for i in range(I):
                z = z**2 + c[x, y]
                if T <= abs(z):
                    M[x, y] = i / I
                    break
            else:
                M[x, y] = 1
                
    return M
                
                
def mandelbrot_paralell(c, M, I, T, P):
    if c.shape != M.shape:
        raise ValueError('c and M must have the same shape')
    
    c_chunks = np.array_split(c, P, axis=0)
    M_chunks = np.array_split(M, P, axis=0)    
    
    pool = mp.Pool(processes=P)

    results = [pool.apply_async(mandelbrot_chunk, args=(c_chunk, M_chunk, I, T)) for c_chunk, M_chunk in zip(c_chunks, M_chunks)]
    
    pool.close()
    pool.join()
    
    M[:] = np.concatenate([result.get() for result in results], axis=0)