#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "cv.h"
#include "cxcore.h"
#include "highgui.h"

#include "index.h"
#include "random_numbers.h"
#include "tsht.h"

/***********************************/
/** Some minor auxilary functions **/
/***********************************/

// Makes sure the choordinates of all the samples are within the image
inline void fix_point (CvPoint &p, const CvSize &size)
{
    // X-choord
    if (p.x < 0)
        p.x = 0;
    else if (p.x > size.width-1)
        p.x = size.width-1;

    // Y-choord
    if (p.y < 0)
        p.y = 0;
    else if (p.y > size.height-1)
        p.y = size.height-1;
}

// Computes euclidian distance between points
inline float dist(const CvPoint &a, const CvPoint &b)
{
    const float tmp_x = (a.x - b.x);
    const float tmp_y = (a.y - b.y);
    const float d = sqrt( tmp_x*tmp_x + tmp_y*tmp_y );
    return d;
}
/************ End of auxilary functions **************/

/*************************/
/** The tsht object **/
/*************************/

// Constructor
tsht::tsht(CvPoint initial_position, unsigned int _radius, unsigned int num_samples)
{
    length  = num_samples;
    samples = (CvPoint*) malloc(length*sizeof(CvPoint));
    weights = (float*)   malloc(length*sizeof(float));
    cumsum  = (float*)   malloc(length*sizeof(float));
    areas   = (int*)     malloc(length*sizeof(int));
    mean = initial_position;
    old_mean = initial_position;
    radius = _radius;

    reinitialize(initial_position, (float)radius/2.0);
}

// Destructor
tsht::~tsht()
{
    free(samples);
    free(weights);
    free(cumsum);
    free(areas);
}

// Returns the currently best estimate of the object position
CvPoint tsht::object_position()
{
    return mean;
}

// Returns the average estimate of the object size (units depend on data)
float tsht::object_size()
{
    int area = 0;
    for (int i = 0; i < length; i++) { area += areas[i]; }
    return (float)area/(float)length;
}

// Returns the actual samples
const CvPoint* tsht::get_samples()
{
    return samples;
}

// Draws new normaly distributed samples around 'new_position'
void tsht::reinitialize(CvPoint new_position, float uncertainty)
{
    // Initial sample values
    for (int i = 0; i < length; i++) {
        samples[i].x = new_position.x + (int)randn(0, uncertainty);
        samples[i].y = new_position.y + (int)randn(0, uncertainty);
        weights[i] = 1.0;
    }
    refresh();
}

// Normalizes the weights and update the accumulated sum of weights.
void tsht::refresh()
{
    // Normalize weights
    double sum = 0;
    for (int i=0; i < length; i++) {
        sum += weights[i];
    }
    if (sum != 0) {
        for (int i = 0; i < length; i++) {
            weights[i] = weights[i]/sum;
        }
    }

    // Accumulated sum
    cumsum[0] = weights[0];
    for (int i = 1; i < length; i++) {
        cumsum[i] = cumsum[i-1] + weights[i];
    }

    // Recompute mean
    int x = 0; int y = 0;
    for (int i = 0; i < length; i++) {
        x += samples[i].x;
        y += samples[i].y;
    }
    mean = cvPoint(x/length, y/length);
}

// The meanshift operator.
//
// Input:
//   P: The probability map.
//   pos: The current position.
//   s: The "filter" will be 2s+1 by 2s+1.
// Output:
//   The function returns the updated position.
//   If given m00_out will contain the computed mean value,
//   which is useful as an estimate of the area of the tracked object.
static CvPoint meanshift(IplImage *P, CvPoint pos, int *m00_out, unsigned int radius)
{
    const int max_iter = 10;
    const CvSize size = cvGetSize(P);
    int m00 = 0, m10, m01;
    CvPoint new_pos;
    new_pos = pos;

    for (int i=0; i < max_iter; i++) {
        // Calculate zeroth and first moment
        const int startx = MAX(0, pos.x-(int)radius);
        const int starty = MAX(0, pos.y-(int)radius);
        const int stopx  = MIN(pos.x+(int)radius, size.width-1);
        const int stopy  = MIN(pos.y+(int)radius, size.height-1);
        m00 = 0; m10 = 0; m01 = 0;
        for (int x = startx; x <= stopx; x++) {
            for (int y = starty; y <= stopy; y++) {
                const int val = GRAY(P, x, y);
                m00 += val;
                m10 += x*val;
                m01 += y*val;
            }
        }

        // If the mean is 0, there's no reason to continue.
        if (m00 <= 0) {
            break;
        }

        // Perform meanshift
        new_pos.x = m10/m00;
        new_pos.y = m01/m00;
        pos = new_pos;
    }

    // We're done
    if (m00_out) *m00_out = m00;
    return new_pos;
}

