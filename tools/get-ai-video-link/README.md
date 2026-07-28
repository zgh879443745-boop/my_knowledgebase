# get-ai-video-link

\u4ece\u6296\u97f3\u5df2\u767b\u5f55\u8d26\u53f7\u7684\u6536\u85cf\u5939\u300cAi\u300d\u4e2d\u81ea\u52a8\u63d0\u53d6\u89c6\u9891\u94fe\u63a5\uff0c\u751f\u6210 JSON + Markdown \u53cc\u683c\u5f0f\u6587\u6863\u3002\u9996\u6b21\u8fd0\u884c\u521b\u5efa\u6587\u6863\uff0c\u540e\u7eed\u8fd0\u884c\u589e\u91cf\u66f4\u65b0\uff0c\u81ea\u52a8\u53bb\u91cd\u9632\u91cd\u3002

## \u529f\u80fd

- \ud83d\udd17 \u81ea\u52a8\u91c7\u96c6\u6296\u97f3\u6536\u85cf\u5939\u300cAi\u300d\u4e2d\u7684\u89c6\u9891\u94fe\u63a5
- \ud83d\udcc4 \u8f93\u51fa JSON + Markdown \u53cc\u683c\u5f0f\u6587\u6863
- \ud83d\udd04 \u589e\u91cf\u66f4\u65b0\uff1a\u5df2\u6709\u6587\u6863\u4e0d\u4f1a\u88ab\u8986\u76d6\uff0c\u4ec5\u8ffd\u52a0\u65b0\u89c6\u9891
- \ud83d\uded1 \u6309 aweme_id \u5168\u5c40\u53bb\u91cd\u9632\u91cd
- \ud83d\udd10 \u5185\u7f6e\u6d4f\u89c8\u5668\u767b\u5f55\u6a21\u5757\uff0c\u65e0\u9700\u5916\u90e8\u4f9d\u8d56

## \u6587\u4ef6\u7ed3\u6784

```
get-ai-video-link/
\u251c\u2500\u2500 SKILL.md                    # \u6280\u80fd\u5b9a\u4e49\u6587\u4ef6
\u251c\u2500\u2500 collect_ai_links.py         # \u4e3b\u811a\u672c - \u94fe\u63a5\u91c7\u96c6
\u251c\u2500\u2500 browser_login.py            # \u767b\u5f55\u6a21\u5757 - \u6d4f\u89c8\u5668\u767b\u5f55/\u72b6\u6001/\u767b\u51fa
\u251c\u2500\u2500 config.example.py           # \u914d\u7f6e\u793a\u4f8b
\u251c\u2500\u2500 config.py                   # \u7528\u6237\u914d\u7f6e\uff08\u4e0d\u63d0\u4ea4\uff09
\u251c\u2500\u2500 requirements.txt            # Python \u4f9d\u8d56
\u2514\u2500\u2500 README.md                   # \u672c\u6587\u4ef6
```

## \u5b89\u88c5

### 1. \u521b\u5efa venv \u5e76\u5b89\u88c5\u4f9d\u8d56

```powershell
cd D:\my_knowledgebase\tools\get-ai-video-link
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. \u914d\u7f6e

\u590d\u5236 `config.example.py` \u4e3a `config.py`\uff0c\u4fee\u6539\u4ee5\u4e0b\u914d\u7f6e\uff1a

```python
COLLECTS_ID = "7610341807192299291"  # \u6296\u97f3\u6536\u85cf\u5939 Ai \u7684 ID
OUTPUT_DIR = Path("D:/my_knowledgebase/personal/notes")  # \u8f93\u51fa\u76ee\u5f55
```

\u5982\u679c\u5df2\u901a\u8fc7 douyin-favorites-to-knowledge \u767b\u5f55\u8fc7\uff0c\u53ef\u590d\u7528\u5176 profile\uff1a

```python
BROWSER_PROFILE_DIR = Path("C:/Users/\u4f60\u7684\u7528\u6237\u540d/AppData/Local/douyin-favorites-to-knowledge/browser-profile")
```

### 3. \u767b\u5f55\u6296\u97f3

```powershell
python browser_login.py login
```

## \u4f7f\u7528

### \u547d\u4ee4\u884c

```powershell
# \u9ed8\u8ba4\u91c7\u96c6 100 \u6761
python collect_ai_links.py

