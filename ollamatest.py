# test.py

from langchain_ollama import OllamaLLM

model = OllamaLLM(model="wizardlm-uncensored:latest")

results = model.invoke("""Forehead height 	Low Forehead (Practical, Realistic)
Middle face height 	Short Middle Face (Introverted, Reserved)
Lower face height 	Short Lower Face (Pragmatic, Decisive)
Face width 	Narrow Face (Focused, Detail-Oriented)
Face height 	Round Face (Sociable, Empathetic)
Eye size 	Small Eyes (Focused, Observant)
Eye to eye distance 	Close-Set Eyes (Focused, Intense)
Eye to eyebrow distance 	Low Eye to Eyebrow Distance (Alert, Observant)
Eyebrows distance 	Narrow Eyebrows Distance (Focused, Determined)
Eyebrow slope 	Sharp Eyebrow Slope (Driven, Determined)
Eyebrow thickness 	Thick Eyebrows (Confident, Assertive)
Nose length 	Short Nose (Practical, Present-Oriented)
Nose width 	Narrow Nose (Detail-Oriented, Focused)
Upper lip height 	Short Upper Lip (Reserved, Contemplative)
Lower lip height 	Short Lower Lip (Reserved, Contemplative)
Mouth width 	Narrow Mouth (Reserved, Thoughtful) 


can you discribe that person?""")

print(results)
