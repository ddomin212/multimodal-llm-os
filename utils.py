from pytube import YouTube
from gradio_client import Client
from hugchat import hugchat
from hugchat.login import Login

def download_video(url):
    """First we dwnload the video from YouTube, then we return the path to the video file."""
    youtube = YouTube(url)
    video = youtube.streams.filter(res="720p").first()
    outname = url.split("/")[-1]
    video.download(output_path="./videos", filename=f"{outname}.mp4")
    return f"./videos/{outname}.mp4"

def call_video_llama(path):
    """
    Next we call the video llama model to get a description of the video. The image is a placeholder,
    the API is a bit shit so it can't be run without the image, but it's free.
    """
    client = Client("https://languagebind-video-llava.hf.space/")
    result = client.predict(
        "https://t3.ftcdn.net/jpg/04/63/51/28/360_F_463512856_GEk2IrQkYatpRVR9YDhiZgRY2z00Zet3.jpg",
        path,	# str (filepath or URL to file) in 'Input Video' Video component
        "What background music would you recommend for this video? Describe it in detail.",	# str in 'parameter_0' Textbox component
        fn_index=3
    )
    return result

def call_text_llama(video_desc, email, passwd):
    """
    We call llama-70b model from huggingface chat to 
    preprocess the video context into a prompt for music.
    """
    sign = Login(email, passwd)
    cookies = sign.login()

    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    query_result = chatbot.query(f"""You are an expert on short form content. 
                                 You know exactly which music to use to make 
                                 a video a viral success. By the description of this video {video_desc}
                                 what music would you recommend? Be as specific as possible, including
                                 notes, tempo, genre, instruments and other details. Here is an example of how to describe a song:
                                 'This techno song features a synth lead playing the main melody. This is accompanied by programmed percussion playing a simple kick focused beat. The hi-hat is accented in an open position on the 3-and count of every bar. The synth plays the bass part with a voicing that sounds like a cello. This techno song can be played in a club. The chord sequence is Gm, A7, Eb, Bb, C, F, Gm. The beat counts to 2. The tempo of this song is 128.0 beats per minute. The key of this song is G minor.'""")

    return str(query_result)

def generate_music(prompt):
    """
    Finally we call the Mustango model to generate the music via a prompt. The final audio gets saved as a temp file.
    """
    from gradio_client import Client

    client = Client("https://declare-lab-mustango.hf.space/--replicas/j7l76/")
    result = client.predict(
            prompt,	# str  in 'Prompt' Textbox component
            200,	# float (numeric value between 100 and 200) in 'Steps' Slider component
            3,	# float (numeric value between 1 and 10) in 'Guidance Scale' Slider component
            api_name="/predict"
    )
    return result