__kernel void mandelbrot_kernel(__global float2 *c,
                                __global float *M,
                                const int I,
                                const float T) {
    // Get the global thread ID
    int gid = get_global_id(0);

    // Create a complex number
    float c_re = c[gid].x;
    float c_im = c[gid].y;

    // Create a complex number z
    float z_re = 0.0f;
    float z_im = 0.0f;

    // Initialize M to 0
    M[gid] = 0.0f;
    
    // Initialize stopped
    bool stopped = false;

    for (int i = 0; i < I; i++) {
        // Compute z = z^2 + c
        float z_re_new = z_re * z_re - z_im * z_im + c_re;
        float z_im_new = 2 * z_re * z_im + c_im;

        // Update z
        z_re = z_re_new;
        z_im = z_im_new;

        // If T <= |z|
        if (T * T <= z_re * z_re + z_im * z_im) {
            M[gid] = (float)i / (float)I;
            stopped = true;
            break;
        }
    }

    // If the point is in the Mandelbrot set, M[gid] = 0
    if (M[gid] == 0.0f && !stopped) {
        M[gid] = 1.0f;
    }
}
