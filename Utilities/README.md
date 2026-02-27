🇳🇱 Nederlands | [🇬🇧 English](./README_en.md)

# Hulpmiddelen

Deze module biedt een lijst met handige tools die je kunnen helpen tijdens de ontwikkeling van je project.

### [Interactieve kleurfiltering](./Support/ColorThresholdSelector.py)

Dit voorbeeld implementeert een interactieve tool om kleurfilterparameters te bepalen. 
De afbeelding wordt eerst geblurred met een Gaussiaanse kernel en aangepast voor gamma. 
De kleurfiltering is afhankelijk van een lagere en hogere limiet van HSV-waarden die worden gebruikt om de afbeelding te drempelen in de HSV-kleurruimte. 
Het script opent een venster met opties voor:

1. Vervaging → Gaussiaanse grootte (Kernel) en standaardafwijking (Sigma)  
2. Gamma-correctie → Doelwaarde (Gamma) (16 → 1.6)  
3. Lagere en hogere drempels voor HSV-afbeeldingsmaskering binnen [0-255]

- Meer informatie: [Gamma-correctie](https://www.e-consystems.com/blog/camera/technology/what-is-gamma-correction-and-why-is-it-so-crucial-for-embedded-vision-systems/)

### [Multithreading](./Support/Thread.py)

Dit voorbeeld demonstreert multithreading in Python. 
Multithreading is een krachtig hulpmiddel waarmee meerdere taken tegelijk of op de achtergrond kunnen worden uitgevoerd. 
Hierdoor blijft de hoofd-Pythonthread vrij om belangrijk werk te doen, zoals het behouden van de responsiviteit van de gebruikersinterface.

- Meer informatie: [Threading](https://realpython.com/intro-to-python-threading/)

### [ROI-selectie](./Support/SimpleROISelector.py)

In computer vision beschrijft een region of interest (ROI) een deelgebied van een afbeelding in pixelcoördinaten. 
Een ROI wordt meestal weergegeven als een vector met 4 elementen [x, y, w, h], waarbij:

1. [x, y] de pixelcoördinaten van het gebied zijn. Dit kan het midden of een van de hoeken zijn.  
2. [w, h] de breedte en hoogte van het gebied zijn.  

Het selecteren van een ROI is een belangrijk onderdeel van latere beeldverwerkingsstappen, omdat het informatie over de inhoud van de afbeelding en de focus aan een algoritme geeft.
Vaak wordt ROI-selectie ook gebruikt om processing kosten te verminderen. 
OpenCV biedt een ROI-selectie-implementatie voor statische afbeeldingen.
Onze eigen eenvoudige implementatie van een ROI-selector die op live afbeeldingen werkt, is ook beschikbaar.

- Meer informatie: [OpenCV Voorbeelden](https://www.geeksforgeeks.org/python-opencv-selectroi-function/)

### [RealSense-camera's](./RealSenseCamera)

Deze module laat zien hoe je toegang krijgt tot de [RealSense-camera](https://www.realsenseai.com/get-started-depth-camera/) streams en hoe je de afbeeldingen verwerkt. 
De RealSense-camera heeft meerdere sensoren die verschillende weergaven van de wereld geven (RGB, diepte, infrarood).

Om de RealSense-camera's beter te leren kennen, kun je het [Intel RealSense SDK](https://intelrealsense.github.io/librealsense/python_docs/_generated/pyrealsense2.html#module-pyrealsense2) bekijken om te experimenteren met de sensoren en enkele filter- en verwerkingsstappen uit te proberen. 
Toegang tot de camerastream kan handmatig via de [Intel API](https://canvas.vub.be/courses/36046/files/2285191?wrap=1) of via onze [RealSenseCamera](./RealSenseCamera/RealSenseCamera.py) klasse die de setup vereenvoudigt.  

De RealSense-camera's maken geavanceerde beeldverwerking en samenvoeging van sensorkaarten mogelijk. 
De [PointcloudViewer.py](./RealSenseCamera/PointCloudViewer2-1.py) biedt een demo van de camera's en toont ruimtelijke en temporele filtering, decimatie, kleurcodering en belichting.

- Meer informatie: [Voorbeelden](https://github.com/IntelRealSense/librealsense/tree/development/wrappers/python/examples), [Filtering](https://github.com/IntelRealSense/librealsense/blob/jupyter/notebooks/depth_filters.ipynb)

### [Muisevenementen verwerken](./Support/Mouse_paint.py)

Dit voorbeeld illustreert hoe je muisevenementen kunt verwerken en deze kunt gebruiken om objecten op het scherm te tekenen.

### [PyGame-OpenCV intergratie](./Support/PygameOpencv.py)

Dit script laat zien hoe je frames die via je webcam met OpenCV worden ingelezen kunt weergeven op een Pygame display.

### [IP Webcam](./Support/IPWebcam.py)

Heb je een eenvoudige, mobiele camera met hoge resolutie nodig? Zoek niet verder dan in je broekzak. Dit voorbeeld laat zien hoe je je (Android-)telefoon met [IP Webcam](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=fr&pli=1) via OpenCV kunt gebruiken. Voor iOS-gebruikers die MacOS gebruiken: bekijk deze [link](https://support.apple.com/guide/mac-help/use-iphone-as-a-webcam-mchl77879b8a/mac) om te zien hoe je je telefoon als native camera voor je computer kunt gebruiken.

### [Homography](./Support/Homography/Homography.py)

Werk je met vlakke oppervlakken in 3D?
Dit script laat zien hoe je afbeeldingen kunt corrigeren die vervormd zijn door de camerahoek.