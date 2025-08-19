# Project EIT - Image processing toolbox

Een verzameling Python modules om image processing te gebruiken in je
project.

## Structuur van de toolbox

### [Detection](https://github.com/vubir-projectEIT/Image_Processing/tree/main/Detection)

Detecteer objecten, kleuren, randen, gezichten, mensen en nog veel meer
met behulp van [OpenCV](https://docs.opencv.org/4.x/). In deze module
verkennen we pure image processing en proberen we dingen te detecteren
in raw images. We bekijken verschillende technieken om vormen, kleuren
of meer complexe features te detecteren in beelden, zodat we programma's
kunnen maken die begrijpen wat ze zien. We leren eenvoudige maar
krachtige technieken die een ingenieur kan gebruiken om een image te
verwerken, en ook complexere tools zoals machine learning models om
moeilijkere taken uit te voeren. Na het verwerken van het beeld kun je
de resultaten verder gebruiken in elke applicatie.

### [Recognition](https://github.com/vubir-projectEIT/Image_Processing/tree/main/Recognition)

Herken handgebaren en gezichten met
[OpenCV](https://docs.opencv.org/4.x/) en
[Mediapipe](https://ai.google.dev/edge/mediapipe/solutions/guide). In
deze module duiken we dieper in de herkenning van mensen in images zodat
ze kunnen interageren met computers. We leren begrijpen hoe onze
computer menselijke eigenschappen zoals handen en gezichten kan
herkennen en hoe we dit kunnen optimaliseren voor real-time interactie.
We bekijken de snelste en krachtigste machine learning models die
hiervoor worden gebruikt en leren hoe we een image kunnen verwerken met
deze tools. Wat je met de resultaten doet, is aan jou.

### [Tracking](https://github.com/vubir-projectEIT/Image_Processing/tree/main/Tracking)

Volg objecten en regio's in images met behulp van
[OpenCV](https://docs.opencv.org/4.x/). In deze module focussen we op
het tracken van de positie van onze objecten in de tijd. We bekijken
geavanceerde methodes om iets belangrijks in het beeld te vinden en het
te blijven volgen zonder het spoor te verliezen. Zodra je objecten
optimaal kunt tracken, kun je hier alles omheen bouwen om een mooi
project te realiseren.

### [Virtual PPG](https://github.com/vubir-projectEIT/Image_Processing/tree/main/VirtualPPG)

Implementeer een real-time virtuele hartslagmeter, ook wel virtual PPG
genoemd, met behulp van [OpenCV](https://docs.opencv.org/4.x/). In deze
module bouwen we een hartslagmeter vanaf nul met image processing tools
en een eenvoudige camera. We gebruiken deze case study om een overzicht
te krijgen van alle stappen die nodig zijn voor image analysis en duiken
dieper in een specifieke toepassing. Wanneer je je hartslag in real-time
kunt meten met je camera, kun je deze biomedische informatie koppelen
aan andere apparaten of applicaties.

## Aan de slag

### De Anaconda environment

Voor deze eerste kennismaking met geavanceerd Python coding, project
management, image processing en machine learning raden we aan de
[Anaconda](https://anaconda.org) environment te gebruiken, een populair
Python data science platform. Development en exploratie worden
eenvoudiger dankzij de verschillende tools die Anaconda aanbiedt.

#### 1. Installeer Anaconda

Als je dit nog niet gedaan hebt, klik dan op de volgende link om
[Anaconda](https://www.anaconda.com/download/success) te downloaden voor
jouw operating system. Volg de [installation
guide](https://docs.anaconda.com/anaconda/install/) en maak je [eerste
Python
programma](https://docs.anaconda.com/anaconda/getting-started/hello-world/)!

[<img width="1728" alt="Screenshot 2024-02-23 at 13 02 22" src="https://github.com/vubir-projectEIT/Image_Processing/assets/152272505/c96af1be-6622-4fca-9b58-d3c694fd112b">](https://www.anaconda.com/download/success)

#### 2. Stel je environment in

De tweede stap is het instellen van je environment zodat je volledige
controle hebt over de code die je uitvoert en de packages die je
installeert. Volg deze stappen om de environment aan te maken en te
activeren die je tijdens het project zal gebruiken.

-   Open je Terminal (MacOS/Linux) of Anaconda Prompt (Windows)

-   Maak je environment aan en installeer Python (dit hoef je maar één
    keer te doen):

``` bash
conda install --name eit python=3.12
```

-   Activeer je environment (dit moet je
    elke keer doen wanneer je de terminal opent):

``` bash
conda activate eit
```

#### 3. Maak een project folder aan

-    MacOS/Linux
  
``` bash
mkdir ~/Desktop/eit
cd ~/Desktop/eit
```

-    Windows
  
``` bash
mkdir %USERPROFILE%\Desktop\eit
cd %USERPROFILE%\Desktop\eit
```

Je bent nu klaar om aan je project te beginnen!

#### 4. Stel je IDE in

Je Python scripts schrijven in een gewone text editor is mogelijk, maar
niet praktisch. Ontwikkelaars gebruiken daarom een Integrated
Development Environment (IDE). Het is sterk aangeraden om in Spyder (of
PyCharm als je dat verkiest) te werken vanuit Anaconda. Volg deze
stappen om Spyder te installeren en te gebruiken in je zojuist
aangemaakte environment.

-   Installeer Spyder:

``` bash
conda install spyder
```

-   Start Spyder:

``` bash
spyder
```

Je bent nu klaar om je eerste script te schrijven!

### Nuttige packages en dependencies

#### 1. Onmisbare imports

Enkele packages zijn onmisbaar voor een ingenieur die met Python
applicaties werkt:

-   [Numpy](https://numpy.org/doc/stable/reference/index.html#reference)
-   [Matplotlib](https://matplotlib.org/stable/users/index) /
    [Seaborn](https://seaborn.pydata.org/index.html)

``` bash
pip install numpy
pip install matplotlib
```

#### 2. OpenCV

[OpenCV (Open Source Computer Vision
Library)](https://docs.opencv.org/4.x/) is een open-source computer
vision en machine learning software library. Het ondersteunt
verschillende programmeertalen zoals Python, Java, C en C++. Wij zullen
echter Python gebruiken voor het grootste deel van onze OpenCV
toepassingen in deze cursus. Voer de volgende command line uit in je
Terminal (MacOS/Linux) of Anaconda Prompt (Windows). Zorg dat je
environment geactiveerd is!

``` bash
pip install opencv-contrib-python==4.9.0.80
```

#### 3. Scikit-learn

[Scikit-learn](https://scikit-learn.org/stable/) is een open-source
machine learning library voor Python. Het bevat een zeer krachtige
verzameling modules die alles aanbieden van model-implementatie tot
pre-processing en post-processing. Voer de volgende command line uit in
je Terminal (MacOS/Linux) of Anaconda Prompt (Windows). Zorg dat je
environment geactiveerd is!

``` bash
conda install scikit-learn
```

#### 4. Mediapipe

[Mediapipe (by
Google)](https://ai.google.dev/edge/mediapipe/solutions/guide) is een
open-source library voor artificial intelligence en machine learning.
Het biedt verschillende cutting-edge getrainde modellen om allerlei
taken efficiënt uit te voeren. Bovendien geeft het de mogelijkheid aan
gevorderde programmeurs om hun modellen te customizen en krachtige
real-time applicaties te draaien. Voer de volgende command line uit in
je Terminal (MacOS/Linux) of Anaconda Prompt (Windows). Zorg dat je
environment geactiveerd is!

``` bash
pip install mediapipe==0.10.18
```
