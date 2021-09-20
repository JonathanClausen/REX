#include "pwc.h"
#include <sys/ioctl.h>
#include "cxcore.h"
#include "cv.h"
#include "index.h"
#include "stdio.h"
#include <time.h>

// This is just a quick-n-dirty hack. I really should use CvCapturecvcam_V4L
// but I'm too lazy too figure out what should be included.
// Since CvCapturecvcam_V4L not is a public structure I don't think
// there's an easy way to do this.
typedef struct pwc_hack
{
    void* vtable;
    int device;
}
pwc_hack;

/* Used with VIDIOCPWC[SG]AWB (Auto White Balance). 
   Set mode to one of the PWC_WB_* values above.
   *red and *blue are the respective gains of these colour components inside 
   the cvcamera; range 0..65535
   When 'mode' == PWC_WB_MANUAL, 'manual_red' and 'manual_blue' are set or read; 
   otherwise undefined.
   'read_red' and 'read_blue' are read-only.
*/   
/*
struct pwc_whitebalance
{
	int mode;
	int manual_red, manual_blue;	// R/W
	int read_red, read_blue;	// R/O
};
*/
#define VIDIOCPWCSAWB   _IOW('v', 202, struct pwc_whitebalance)
#define VIDIOCPWCGAWB   _IOR('v', 202, struct pwc_whitebalance)

// Contructor
pwc::pwc(CvCapture *cam)
{
    // Create cvcamera handle through opencv
    cvcam = cam;

    // Save device handle
    pwc_hack *hack = (pwc_hack*) cam;
    device = hack->device;

    // Read automaticly tuned parameters
    whitebalance.mode = PWC_WB_AUTO;
    ioctl(device, VIDIOCPWCGAWB, &whitebalance);
    current_red  = whitebalance.read_red;
    current_blue = whitebalance.read_blue;

    // Sleep a while so the camera has time to get adjusted
    cvWaitKey(100);
}

// Destructor
pwc::~pwc()
{
    set_balance_mode(PWC_WB_AUTO);
    cvWaitKey(100);
}

// Controls window size
void pwc::set_window_size(CvSize _size)
{
    cvSetCaptureProperty(cvcam, CV_CAP_PROP_FRAME_WIDTH,  _size.width);
    cvSetCaptureProperty(cvcam, CV_CAP_PROP_FRAME_HEIGHT, _size.height);
}

CvSize pwc::get_window_size()
{
    const double width  = cvGetCaptureProperty(cvcam, CV_CAP_PROP_FRAME_WIDTH);
    const double height = cvGetCaptureProperty(cvcam, CV_CAP_PROP_FRAME_HEIGHT);
    const CvSize size = cvSize( (int)width, (int)height );
    return size;
}

// Gain control
#define VIDIOCPWCSAGC   _IOW('v', 200, int)
void pwc::set_gain(int gain)
{
	ioctl(device, VIDIOCPWCSAGC, &gain);
}

// Color control
void pwc::set_balance_mode(int mode)
{
    whitebalance.mode = mode;
    whitebalance.manual_red  = current_red;
    whitebalance.manual_blue = current_blue;	
    ioctl(device, VIDIOCPWCSAWB, &whitebalance);
}

void pwc::set_balance(int red, int blue)
{
    if (red < 0) red = 0;
    if (red > 65535) red = 65535;
    if (blue < 0) blue = 0;
    if (blue > 65535) blue = 65535;
    current_red  = red;
    current_blue = blue;
    whitebalance.manual_red  = red;
    whitebalance.manual_blue = blue;
    ioctl(device, VIDIOCPWCSAWB, &whitebalance);
}

void pwc::get_balance(int *red, int *blue)
{
    *red  = current_red;
    *blue = current_blue;
}

// Shutter speed
#define VIDIOCPWCSSHUTTER	_IOW('v', 201, int)
void pwc::set_shutter_speed(int speed)
{
    ioctl(device, VIDIOCPWCSSHUTTER, &speed);
}


