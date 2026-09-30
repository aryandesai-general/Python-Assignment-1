"""Q8: Build/search a token index, pickle it, and archive logs plus index.

BUILD usage through stdin: BUILD <folder_path> <archive.zip>
SEARCH usage through stdin: SEARCH <index.pkl> <number_of_queries>, followed by tokens.
"""
import os
import pickle
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


TOKEN_RE = re.compile(r"\b[\w.-]+\b", re.UNICODE)


def build_index(folder):
    index = defaultdict(list)
    file_count = 0
    line_count = 0
    for path in sorted(Path(folder).rglob("*")):
        if not path.is_file():
            continue
        file_count += 1
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for number, line in enumerate(handle, 1):
                    line_count += 1
                    for token in TOKEN_RE.findall(line.casefold()):
                        index[token].append((str(path), number))
        except OSError as exc:
            print(f"Warning: skipped {path}: {exc}", file=sys.stderr)
    return dict(index), file_count, line_count


def main():
    first = sys.stdin.readline().strip().split(maxsplit=2)
    if not first:
        print("Invalid input.")
        return

    mode = first[0].upper()
    if mode == "BUILD" and len(first) == 3:
        folder, archive_name = first[1], first[2]
        if not Path(folder).is_dir():
            print("Folder not found.")
            return
        index, file_count, line_count = build_index(folder)
        archive_path = Path(archive_name)
        index_path = archive_path.with_suffix(".pkl")
        with index_path.open("wb") as handle:
            pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(Path(folder).rglob("*")):
                if path.is_file():
                    archive.write(path, arcname=str(Path("logs") / path.relative_to(folder)))
            archive.write(index_path, arcname=index_path.name)
        print(f"FILES {file_count}")
        print(f"LINES {line_count}")
        print(f"TOKENS {len(index)}")
    elif mode == "SEARCH" and len(first) == 3:
        index_path, query_count = first[1], int(first[2])
        with open(index_path, "rb") as handle:
            index = pickle.load(handle)
        for _ in range(query_count):
            token = sys.stdin.readline().strip().casefold()
            matches = index.get(token, [])
            print(f"{token}:", *(f"{filename}:{line}" for filename, line in matches))
    else:
        print("Invalid command. Use BUILD folder archive.zip or SEARCH index.pkl q.")


if __name__ == "__main__":
    main()
