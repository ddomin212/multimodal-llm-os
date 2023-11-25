### App
A simple app that takes in a youtube short link, uses LLaVA to process what happens in the video, then uses Llama-70b to generate a song description based on the video. The song is then transformed using the Mustango model. The app is subpar at the moment, but the idea has some future.

### Usage
- run `python -m venv env` to create a separate virtual enviroment, then `source env/bin/activate` to activate it
- run `pip install -r requirements.txt` to install the requirements
- run `steamlit run app.py` to run the app, hosted on `http://localhost:8501/`

### Credits
LLaVA: https://paperswithcode.com/paper/video-llava-learning-united-visual-1
Mustango: https://paperswithcode.com/paper/mustango-toward-controllable-text-to-music
Llama2: https://ai.meta.com/llama/