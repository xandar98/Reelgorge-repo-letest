import io
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip
import tempfile, os

def create_reel(img_bytes: bytes, prompt: str) -> bytes:
    # prepare base image
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB").resize((720, 1280))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    text_x, text_y = 30, 1100
    draw.text((text_x, text_y), prompt, fill="white", font=font)

    # save frame temporarily
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        img.save(tmp_img.name)
        frame_path = tmp_img.name

    # create video with moviepy
    clip = ImageClip(frame_path).set_duration(6)
    music_path = os.path.join("music", "lofi.mp3")
    if os.path.exists(music_path) and os.path.getsize(music_path) > 0:
        audio = AudioFileClip(music_path).subclip(0, 6)
        clip = clip.set_audio(audio)
    # write result to bytes
    tmp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    clip.write_videofile(tmp_video.name, codec="libx264", fps=24, audio_codec="aac", verbose=False, logger=None)
    clip.close()

    with open(tmp_video.name, "rb") as f:
        video_bytes = f.read()

    # cleanup
    os.remove(frame_path)
    os.remove(tmp_video.name)
    return video_bytes
