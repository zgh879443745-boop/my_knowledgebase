import sys
import os

# 添加 ffmpeg 路径
ffmpeg_path = r"C:\Users\v_qqghzhang\ffmpeg\ffmpeg-8.1.1-essentials_build\bin"
os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ.get("PATH", "")

import whisper

print("Whisper 就绪，开始加载模型...", flush=True)
model = whisper.load_model("base")
print("模型加载完成，开始识别音频...", flush=True)

audio_path = r"D:\my_knowledgebase\skills\douyin-to-obsidian\temp\7623675448022617386.mp3"
result = model.transcribe(audio_path, language="zh")
print("识别完成！", flush=True)
print("=== 识别结果 ===")
print(result["text"])
print("=== 结束 ===")
