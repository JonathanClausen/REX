/**
 * This header includes macros for indexing pixels in the IplImage data structure
 * used in OpenCV 1.0 and onwards.
 */

#ifndef INDEX_H
#define INDEX_H

#define GRAY(IMAGE, X, Y) \
    ((uchar*)((IMAGE)->imageData  + (IMAGE)->widthStep*(Y)))[X]
#define RED(IMAGE, X, Y) \
  ((uchar*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3+2]
#define GREEN(IMAGE, X, Y) \
  ((uchar*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3+1]
#define BLUE(IMAGE, X, Y) \
  ((uchar*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3]

#define GRAY_T(TYPE, IMAGE, X, Y) \
    ((TYPE*)((IMAGE)->imageData  + (IMAGE)->widthStep*(Y)))[X]
#define RED_T(TYPE, IMAGE, X, Y) \
  ((TYPE*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3+2]
#define GREEN_T(TYPE, IMAGE, X, Y) \
  ((TYPE*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3+1]
#define BLUE_T(TYPE, IMAGE, X, Y) \
  ((TYPE*)((IMAGE)->imageData + (IMAGE)->widthStep*(Y)))[(X)*3]

#endif
