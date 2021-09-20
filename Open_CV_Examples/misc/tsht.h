#include "cxcore.h"

#ifndef TSHT_H
#define TSHT_H

enum status {
    LOST_OBJECT,        // The tracker lost the object.
    OK                  // The tracker is still tracking the object.
};

class tsht {
    public:
        // Constructor and destructor
        tsht(CvPoint initial_position, unsigned int radius=10, unsigned int num_samples=50);
        ~tsht();

        // The tracking functionality
        status update(IplImage *probmap);
        void reinitialize(CvPoint new_position, float uncertainty=10);

        // Get information about the tracked object
        CvPoint object_position();
        float object_size();
        const CvPoint* get_samples();

    private:
        // Data
        CvPoint *samples;
        float *weights;
        float *cumsum;
        int *areas;
        unsigned int length;
        CvPoint mean;
        CvPoint old_mean;
        unsigned int radius;

        // Helper functions
        void refresh(); // Normalizes the weights and update the accumulated sum of weights.
        void measure_meanshift(IplImage *P, int radius); // Runs meanshift on all samples.

        // Predictors
        void predict(); // Covariance model
        void predict_brown(); // Brownian motion
};

#endif
