"""
抖音转Obsidian配置文件
"""
from pathlib import Path
import os
import sys

OBSIDIAN_PATH = Path("D:/my_knowledgebase")

TEMP_PATH = Path("D:/my_knowledgebase/skills/douyin-to-obsidian/douyin_temp")

DEFAULT_CATEGORY = "产品资讯"

WHISPER_MODEL = "base"

PYTHON_PATH = sys.executable

TEMP_PATH.mkdir(parents=True, exist_ok=True)

def setup_ffmpeg():
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = Path(ffmpeg_path).parent
        os.environ['PATH'] = str(ffmpeg_dir) + os.pathsep + os.environ['PATH']
        return True
    except:
        print("警告: 无法自动配置 FFmpeg")
        return False

setup_ffmpeg()
