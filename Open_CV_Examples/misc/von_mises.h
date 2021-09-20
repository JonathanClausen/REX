#ifndef VON_MISES_H
#define VON_MISES_H

#include <cmath>

inline
double square (double x)
{
  return x*x;
}

inline
double bessi0 (double x)
{
  const double abs_x = fabs (x);
  double retval;

  if (abs_x < 3.75)
    {
      const double y = square (x / 3.75);
      retval = 1.0 + y * (3.5156229 + y * (3.0899424 + y * (1.2067492 + 
                     y * (0.2659732 + y * (0.360768e-1 + y * 0.45813e-2)))));
    }
  else
    {
      const double y = 3.75 / abs_x;
      retval = (exp (abs_x) / sqrt(abs_x)) * (0.39894228 + y * (0.1328592e-1 + 
               y * (0.225319e-2 + y * (-0.157565e-2 + y * (0.916281e-2 +
               y * (-0.2057706e-1 + y * (0.2635537e-1 + y * (-0.1647633e-1 +
               y * 0.392377e-2))))))));
    }

  return retval;
}

inline
double von_mises_pdf (double x, double mu, double kappa)
{
  const double p = exp (kappa * cos (x - mu));
  const double Z = 2.0 * M_PI * bessi0 (kappa);
  return p / Z;
}

#endif // VON_MISES_H
