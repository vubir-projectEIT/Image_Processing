[🇳🇱 Nederlands](./README.md) | 🇬🇧 English

# Project EIT - Image processing toolbox

A set of Python modules to use image processing in your project.

## Structure of the toolbox

### [Detection](./Detection)

Detect objects, colors, edges, faces, people, and much more using [OpenCV](https://docs.opencv.org/4.x/). In this module, we will explore pure image processing and attempt to detect stuff in raw images. We will look at different techniques to detect shapes, colors, or more complex features in images to create programs that can understand what they see. We will learn simple but very powerful techniques that an engineer can use to process an image and more complex tools, like machine learning models, to perform more difficult tasks. After the image is processed, you can use the results further in any application.

### [Recognition](./Recognition)

Recognize hand gestures and faces using [OpenCV](https://docs.opencv.org/4.x/) and [Mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide). In this module, we dive deeper into the recognition of humans in images so that they can interact with computers. We will understand how our computer can understand human attributes like hands and faces and how we can optimize this to interact with our computer in real-time. We will look at the fastest and most powerful machine-learning models that are used for these tasks and learn how to process an image using those tools. What we can do with these results is up to you.

### [Tracking](./Tracking)

Track objects and regions of images using [OpenCV](https://docs.opencv.org/4.x/). In this module, we will focus on tracking the position of our objects in our image in time. We will check advanced methods to find something important in the image and keep following it without losing its trail. Once you can track objects optimally, you can build anything around this to create a nice project.

### [Virtual PPG](./VirtualPPG)

Implement a real-time virtual heart rate sensor, also called virtual PPG, using [OpenCV](https://docs.opencv.org/4.x/). In this module, we implement a heart rate sensor from scratch using image processing tools and a simple camera. We will use this case study to get an overview of all the steps required to do image analysis and dive deep into a specific application. When you are able to measure your heart rate in real-time using your camera, you can connect this biomedical information to any other device or application. 

## Get started

### The Anaconda environment

For this first encounter with advanced Python coding, project management, image processing, and machine learning, we advise you to use the [Anaconda](https://anaconda.org) environment, a popular Python data science platform. Development and exploration are made easy thanks to the different tools provided by Anaconda.

#### 1. Install Anaconda

If not done yet, click on the following link to download [Anaconda](https://www.anaconda.com/download/success) for your operating system. Follow the [installation guide](https://docs.anaconda.com/anaconda/install/) and create your [first Python program](https://docs.anaconda.com/anaconda/getting-started/hello-world/)!

[<img src="https://github.com/vubir-projectEIT/Image_Processing/assets/152272505/c96af1be-6622-4fca-9b58-d3c694fd112b" style="width:100%;">](https://www.anaconda.com/download/success)


#### 2. Setup your environment

The second step will be to set up your environment to have full control over the code that you run and the packages that you install. Follow the following steps to create and activate the environment that you will use during the project.

- Open your Terminal (MacOS/Linux) or Anaconda Prompt (Windows)

<img src="https://github.com/user-attachments/assets/3341ce6a-4e53-4487-ac91-083b2707e310" style="width:67%;">
<img src="https://github.com/user-attachments/assets/639be456-f9f2-42a9-be72-f0b8839405d3" style="width:32%;">


- Create your environment and install Python (you only need to do this once):

``` bash
conda create --name eit python=3.12 spyder jupyter
```

- Activate your environment (you have to do this every time you open your terminal):

``` bash
conda activate eit
```

Developing your Python scripts in your text editor is possible but very impractical. Developers instead use Integrate Developers Environments, or IDE for short. It is strongly recommended to work in Spyder (or PyCharm if you prefer) from inside Anaconda. Jupyter notebooks are also nice for following tutorials. If you check 

- Run Spyder:

``` bash
spyder
```

- Run Jupyter Notebook:

``` bash
jupyter notebook
```

You are now ready to write your first script!


#### 3. Useful packages and dependencies

Here follows the command to install all dependencies. Under that, you can find more information about the packages.

``` bash
pip install numpy==1.26.4 matplotlib==3.10.5 opencv-contrib-python==4.11.0.86 scikit-learn==1.6.1 mediapipe==0.10.21
```

##### 1. Usual imports

Several packages are a must for an engineer when developing any kind of Python application:

- [Numpy](https://numpy.org/doc/stable/reference/index.html#reference)
- [Matplotlib](https://matplotlib.org/stable/users/index) / [Seaborn](https://seaborn.pydata.org/index.html)

``` bash
pip install numpy==1.26.4
pip install matplotlib==3.10.5
```

##### 2. OpenCV

[OpenCV (Open Source Computer Vision Library)](https://docs.opencv.org/4.x/) is an open-source computer vision and machine learning software library. It supports several programming languages, such as Python, Java, C, and C++.  We will, however, be using Python for most of our openCV applications in this course. Run the following command line in your Terminal (MacOS/Linux) or Anaconda Prompt (Windows). Make sure that your environment is activated!

``` bash
pip install opencv-contrib-python==4.11.0.86
```

##### 3. Scikit-learn

[Scikit-learn](https://scikit-learn.org/stable/) is an open-source machine learning libarary for Python. It is a very powerful combination of modules that range from the implemention of all kinds of models, to pre-processing and post-processing. Run the following command line in your Terminal (MacOS/Linux) or Anaconda Prompt (Windows). Make sure that your environment is activated!

``` bash
pip install scikit-learn==1.6.1
```

##### 4. Mediapipe

[Mediapipe (by Google)](https://ai.google.dev/edge/mediapipe/solutions/guide) is an open-source library for artificial intelligence and machine learning. It proposes several cutting-edge trained models to perform all kinds of tasks in an efficient way. Additionally, it provides the possibility for advanced programmers to customize their models to run powerful real-time applications. Run the following command line in your Terminal (MacOS/Linux) or Anaconda Prompt (Windows). Make sure that your environment is activated!

``` bash
pip install mediapipe==0.10.21
```
