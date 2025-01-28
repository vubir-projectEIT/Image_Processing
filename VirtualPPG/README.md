# Virtual PPG

Implement a real-time virtual heart rate sensor, also called virtual PPG, using opencv. 
In this module, we implement a heart rate sensor from scratch using image processing tools and a simple camera. 
We will use this case study to get an overview of all the steps required to do image analysis and dive deep into a specific application. 
When you are able to measure your heart rate in real-time using your camera, you can connect this biomedical information to any other device or application.

We provide you with a template [Virtual_PPG_template.py](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/VirtualPPG/Virtual_PPG_template.py) and some helper functions [Virtual_PPG_helpers.py](https://github.com/LorisGiordano/ProjectEIT-Image-processing-toolbox/blob/main/VirtualPPG/Virtual_PPG_helpers.py) to start your journey. 
Let's start with the idea behind the virtual PPG and a small overview of what we aim to do.

### How does it work?
Virtual heart rate sensing using a camera, also known as virtual photoplethysmography, is a non-contact method that estimates heart rate by analyzing subtle color variations in facial skin captured through video. 
These color changes correspond to blood volume fluctuations with each heartbeat.

The method involves recording a facial video and selecting regions of interest (ROIs) on the face. 
By analyzing the color channels within these ROIs, it is possible to extract signals that reflect physiological rhythms. 
To isolate the heart rate signal, we can apply independent component analysis (ICA) to separate the source signals and identify the components corresponding to the cardiac pulse.
This component is then processed to estimate the heart rate.
This method has been pioneered by [Poh et al. (2008)](https://doi.org/10.1364/OE.18.010762)

### Implementation

The method involves four major steps: region of interest detection, color signal extraction, independent component analysis, and heart rate estimation.
Let's have a look at each of these.

#### Region of interest detection
The first step is to extract the region that we are interested in from our input image. 
We indeed receive a simple input frame captured by the camera, with a background, maybe other objects, probably your torso, and most importantly... your face.
This is way too much information to be processed, and most of it is not relevant to the task we want to perform.
We will thus first extract the region of the head and apply some masks to remove less interesting regions.
The Haar cascade face classifier is ideal for this.
It allows a computer to very quickly and repeatably extract faces from images.
Check for yourself how Haar cascade classifiers work!

Once the face is extracted from the image, we can go a step further and crop it to a more specific region of interest.
Indeed, we are trying to detect the pulses of your heart by measuring changes in the color of the skin. 
We can thus safely remove the eyes, or maybe only keep the forehead.
Check the complete implementation of this step in the Virtual_PPG_helpers.py file!

#### Color signal extraction
We can now extract a region of interest from one input image. Great! But not enough to analyze heart rate over time.
We know that the region of interest that we extract from the images is lightly pulsing at a certain rate that is correlated to our heart rate.
The next step is to capture this color pulsing in time from a sequence of frames. 
For every new input image that we receive, we will extract the region of interest, then from the region of interest, extract the color values.
To simplify our input even further, we will extract the mean red, green, and blue values of our region of interest.
By doing this, we can create a list of three color values for each time point, giving us our color signal.

#### Independent component analysis
We have now simplified our input stream of images (i.e. our video) to an input stream of three values: mean red, mean green, and mean blue found in the region of interest.
Similar to how the color of our skin captured by a camera is a mix of red, green, and blue, the pulsing signal that we are looking for is spread over the red, green, and blue channels. 
This additional step of independent component analysis will allow us to untangle the color signal into the most interesting pulsating signal and the other ones.
Check for yourself what independent component analysis is and how it works!

#### Heart rate estimation
Following the three previous, we now have three signals representing the change of color in our region of interest over time. 
Let us now identify the signal corresponding to the human heart rate and provide an estimate for the beats per minute of your heart.
We will use a Fourier analysis to extract the frequency that has the highest power in the Fourier spectrum. 
This frequency corresponds to your heart rate (in Hertz).
