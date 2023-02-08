# speech-to-text-demo

## Installation
``` 
conda create -n speech2text python
conda activate speech2text
cd speech-to-text-demo
pip install -r requirements.txt
```

## How to run?
**Google cloud API key is necessary for this code to run. Please place your google.json file containing the API key in the folder (speech-to-text-demo) before running the following steps.**

* export GOOGLE_APPLICATION_CREDENTIALS=</path/to/google.json>
* python server.py

This will give a link: eg: http://127.0.0.1:8080
Or any other port that you mention in line 131 in server.py


