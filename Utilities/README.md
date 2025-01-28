# Utilities

This module provides a list of helpful tools that can help you during the development of your project.

### [Interactive color filtering](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/Utilities/Support/ColorThresholdSelector.py)

This example implements an interactive tool for determining color filtering parameters. The image is first blurred using a gaussian kernel, and adjusted for gamma. The color filtering depends on a lower and upper limit of HSV values which are used to threshold the image in HSV color-space. The script will open a window providing controls for:

  1. Blurring --> Gaussian size (Kernel) and standard deviation (Sigma)
  2. Gamma correction --> Target value (Gamma) (16 --> 1.6)
  3. Lower and Upper thresholds for HSV image masking within  [0-255]    
    
- More information: [Gamma correction](https://www.e-consystems.com/blog/camera/technology/what-is-gamma-correction-and-why-is-it-so-crucial-for-embedded-vision-systems/)

### [Multi-threading](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/Utilities/Support/MultiThreading.py)

This example demonstrates multithreading in Python. Multithreading is a powerful tool that allows multiple tasks to run concurrently or in the background. This keeps the main Python thread free to perform important work, such as maintaining UI responsiveness.

- More information: [Threading](https://realpython.com/intro-to-python-threading/)

### [ROI selection](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/Utilities/Support/SimpleROISelector.py)

In computer vision, a region of interest (ROI) describes a subregion of an image in pixel coordinates. An ROI is commonly represented as a vector with 4 elements [x ,y, w, h] where:

1. [x, y] are the pixel coordinates of the region. This can be the center or one of the corners. 
2. [w, h] are the width and height of the region.
   
Selecting an ROI is a key part of later image processing stages as it provides information about the image content and focus to an algorithm and often reduces the process cost involved.
OpenCV offers an ROI selection implementation that works on static images. Our own simple implementation of an ROI selector that allows working on live images is also made available.

- More information: [OpenCV Examples](https://www.geeksforgeeks.org/python-opencv-selectroi-function/)

### [RealSense cameras](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/tree/main/Utilities/RealSenseCamera)

This module demonstrates how to access the RealSense camera streams and process the images. The RealSense camera has multiple sensors that give different views of the world (RGB, depth, infrared).

To get to know the RealSense cameras, you can check out the [Intel RealSense SDK](https://intelrealsense.github.io/librealsense/python_docs/_generated/pyrealsense2.html#module-pyrealsense2) to play around with the sensors and try out some filtering and processing steps. Camera stream access may be achieved manually using the [Intel API](https://canvas.vub.be/courses/36046/files/2285191?wrap=1) or using our [RealSenseCamera](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/tree/main/Utilities/RealSenseCamera/RealSenseCamera.py) class which simplifies setup. 

The RealSense cameras enable advanced image processing and merging of sensor maps. The [PointcloudViewer.py](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/Utilities/RealSenseCamera/PointCloudViewer2-1.py) provides a demo of the cameras highlighting spatial & temporal filtering, decimation, colorization, and lighting.

- More information:  [Examples](https://github.com/IntelRealSense/librealsense/tree/development/wrappers/python/examples), [Filtering](https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/depth_filters.ipynb)

### [Handling mouse events](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/Utilities/Support/Mouse_paint.py)

This example illustrates how to handle mouse events and use them to draw objects on a screen.
