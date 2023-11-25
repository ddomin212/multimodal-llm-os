import streamlit as st
from utils import download_video, call_video_llama, generate_music, call_text_llama
import subprocess
import sys

def fix_gradio_lib():
    print(sys.path[-1])
    subprocess.run(["cp", "gradio_replace/serializing.py", f"{sys.path[-1]}/gradio_client/serializing.py"])
    subprocess.run(["cp", "gradio_replace/utils.py", f"{sys.path[-1]}/gradio_client/utils.py"])

def main():
    st.title("Let AI generate music for your YouTube Shorts!")
    st.markdown("disclaimer: it sucks and it's only 10 seconds long, its still cool tho")
    url = st.text_input("Enter YouTube Short URL")
    if url:
        video_filename = download_video(url)
        st.info(f"Video downloaded successfully: {video_filename}")
        with st.expander("Log In to HuggingFace"):
            email = st.text_input("Email")
            passwd = st.text_input("Password", type="password")
            if st.button("Log In"):
                with st.spinner("Generating music..."):
                    video_desc = call_video_llama(video_filename)
                    st.info("Fetched video")
                    music_prompt = call_text_llama(video_desc, email, passwd)
                    st.info("Fetched music prompt")
                    music_file_path = generate_music(music_prompt)
                if music_file_path:
                    st.audio(music_file_path, format="audio/wav")
                else:
                    st.error("Something went wrong, please try again.")

if __name__ == "__main__":
    fix_gradio_lib()

    st.set_page_config(
        page_title="gen_outdated_music.ai",
        page_icon="🎶",
        layout="wide",
    )
    main()