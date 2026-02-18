from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


#DIR_1_NAME = "01_all_seasons_utf_8"
DIR_1_NAME = "../../cl_st1_ph1_marcia/corpus/01_all_seasons_utf_8"
DIR_2_NAME = "01_all_seasons_utf_8_straight"
REPORT_NAME = "02_all_seasons_check_report.txt"

DIR_1_SUFFIX = ".txt"
DIR_2_SUFFIX = ".straight.txt"


@dataclass(frozen=True)
class FileInfo:
    path: Path
    size_bytes: int
    sha256: str


def sha256_of_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def build_fileinfo(path: Path) -> FileInfo:
    stat = path.stat()
    return FileInfo(path=path, size_bytes=stat.st_size, sha256=sha256_of_file(path))


def list_files_with_suffix(directory: Path, suffix: str) -> list[Path]:
    return sorted([p for p in directory.iterdir() if p.is_file() and p.name.endswith(suffix)])


def base_name_from_dir1(filename: str) -> str:
    # "Amy_Season_3.txt" -> "Amy_Season_3"
    if not filename.endswith(DIR_1_SUFFIX):
        raise ValueError(f"Unexpected Directory 1 filename (expected *{DIR_1_SUFFIX}): {filename}")
    return filename[: -len(DIR_1_SUFFIX)]


def expected_dir2_filename(base_name: str) -> str:
    # "Amy_Season_3" -> "Amy_Season_3.straight.txt"
    return f"{base_name}{DIR_2_SUFFIX}"


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    dir1 = script_dir / DIR_1_NAME
    dir2 = script_dir / DIR_2_NAME
    report_path = script_dir / REPORT_NAME

    if not dir1.exists() or not dir1.is_dir():
        raise FileNotFoundError(f"Directory 1 not found: {dir1}")
    if not dir2.exists() or not dir2.is_dir():
        raise FileNotFoundError(f"Directory 2 not found: {dir2}")

    dir1_files = list_files_with_suffix(dir1, DIR_1_SUFFIX)
    dir2_files = list_files_with_suffix(dir2, DIR_2_SUFFIX)

    dir1_basenames = {base_name_from_dir1(p.name): p for p in dir1_files}
    dir2_basenames = {}
    for p in dir2_files:
        # "Amy_Season_3.straight.txt" -> "Amy_Season_3"
        if not p.name.endswith(DIR_2_SUFFIX):
            continue
        base = p.name[: -len(DIR_2_SUFFIX)]
        dir2_basenames[base] = p

    missing_in_dir2: list[str] = []
    mismatched: list[tuple[str, FileInfo, FileInfo]] = []
    matched: list[str] = []

    # Compare pairs from Directory 1 -> expected Directory 2 counterpart
    for base, p1 in sorted(dir1_basenames.items(), key=lambda x: x[0].lower()):
        p2 = dir2_basenames.get(base)
        if p2 is None:
            missing_in_dir2.append(base)
            continue

        info1 = build_fileinfo(p1)
        info2 = build_fileinfo(p2)

        if info1.size_bytes == info2.size_bytes and info1.sha256 == info2.sha256:
            matched.append(base)
        else:
            mismatched.append((base, info1, info2))

    # Leftovers: files in Directory 2 without a corresponding Directory 1 file
    missing_in_dir1 = sorted(
        [base for base in dir2_basenames.keys() if base not in dir1_basenames],
        key=lambda s: s.lower(),
    )

    # Write report
    lines: list[str] = []
    lines.append("all_seasons_check report")
    lines.append("")
    lines.append(f"Directory 1: {dir1}")
    lines.append(f"Directory 2: {dir2}")
    lines.append("")
    lines.append("Summary")
    lines.append("-------")
    lines.append(f"Directory 1 files (*{DIR_1_SUFFIX}): {len(dir1_files)}")
    lines.append(f"Directory 2 files (*{DIR_2_SUFFIX}): {len(dir2_files)}")
    lines.append(f"Matched pairs: {len(matched)}")
    lines.append(f"Mismatched pairs: {len(mismatched)}")
    lines.append(f"Missing in Directory 2: {len(missing_in_dir2)}")
    lines.append(f"Leftovers in Directory 2 (missing in Directory 1): {len(missing_in_dir1)}")
    lines.append("")

    if mismatched:
        lines.append("Mismatched pairs (NOT identical)")
        lines.append("-------------------------------")
        for base, info1, info2 in mismatched:
            lines.append(f"- Base name: {base}")
            lines.append(f"  Dir1: {info1.path.name}  size={info1.size_bytes}  sha256={info1.sha256}")
            lines.append(f"  Dir2: {info2.path.name}  size={info2.size_bytes}  sha256={info2.sha256}")
        lines.append("")

    if missing_in_dir2:
        lines.append("Missing in Directory 2 (expected counterpart not found)")
        lines.append("------------------------------------------------------")
        for base in missing_in_dir2:
            lines.append(f"- {expected_dir2_filename(base)} (for {base}{DIR_1_SUFFIX})")
        lines.append("")

    if missing_in_dir1:
        lines.append("Leftovers in Directory 2 (no corresponding file in Directory 1)")
        lines.append("--------------------------------------------------------------")
        for base in missing_in_dir1:
            lines.append(f"- {dir2_basenames[base].name}")
        lines.append("")

    ok = (not mismatched) and (not missing_in_dir2) and (not missing_in_dir1)
    lines.append("Result")
    lines.append("------")
    if ok:
        lines.append("OK: All files have exactly one corresponding pair and all pairs are identical.")
        exit_code = 0
    else:
        lines.append("NOT OK: See sections above for mismatches and/or missing/leftover files.")
        exit_code = 1

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report: {report_path}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())