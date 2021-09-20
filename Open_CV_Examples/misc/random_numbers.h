#ifndef RANDOM_NUMBERS_H
#define RANDOM_NUMBER_H

// Random number between 0 and 1 (uniform distribution)
float randf();

// Normal random number generater (Box-Muller method)
// (see www.taygeta.com/random/gaussian.html)
// mean m, standard derivation s
float randn(float m, float s);

#endif
