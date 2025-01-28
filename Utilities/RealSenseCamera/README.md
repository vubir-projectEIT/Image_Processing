# RealSense camera

### Get to know the RealSense camera

The RealSense camera has multiple sensors that give different views of the world:
- RGB sensor map
- 3D depth map
- Infrared sensor map (left and right)
  
To get to know the RealSense cameras, you can check out the Intel RealSense SDK to play around with the sensors and try out some filtering and processing steps.
Camera stream access may be achieved manually using the Intel API or using our RealSenseCamera.py class which simplifies setup.

### Image processing and merging of sensor maps

The demo highlights:
- Spatial & Temporal filtering
- Decimation
- Colorization
- Lighting
The demo relies on the Intel RealSense2 SDK and is implemented in Python. However, alternate bindings are provided in the SDK (eg, MATLAB, C#/.NET).

Other sample codes can be found [here](https://github.com/IntelRealSense/librealsense/tree/development/wrappers/python/examples).
Information on filtering can be found [here](https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/depth_filters.ipynb).
