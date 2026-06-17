"""
引用溯源：验证 L1 卡片中的引用是否真实出现在素材中。
不是检查"有没有引用"——是检查"引用内容是否真实"。

用法: python factcheck.py [卡片文件] [素材目录]
      python factcheck.py cards/安全边际.md raw/buffett/

输出: 每条引用 → 在素材中搜到的行号 or ❌ 未找到
"""

import sys, os, re, glob

def extract_quotes(card_path):
    """从卡片中提取所有 > 引用"""
    with open(card_path, 'r', encoding='utf-8') as f:
        content = f.read()
    quotes = re.findall(r'^>\s*[""](.+?)[""]', content, re.MULTILINE)
    quotes += re.findall(r'^>\s*(.+?)(?:（|——|$)', content, re.MULTILINE)
    return [q.strip() for q in quotes if len(q.strip()) > 20]

def search_in_sources(quote, source_dir):
    """在素材目录中搜索引用片段（排除卡片本身）"""
    keyword = quote[:20]
    results = []
    for ext in ['*.md', '*.html', '*.txt']:
        for f in glob.glob(f"{source_dir}/**/{ext}", recursive=True):
            # 跳过卡片本身和项目笔记（它们是产物，不是素材）
            if 'cards' in f or 'notes' in f or 'cognition' in f:
                continue
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
                    lines = fh.readlines()
                for i, line in enumerate(lines, 1):
                    if keyword in line:
                        results.append((f, i, line.strip()[:100]))
                        if len(results) >= 3:
                            return results
            except:
                pass
    return results

def main():
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    card = sys.argv[1] if len(sys.argv) > 1 else None
    source_dir = sys.argv[2] if len(sys.argv) > 2 else "raw/buffett/"

    if not card:
        print("用法: python factcheck.py [卡片文件] [素材目录]")
        return

    quotes = extract_quotes(card)
    print(f"\n检查 {card}: {len(quotes)} 条引用\n")

    verified = 0
    unverified = 0

    for q in quotes:
        matches = search_in_sources(q, source_dir)
        if matches:
            verified += 1
            print(f"  ✅ [{matches[0][0].split('/')[-1]}:L{matches[0][1]}] {q[:60]}...")
        else:
            unverified += 1
            print(f"  ❌ 未找到匹配: {q[:60]}...")

    print(f"\n结果: {verified}✅ / {unverified}❌ / {len(quotes)}")

if __name__ == "__main__":
    main()
