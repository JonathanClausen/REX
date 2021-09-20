#include <cstdlib>
#include <math.h>

// Random number between 0 and 1 (uniform distribution)
float randf()
{
    const int r = rand();
    return ((float)r)/(float)RAND_MAX;
}

// Normal random number generater (Box-Muller method)
// (see www.taygeta.com/random/gaussian.html)
// mean m, standard deviation s
float randn(float m, float s)
{
    float x1, x2, w, y1, y2;

    do {
        x1 = 2.0 * randf() - 1.0;
        x2 = 2.0 * randf() - 1.0;
        w = x1 * x1 + x2 * x2;
} while(w >= 1.0);
    w = sqrt((-2.0 * log(w)) / w);
    y1 = x1 * w;
    y2 = x2 * w;
    return (m + y1 * s);
}
