#include "highgui.h"

#ifndef PWC_H
#define PWC_H

/* pwc_whitebalance.mode values */
#define PWC_WB_INDOOR       0
#define PWC_WB_OUTDOOR      1
#define PWC_WB_FL           2
#define PWC_WB_MANUAL       3
#define PWC_WB_AUTO         4

struct pwc_whitebalance
{
    int mode;
    int manual_red, manual_blue;    /* R/W */
    int read_red, read_blue;        /* R/O */
};

class pwc {
public:
    pwc(CvCapture *cam);
    ~pwc();

    void   set_window_size(CvSize size);
    CvSize get_window_size();

    void set_gain(int gain);
    void set_balance_mode(int mode);
    void set_balance(int red, int blue);
    void get_balance(int *red, int *blue);
    void set_shutter_speed(int speed);

private:
    int device;
    struct pwc_whitebalance whitebalance;
    CvCapture *cvcam;
    int current_red, current_blue;
};

#endif
