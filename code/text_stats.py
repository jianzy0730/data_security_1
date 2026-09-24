"""统计文本文件中的单词频次，并输出出现次数最多的 10 个单词。"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


# 匹配 Unicode 单词字符，同时排除下划线。
WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def configure_output_encoding() -> None:
    """尽量使用 UTF-8 输出，避免 Windows 控制台显示中文乱码。"""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def count_words(file_path: Path) -> Counter[str]:
    """读取文本文件并返回单词频次。"""
    text = file_path.read_text(encoding="utf-8")
    words = (word.casefold() for word in WORD_PATTERN.findall(text))
    return Counter(words)


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="统计 txt 文件中的单词频次")
    parser.add_argument("file", nargs="?", help="要统计的 txt 文件路径")
    return parser.parse_args()


def main() -> int:
    """程序入口。"""
    configure_output_encoding()
    args = parse_args()
    file_name = args.file or input("请输入 txt 文件路径：").strip()

    if not file_name:
        print("错误：未提供文件路径。", file=sys.stderr)
        return 1

    file_path = Path(file_name)
    if not file_path.is_file():
        print(f"错误：文件不存在：{file_path}", file=sys.stderr)
        return 1

    try:
        word_counts = count_words(file_path)
    except UnicodeDecodeError:
        print("错误：文件不是 UTF-8 编码，暂无法读取。", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"错误：无法读取文件：{exc}", file=sys.stderr)
        return 1

    print("排名\t单词\t次数")
    for rank, (word, count) in enumerate(
        sorted(word_counts.items(), key=lambda item: (-item[1], item[0]))[:10],
        start=1,
    ):
        print(f"{rank}\t{word}\t{count}")

    if not word_counts:
        print("文件中没有找到单词。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