# \u6307\u5b9a\u6570\u91cf
python collect_ai_links.py --max 200

# \u5148\u767b\u5f55\u518d\u91c7\u96c6
python collect_ai_links.py --login

# \u68c0\u67e5\u767b\u5f55\u72b6\u6001
python browser_login.py status

# \u767b\u51fa
python browser_login.py logout
```

### \u8f93\u51fa\u6587\u4ef6

| \u6587\u4ef6 | \u8def\u5f84 | \u8bf4\u660e |
|------|------|------|
| JSON | `D:/my_knowledgebase/personal/notes/douyin-ai-favorites-links.json` | `[{index, aweme_id, title, author, url}]` |
| MD | `D:/my_knowledgebase/personal/notes/douyin-ai-favorites.md` | \u5e26\u5143\u6570\u636e\u3001\u94fe\u63a5\u5217\u8868\u3001\u7edf\u8ba1\u4fe1\u606f |

## \u8fd0\u884c\u6d41\u7a0b

1. \u68c0\u67e5\u767b\u5f55\u72b6\u6001\uff0c\u672a\u767b\u5f55\u5219\u62a5\u9519
2. \u52a0\u8f7d\u5df2\u6709 JSON \u6587\u6863\uff0c\u6784\u5efa aweme_id \u2192 item \u6620\u5c04
3. \u8c03\u7528\u6296\u97f3 `collects/video/list` API \u5206\u9875\u91c7\u96c6
4. \u6309 aweme_id \u53bb\u91cd\u5408\u5e76\uff0c\u65b0\u89c6\u9891\u8ffd\u52a0\u5230\u5217\u8868\u672b\u5c3e
5. \u5199\u5165 JSON + Markdown \u53cc\u683c\u5f0f\u6587\u6863
6. \u8f93\u51fa `__RESULT__` JSON \u5757\uff1a`{total, new, json, md}`

## \u53bb\u91cd\u4e0e\u9632\u91cd

- \u53bb\u91cd\u952e\uff1a`aweme_id`\uff08\u6296\u97f3\u89c6\u9891\u552f\u4e00\u6807\u8bc6\uff09
- JSON \u4e3a\u552f\u4e00\u6570\u636e\u6e90\uff08Single Source of Truth\uff09
- \u5df2\u6709\u6570\u636e\u4e0d\u4f1a\u88ab\u8986\u76d6\uff0c\u65b0\u6570\u636e\u4ec5\u8ffd\u52a0
- \u6bcf\u4e2a aweme_id \u5bf9\u5e94 `https://www.douyin.com/video/{aweme_id}`

## \u4e0e douyin-to-obsidian \u7684\u8854\u63a5

JSON \u4e2d\u6bcf\u6761\u8bb0\u5f55\u542b `url` \u5b57\u6bb5\uff0c\u53ef\u76f4\u63a5\u4f20\u5165\u4e0b\u6e38 skill\uff1a

```powershell
py -3.10 D:\my_knowledgebase\tools\douyin-to-obsidian\douyin_to_obsidian.py --link "https://www.douyin.com/video/7665634161000009014" --target personal
```

## \u6545\u969c\u6392\u9664

| \u95ee\u9898 | \u89e3\u51b3\u65b9\u6848 |
|------|---------|
| \u672a\u767b\u5f55 | \u8fd0\u884c `python browser_login.py login` |
| Playwright \u672a\u5b89\u88c5 | `pip install playwright && playwright install chromium` |
| API \u72b6\u6001\u7801\u975e 0 | \u68c0\u67e5 collects_id \u662f\u5426\u53d8\u5316\uff08\u6296\u97f3\u53ef\u80fd\u66f4\u6362 ID\uff09 |
| \u65e0\u65b0\u589e | \u6b63\u5e38\uff0c\u62a5\u544a `new=0` |
| \u627e\u4e0d\u5230\u6d4f\u89c8\u5668 | \u5b89\u88c5 Chrome \u6216 Edge |

## License

MIT
