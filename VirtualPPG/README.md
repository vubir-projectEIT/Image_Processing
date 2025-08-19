🇳🇱 Nederlands | [🇬🇧 English](./README_en.md)

# Virtual PPG

Implementeer een real-time virtuele hartslagmeter, ook wel virtual PPG genoemd, met behulp van OpenCV.
In deze module bouwen we een hartslagmeter vanaf nul met image processing tools en een eenvoudige camera.
We gebruiken deze case study om een overzicht te krijgen van alle stappen die nodig zijn voor image analysis en duiken dieper in een specifieke toepassing.
Wanneer je je hartslag in real-time kan meten met je camera, kan je deze biomedische informatie koppelen aan eender welk ander apparaat of applicatie.  

We voorzien je van een template [Virtual_PPG_template.py](https://github.com/vubir-projectEIT/Image_Processing/blob/main/VirtualPPG/Virtual_PPG_template.py) en enkele helperfuncties [Virtual_PPG_helpers.py](https://github.com/vubir-projectEIT/Image_Processing/blob/main/VirtualPPG/Virtual_PPG_helpers.py) om je op weg te helpen.
Laten we starten met het idee achter de virtuele PPG en een klein overzicht van wat we willen bereiken.  

### Hoe werkt het?

Virtuele hartslagmeting met een camera, ook bekend als virtuele photoplethysmografie, is een non-contact methode die de hartslag schat door subtiele kleurvariaties in de gezichtshuid te analyseren die via video worden vastgelegd.
Deze kleurveranderingen komen overeen met fluctuaties in het bloedvolume bij elke hartslag.

De methode bestaat uit het opnemen van een gezichts-video en het selecteren van regions of interest (ROIs) op het gezicht.
Door de kleurkanalen binnen deze ROIs te analyseren, is het mogelijk signalen te extraheren die fysiologische ritmes weerspiegelen.
Om het hartslagsignaal te isoleren, kunnen we independent component analysis (ICA) toepassen om de bronsignalen te scheiden en de componenten te identificeren die overeenkomen met de hartslag.
Deze component wordt vervolgens verwerkt om de hartslag te schatten.
Deze methode werd geïntroduceerd door [Poh et al. (2008)](https://doi.org/10.1364/OE.18.010762).  

### Implementatie

De methode omvat vier fasen: detectie van de regio van interesse, extractie van het kleursignaal, independent component analysis en hartslagschatting.
Laten we elk van deze bekijken.

#### Detectie van de regio van interesse

De eerste stap is het extraheren van de regio die ons interesseert uit de input image. 
We krijgen immers een eenvoudig frame van de camera, met achtergrond, mogelijk andere objecten, waarschijnlijk je torso, en het belangrijkste... je gezicht.
Dit is veel te veel informatie om te verwerken, en het meeste is niet relevant voor de taak die we willen uitvoeren.
Daarom extraheren we eerst de regio van het hoofd en passen we maskers toe om minder interessante gebieden te verwijderen.
De Haar cascade face classifier is hier ideaal voor.  
Deze laat een computer snel en betrouwbaar gezichten uit beelden halen.  
Ontdek [hier](https://github.com/vubir-projectEIT/Image_Processing/tree/main/Detection/Eye_and_face) zelf hoe Haar cascade classifiers werken!  

Wanneer het gezicht uit het beeld is gehaald, kunnen we nog een stap verder gaan en het croppen tot een specifiekere regio van interesse.
We proberen immers de hartslagen te detecteren door veranderingen in de huidskleur te meten.
We kunnen dus gerust de ogen weglaten, of enkel het voorhoofd behouden.
Bekijk de volledige implementatie van deze stap in het bestand *Virtual_PPG_helpers.py*!  

#### Extractie van het kleursignaal

We kunnen nu een regio van interesse extraheren uit één input image. Mooi! Maar dit is niet genoeg om de hartslag in de tijd te analyseren.
We weten dat de regio van interesse die we uit de beelden halen, licht pulseert aan een tempo dat gecorreleerd is aan onze hartslag.
De volgende stap is dus om dit kleurpulseren in de tijd vast te leggen via een reeks frames.
Voor elk nieuw input beeld dat we ontvangen, extraheren we de regio van interesse en halen we de kleurwaarden eruit.
Om onze input nog verder te vereenvoudigen, nemen we het gemiddelde van de rode, groene en blauwe waarden in onze regio van interesse.
Zo verkrijgen we een lijst van drie kleurwaarden per tijdstip, wat ons kleursignaal oplevert.  

#### Independent component analysis

We hebben onze input stream van images (video) nu vereenvoudigd tot een stream van drie waarden: gemiddelde rood, groen en blauw in de regio van interesse.
Net zoals de huidskleur die door een camera wordt vastgelegd een mix is van rood, groen en blauw, is ook het pulserende signaal dat we zoeken verspreid over deze drie kanalen.
Met deze extra stap van independent component analysis kunnen we het kleursignaal ontwarren in het meest interessante pulssignaal en de andere signalen.
Ontdek [hier](https://www.geeksforgeeks.org/machine-learning/ml-independent-component-analysis/) zelf wat independent component analysis is en hoe het werkt!  

#### Hartslagschatting

Na de drie vorige stappen hebben we nu drie signalen die de kleurverandering in de regio van interesse over tijd weergeven.
Nu identificeren we het signaal dat overeenkomt met de menselijke hartslag en schatten we het aantal slagen per minuut van je hart.
We gebruiken Fourier analyse om de frequentie te extraheren die de hoogste piek heeft in het Fourier spectrum.
Deze frequentie komt overeen met je hartslag (in Hertz).  
