from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

def create_reel(image_path, audio_path, output_path, caption_text=""):
    clip_duration = 30  # seconds

    image = ImageClip(image_path).set_duration(clip_duration).resize(height=1080).set_position("center")
    audio = AudioFileClip(audio_path).subclip(0, clip_duration)

    # Add caption text
    if caption_text:
        from moviepy.editor import TextClip
        caption = TextClip(caption_text, fontsize=60, color='white', font="Arial-Bold")
        caption = caption.set_position(("center", "bottom")).set_duration(clip_duration)
        final = CompositeVideoClip([image, caption])
    else:
        final = image

    final = final.set_audio(audio)
    final.write_videofile(output_path, fps=24)
