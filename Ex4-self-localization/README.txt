This directory contains source code that might be helpful when solving
exercise 4. We provide both Python and C++ versions of this code.

The only file that needs editing to create a working system
is selflocalize.py or exercise4.cc, but it is recommended to have a brief look at the rest
of the source code. In particular it is recommended to look at particle.[py|h|cc]
to see how particles are represented.

The files selflocalize.py and exercise4.cc was created by simply removing parts of a
functioning program and replacing these parts by lines saying:
  //XXX: You do this
So look for 'XXX' to see where you should concentrate your efforts. But feel free to restructure 
the code as you see fit.

The program uses the camera class found in camera.[py|h|cc] to access the camera and do the image
analysis. The Python version includes some roughly right calibrations in the constructor of the Camera class. 
The C++ version of this class requires a file containing camera calibration parameters in YAML format. You can calibrate
your own camera using the camera_calibrator found in Absalon under OpenCV, but we also provide some roughly right 
calibration files.

The main C++ project for this exercise can be build using the make command. Just type
make

Alternatively, CMake can be used like this:
mkdir build
cd build/
cmake ..
make

This auto-generates makefile's or you can use the generator facility of cmake to generate project files for your favourite IDE. 

If you have problems understanding the code, do not hesitate to contact me.


Kim Steenstrup Pedersen, september, 2015, 2017, 2018, 2020.
Søren Hauberg, august 21st, 2006.
