import multiprocessing as mp
import numpy as np
from numba import jit


@jit(nopython=True)
def mandelbrot_chunk(c, I, T):
    M = np.zeros(c.shape)
    
    x_max, y_max = c.shape
    
    for x in range(x_max):
        for y in range(y_max):
            z = 0
            for i in range(I):
                z = z**2 + c[x, y]
                if abs(z) > T:
                    M[x, y] = i
                    break
            else:
                M[x, y] = I
    
    return M

def mandelbrot_paralell(c, I, T, P, C):
    pool = mp.Pool(processes=P)

    results = [pool.apply_async(mandelbrot_chunk, args=(c[i:i+C, :], I, T)) for i in range(0, c.shape[0], C)]

    pool.close()
    pool.join()

    return results