// Runs meanshift on all samples. The found areas are used to update
// the weights (large areas, gives large weights). The weights are updated
// like this:
//   new_weight = f(area) * old_weight;
// where 'f' is the following piecewise linear function
//  f(area) = 1.0,                     if area > 0.8*max_area
//  f(area) = 0.0,                     if area < 0.2*max_area
//  f(area) = (area-min)/(max-min),    otherwise
// so 'f' is a continuous function.
void tsht::measure_meanshift(IplImage *P, int radius)
{
    const CvSize size = cvGetSize(P);

    // Variables for the weight updating
    const float max_area = (2*radius+1)*(2*radius+1)*255;
    const float max = 0.8*max_area;
    const float min = 0.2*max_area;
    int area;
    float area_weight;

    // Meanshift on all samples
    for (int i = 0; i < length; i++) {
        // Call meanshift
        samples[i] = meanshift(P, samples[i], &area, radius);
        fix_point(samples[i], size);
        areas[i] = area;

        // Update sample weight according to the area.
        if (area > max) {
            area_weight = 1;
        } else if (area < min) {
            area_weight = 0;
        } else {
            area_weight = (area-min)/(max-min);
        }
        weights[i] = GRAY(P, samples[i].x, samples[i].y) * area_weight;
    }
}

// Updates the position of the object using a particle filter and
// the meanshift operator.
status tsht::update(IplImage *P)
{
    // Select new samples
    CvPoint sm[length];
    for (int i = 0; i < length; i++) {
        const float r = randf();
        for (int j = 0; j < length; j++) {
            if (cumsum[j] >= r) {
                sm[i] = samples[j];
                break;
            }
        }
    }
    for (int i = 0; i < length; i++) {
        samples[i] = sm[i];
    }

    // Predict
    predict();
    //predict_brown();

    // Measure
    measure_meanshift(P, radius);

    // Update the tsht object (normalize weights, etc.)
    refresh();

    // If all samples have weight zero, the tracker has lost the object
    if (cumsum[length-1] == 0) {
        return LOST_OBJECT;
    } else {
        return OK;
    }
}


/************************/
/**     Prediction     **/
/************************/

// The default predictor. This function might be the most complex
// part of the code. The predictions will be drawn from a non-isotropic
// normal distribution whose main principal axis is parallel to the
// standard linear prediction.
void tsht::predict ()
{
    CvPoint new_m = mean;
    const int min_cov = 3;
    CvPoint trans;
    trans.x = (new_m.x - old_mean.x);
    trans.y = (new_m.y - old_mean.y);

    /////////////////////////////////
    //     cov model
    ///////////////////////////////

    float v1[2];
    float v2[2];
    // Hvad er dette for en størrelse??
    float d = dist(new_m, old_mean);

    float dist1;
    if (d < min_cov) {
        v1[0] = 0;
        v1[1] = min_cov;
        v2[0] = min_cov; v2[1] = 0;
    } else {
        v1[0] = (float)trans.x;
        v1[1] = (float)trans.y;

        if (v1[1] == 0) {
	        v2[0] = 0.0;
            v2[1] = 1;
        } else {
            v2[1] = -v1[0]/v1[1];
            v2[0] = 1;
        }
        dist1 = sqrt((v2[1]*v2[1]+1));
        v2[0] = (v2[0]/dist1)*(d/2); 
        v2[1] = (v2[1]/dist1)*(d/2);
    }

    const float spread = 2;
    CvPoint transform;
    for (int i = 0; i < length; i++) {
        float d0 = randn(0, spread);
        float d1 = randn(0, spread); 

        ////////////////////////////////////
        //            cov model
        ////////////////////////////////////
        transform.x = (int)round(v1[0] * d0 + v2[0] * d1);
        transform.y = (int)round(v1[1] * d0 + v2[1] * d1);

        samples[i].x += transform.x;
        samples[i].y += transform.y;
        // fix_point(samples[i]); // XXX: Denne linie skal ikke være udkommenteret
    }
}

void tsht::predict_brown()
{
    const int spread = 3;
 
    for (int i = 0; i < length; i++) {
        samples[i].x += (int)round(randn(0, spread));
        samples[i].y += (int)round(randn(0, spread));
        // fix_point(samples[i]); // XXX: Denne linie skal ikke være udkommenteret
    }
}

/*
// Returns the mean point of the samples.
CvPoint mean(object &obj)
{
  int x = 0; int y = 0;

  for (int i = 0; i < obj.length; i++) {
      x += obj.samples[i].x;
      y += obj.samples[i].y;
}
  
  return cvPoint(x/obj.length, y/obj.length);  
}

// Returns the mean point of the samples.
int mean_area(object &obj)
{
    int sum = 0;
    for (int i = 0; i < obj.length; i++) {
        sum += obj.areas[i];
}
    return sum/obj.length;  
}
*/

