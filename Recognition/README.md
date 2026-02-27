🇳🇱 Nederlands | [🇬🇧 English](./README_en.md)

# Recognition module

Herken handgebaren en gezichten met behulp van OpenCV en Mediapipe.
In deze module duiken we dieper in de herkenning van mensen in beelden zodat ze kunnen interageren met computers.
We leren begrijpen hoe onze computer menselijke eigenschappen zoals handen en gezichten kan herkennen en hoe we dit kunnen optimaliseren voor real-time interactie.
We bekijken de snelste en krachtigste machine learning modellen die voor deze taken worden gebruikt en leren hoe we een image kunnen verwerken met deze tools.
Wat je met deze resultaten doet, is aan jou.  

### [Gezicht herkenning](./Face/Face_recognition.py)

Train een machine learning model om verschillende personen direct te herkennen.
Onderzoek hoe local binary pattern histograms worden gebruikt om het gezicht van een mens te encoderen en hoe je machine learning modellen kan trainen en gebruiken.  

- Meer informatie: [LBPH](https://www.geeksforgeeks.org/face-recognition-with-local-binary-patterns-lbps-and-opencv/)
  
### [Hand herkenning](./Hand)

Gebruik een state-of-the-art hand detectie en handgebaar herkenningsmodel ontwikkeld door Google.
Onderzoek meer geavanceerde machine learning modellen zoals deep learning en neural networks.  

- Meer informatie: [Hand gestures and landmarks](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python)

### [Diepth predictie](./Depth/depth.py)

Gebruik het state-of-the-art diepte detectie model Depth Anything om een derde dimensie toe te voegen aan je 2D beelden. 
Onderzoek meer geavanceerde machine learning modellen zoals deep learning en neural networks.

Meer informatie: [Depth Anything](https://huggingface.co/docs/transformers/tasks/monocular_depth_estimation)