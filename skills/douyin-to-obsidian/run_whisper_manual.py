#!/usr/bin/env python3
"""
手动运行 Whisper 识别音频
"""
import sys
import json
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

AUDIO_PATH = Path(r"D:\my_knowledgebase\skills\douyin-to-obsidian\temp\7623675448022617386.mp3")
OUTPUT_JSON = Path(r"D:\my_knowledgebase\skills\douyin-to-obsidian\temp\whisper_result.json")

def main():
    print("=" * 60)
    print("  手动运行 Whisper 语音识别")
    print("=" * 60)
    
    if not AUDIO_PATH.exists():
        print(f"❌ 音频文件不存在: {AUDIO_PATH}")
        sys.exit(1)
    
    print(f"🎧 音频文件: {AUDIO_PATH}")
    print(f"📊 文件大小: {AUDIO_PATH.stat().st_size / 1024 / 1024:.2f} MB")
    
    try:
        import whisper
        
        model_name = "base"  # 与 config.py 中配置一致
        print(f"\n🔄 加载 Whisper 模型: {model_name}")
        model = whisper.load_model(model_name)
        
        print(f"🎙️  开始识别音频...")
        result = model.transcribe(str(AUDIO_PATH), language='zh')
        
        text = result['text']
        print(f"✅ 识别完成，共 {len(text)} 字")
        
        # 保存到 JSON
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump({"text": text}, f, ensure_ascii=False)
        
        print(f"💾 识别结果已保存: {OUTPUT_JSON}")
        
        # 打印前 500 字符
        print("\n" + "=" * 60)
        print("  识别结果预览（前 500 字）")
        print("=" * 60)
        print(text[:500] + ("..." if len(text) > 500 else ""))
        print("=" * 60)
        
        return text
        
    except Exception as e:
        print(f"❌ 识别失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
