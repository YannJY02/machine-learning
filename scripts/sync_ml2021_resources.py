#!/usr/bin/env python3
"""Build and optionally download the ML2021 Spring resource manifest."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urljoin, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - local setup guard
    print("Missing dependency: beautifulsoup4. Install it with `python3 -m pip install beautifulsoup4`.", file=sys.stderr)
    raise


COURSE_URL = "https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php"
UPSTREAM_REPO_URL = "https://github.com/ga642381/ML2021-Spring.git"
OUT_DIR = Path("resources/2021-spring")
MANIFEST_PATH = OUT_DIR / "manifest.json"
CATALOG_PATH = OUT_DIR / "catalog.md"
UPSTREAM_DIR = OUT_DIR / "upstream/ML2021-Spring"
DATASET_MANIFEST_PATH = OUT_DIR / "dataset-manifest.json"
DATASET_CATALOG_PATH = OUT_DIR / "datasets.md"
DATASETS_DIR = OUT_DIR / "datasets"


def slug(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "item"


def filename_from_url(url: str) -> str:
    return unquote(PurePosixPath(urlparse(url).path).name).replace(" ", "_")


def suffix(url: str) -> str:
    return PurePosixPath(urlparse(url).path).suffix.lower()


def raw_colab_url(url: str) -> str | None:
    prefix = "https://colab.research.google.com/github/"
    if not url.startswith(prefix) or "/blob/" not in url:
        return None
    repo, path = url[len(prefix) :].split("/blob/", 1)
    branch, file_path = path.split("/", 1)
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{file_path}"


def request_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, quote(parts.path, safe="/%()"), parts.query, parts.fragment))


def node_links(node, base_url: str) -> list[dict[str, str]]:
    links = []
    for anchor in node.find_all("a"):
        href = anchor.get("href")
        if not href or href == "#!":
            continue
        links.append({"label": anchor.get_text(" ", strip=True), "url": urljoin(base_url, href)})
    return links


def fetch_soup(url: str) -> BeautifulSoup:
    request = Request(request_url(url), headers={"User-Agent": "machine-learning-study-resource-sync/1.0"})
    with urlopen(request, timeout=30) as response:
        return BeautifulSoup(response.read(), "html.parser")


def build_manifest() -> dict:
    soup = fetch_soup(COURSE_URL)
    downloadables: list[dict[str, str]] = []
    seen_downloads: set[str] = set()

    def add_download(kind: str, source_url: str, path: str, title: str) -> None:
        if suffix(source_url) != ".pdf":
            return
        download_url = raw_colab_url(source_url) or source_url
        if download_url in seen_downloads:
            return
        seen_downloads.add(download_url)
        downloadables.append(
            {
                "kind": kind,
                "title": title,
                "source_url": source_url,
                "download_url": download_url,
                "path": path,
            }
        )

    lectures = []
    for order, card in enumerate(soup.select("div.content_timeline"), 1):
        strong = card.find("strong")
        title = strong.get_text(" ", strip=True) if strong else f"Lecture {order}"
        item_slug = slug(title)
        links = node_links(card, COURSE_URL)
        slides = [link for link in links if suffix(link["url"]) == ".pdf"]
        videos = [link for link in links if "youtube.com" in link["url"] or "youtu.be" in link["url"]]
        homework_refs = sorted(set(re.findall(r"HW\d+", card.get_text(" ", strip=True))))
        lectures.append(
            {
                "order": order,
                "title": title,
                "slug": item_slug,
                "slides": slides,
                "videos": videos,
                "homework_refs": homework_refs,
            }
        )
        for link in slides:
            add_download(
                "lecture_slide",
                link["url"],
                f"downloads/lectures/{order:02d}-{item_slug}/slides/{filename_from_url(link['url'])}",
                title,
            )

    table = soup.find("table")
    if table is None:
        raise RuntimeError("Could not find homework table on the official page.")

    headers = [cell.get_text(" ", strip=True) for cell in table.find("tr").find_all(["th", "td"])]
    homework = []
    for table_row in table.find_all("tr")[1:]:
        cells = table_row.find_all(["th", "td"])
        row = {header: cells[index] if index < len(cells) else None for index, header in enumerate(headers)}
        number = row["#"].get_text(" ", strip=True)
        title = row["HW"].get_text(" ", strip=True)
        item_slug = slug(f"{number}-{title}" if number.lower() != "x" else title)
        item = {
            "number": number,
            "title": title,
            "slug": item_slug,
            "assignment_slides": node_links(row["Slide"], COURSE_URL),
            "code": [],
            "platforms": node_links(row["Platforms"], COURSE_URL),
            "videos_en": node_links(row["Video(En)"], COURSE_URL),
            "videos_zh": node_links(row["Video(Zh)"], COURSE_URL),
            "date": row["Date"].get_text(" ", strip=True),
            "ta": row["TA"].get_text(" ", strip=True),
        }
        for link in node_links(row["Code"], COURSE_URL):
            raw_url = raw_colab_url(link["url"])
            if raw_url:
                link["raw_url"] = raw_url
            item["code"].append(link)
        homework.append(item)

        base = "tutorials" if number.lower() == "x" else "homework"
        for link in item["assignment_slides"]:
            add_download(
                "tutorial_slide" if base == "tutorials" else "homework_slide",
                link["url"],
                f"downloads/{base}/{item_slug}/slides/{filename_from_url(link['url'])}",
                title,
            )
        for link in item["code"]:
            download_url = link.get("raw_url") or link["url"]
            add_download(
                "tutorial_notebook" if base == "tutorials" else "homework_notebook",
                link["url"],
                f"downloads/{base}/{item_slug}/notebooks/{filename_from_url(download_url)}",
                title,
            )

    return {
        "course": "Machine Learning 2021 Spring",
        "source_url": COURSE_URL,
        "generated_from": "official course page",
        "local_download_root": str(OUT_DIR / "downloads"),
        "download_policy": "Download and index PDF resources only for slides and assignments. Keep notebooks, videos, Kaggle pages, and large datasets as links; ignore PPT/PPTX files.",
        "lectures": lectures,
        "homework": homework,
        "downloadables": downloadables,
    }


def write_manifest(manifest: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def markdown_link(label: str, url: str) -> str:
    safe_label = label.replace("|", "\\|")
    safe_url = url.replace(" ", "%20")
    return f"[{safe_label}]({safe_url})"


def write_catalog(manifest: dict) -> None:
    by_source = {item["source_url"]: item for item in manifest["downloadables"]}
    lines = [
        "# ML2021 Spring Catalog",
        "",
        f"Source: {markdown_link(manifest['source_url'], manifest['source_url'])}",
        "",
        f"Download policy: {manifest['download_policy']}",
        "",
        f"Downloadable PDFs: {len(manifest['downloadables'])}",
        "",
        "## Lecture PDFs",
        "",
        "| # | Lecture | PDF | Local Path |",
        "| --- | --- | --- | --- |",
    ]
    for lecture in manifest["lectures"]:
        for slide in lecture["slides"]:
            item = by_source.get(slide["url"])
            local_path = item["path"] if item else ""
            lines.append(
                f"| {lecture['order']} | {lecture['title']} | {markdown_link(filename_from_url(slide['url']), slide['url'])} | `{local_path}` |"
            )

    lines.extend(
        [
            "",
            "## Tutorials And Homework PDFs",
            "",
            "| # | Title | Date | PDF | Local Path |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in manifest["homework"]:
        for slide in item["assignment_slides"]:
            downloadable = by_source.get(slide["url"])
            local_path = downloadable["path"] if downloadable else ""
            lines.append(
                f"| {item['number']} | {item['title']} | {item['date']} | {markdown_link(filename_from_url(slide['url']), slide['url'])} | `{local_path}` |"
            )

    lines.extend(
        [
            "",
            "## Linked-Only Resources",
            "",
            "Colab notebooks, YouTube videos, Kaggle pages, and large datasets are indexed in `manifest.json` but not downloaded.",
            "",
        ]
    )
    CATALOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def sync_upstream(repo_root: Path) -> None:
    target = repo_root / UPSTREAM_DIR
    if target.exists():
        subprocess.run(["git", "-C", str(target), "pull", "--ff-only"], check=True)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", UPSTREAM_REPO_URL, str(target)], check=True)


def notebook_source(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in data.get("cells", []))


def cell_output_paths(cell: dict) -> list[str]:
    paths = []
    for output in cell.get("outputs", []):
        text = output.get("text", "")
        if isinstance(text, list):
            text = "".join(text)
        for match in re.finditer(r"To:\s+([^\n\r]+)", text):
            paths.append(Path(match.group(1).strip()).name)
    return paths


def parse_gdown_assets(repo_root: Path) -> dict:
    upstream = repo_root / UPSTREAM_DIR
    if not upstream.exists():
        raise RuntimeError(f"Missing upstream mirror: {UPSTREAM_DIR}. Run with --sync-upstream first.")

    assets_by_key: dict[tuple[str, str], dict] = {}
    for notebook in sorted(upstream.glob("HW*/HW*.ipynb")):
        hw = notebook.parts[-2].lower()
        data = json.loads(notebook.read_text(encoding="utf-8"))
        for cell in data.get("cells", []):
            text = "".join(cell.get("source", [])).replace("\\\n", " ")
            output_paths = cell_output_paths(cell)
            for index, match in enumerate(
                re.finditer(
                    r"gdown\s+--id\s+['\"]?([A-Za-z0-9_-]{15,})['\"]?(?:\s+(?:--output|-O)\s+['\"]?([^\n'\"]+)['\"]?)?",
                    text,
                )
            ):
                file_id = match.group(1)
                output = (match.group(2) or (output_paths[index] if index < len(output_paths) else f"{file_id}.download")).strip()
                output = output.replace("{workspace_dir}/", "").strip()
                output = Path(output).name
                if not output or output.startswith("{"):
                    output = f"{file_id}.download"
                key = (hw, output)
                if key in assets_by_key:
                    if file_id not in assets_by_key[key]["file_ids"]:
                        assets_by_key[key]["file_ids"].append(file_id)
                    continue
                assets_by_key[key] = {
                    "homework": hw,
                    "source": str(notebook.relative_to(upstream)),
                    "kind": "google_drive",
                    "file_id": file_id,
                    "file_ids": [file_id],
                    "filename": output,
                    "path": str(DATASETS_DIR / hw / output),
                }

    return {
        "source_repo": UPSTREAM_REPO_URL,
        "upstream_mirror": str(UPSTREAM_DIR),
        "local_dataset_root": str(DATASETS_DIR),
        "policy": "Download exercise assets found in official notebooks when they are publicly accessible through Google Drive. Kaggle and access-controlled sources stay as links/manual follow-up.",
        "assets": list(assets_by_key.values()),
    }


def write_dataset_manifest(dataset_manifest: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_MANIFEST_PATH.write_text(json.dumps(dataset_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# ML2021 Spring Exercise Assets",
        "",
        f"Source repo: {markdown_link('ga642381/ML2021-Spring', 'https://github.com/ga642381/ML2021-Spring')}",
        "",
        dataset_manifest["policy"],
        "",
        f"Detected Google Drive assets: {len(dataset_manifest['assets'])}",
        "",
        "| Homework | File | Status | Size | Mirrors | Source Notebook | Local Path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in dataset_manifest["assets"]:
        local_path = Path(item["path"])
        status = "downloaded" if local_path.exists() else "missing"
        size = human_size(local_path.stat().st_size) if local_path.exists() else ""
        mirror_count = len(item.get("file_ids", [item["file_id"]]))
        lines.append(
            f"| {item['homework']} | `{item['filename']}` | {status} | {size} | {mirror_count} | `{item['source']}` | `{item['path']}` |"
        )
    lines.extend(
        [
            "",
            "## Manual Sources",
            "",
            "- Kaggle competitions require a Kaggle account, API token, and accepting the competition rules.",
            "- Some notebooks include backup mirrors on Dropbox, OneDrive, MEGA, or academic torrents; use those only when the Google Drive asset is unavailable.",
            "",
        ]
    )
    DATASET_CATALOG_PATH.write_text("\n".join(lines), encoding="utf-8")


def human_size(bytes_count: int) -> str:
    value = float(bytes_count)
    for unit in ["B", "KB", "MB", "GB"]:
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{bytes_count} B"


def google_drive_confirm_token(response: requests.Response) -> str | None:
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    match = re.search(r"confirm=([0-9A-Za-z_]+)", response.text[:4096])
    return match.group(1) if match else None


def download_google_drive(file_id: str, target: Path, overwrite: bool) -> str:
    if target.exists() and not overwrite:
        return "skipped"
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp_target = target.with_suffix(target.suffix + ".part")

    try:
        import gdown
    except ImportError:
        gdown = None

    if gdown is not None:
        result = gdown.download(id=file_id, output=str(tmp_target), quiet=False, use_cookies=True)
        if not result:
            tmp_target.unlink(missing_ok=True)
            raise RuntimeError("gdown did not return a downloaded file")
        if looks_like_html(tmp_target):
            tmp_target.unlink(missing_ok=True)
            raise RuntimeError("download returned an HTML error page")
        tmp_target.replace(target)
        return "downloaded"

    session = requests.Session()
    params = {"export": "download", "id": file_id}
    response = session.get("https://drive.google.com/uc", params=params, stream=True, timeout=60)
    token = google_drive_confirm_token(response)
    if token:
        response.close()
        params["confirm"] = token
        response = session.get("https://drive.google.com/uc", params=params, stream=True, timeout=60)
    response.raise_for_status()

    with tmp_target.open("wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)
    if looks_like_html(tmp_target):
        tmp_target.unlink(missing_ok=True)
        raise RuntimeError("download returned an HTML error page")
    tmp_target.replace(target)
    return "downloaded"


def looks_like_html(path: Path) -> bool:
    if not path.exists() or path.stat().st_size > 64 * 1024:
        return False
    head = path.read_bytes()[:512].lstrip().lower()
    return head.startswith(b"<!doctype html") or head.startswith(b"<html")


def download_datasets(dataset_manifest: dict, repo_root: Path, overwrite: bool) -> tuple[int, int, int]:
    downloaded = skipped = failed = 0
    completed_by_id: dict[str, Path] = {}
    for item in dataset_manifest["assets"]:
        target = repo_root / item["path"]
        file_ids = item.get("file_ids", [item["file_id"]])
        for file_id in file_ids:
            if target.exists() and not overwrite:
                completed_by_id[file_id] = target
        existing_source = next((completed_by_id[file_id] for file_id in file_ids if file_id in completed_by_id), None)
        if existing_source and existing_source != target and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                target.hardlink_to(existing_source)
            except OSError:
                shutil.copy2(existing_source, target)
            print(f"linked {target} -> {existing_source}", flush=True)
            skipped += 1
            continue

        print(f"asset {item['homework']} {item['filename']}", flush=True)
        if target.exists() and not overwrite:
            skipped += 1
            continue

        last_error = None
        for file_id in file_ids:
            if file_id in completed_by_id:
                try:
                    target.hardlink_to(completed_by_id[file_id])
                except OSError:
                    shutil.copy2(completed_by_id[file_id], target)
                print(f"linked {target} -> {completed_by_id[file_id]}", flush=True)
                skipped += 1
                break
            try:
                result = download_google_drive(file_id, target, overwrite)
            except Exception as error:  # noqa: BLE001 - keep going through mirrors and independent assets
                last_error = error
                print(f"mirror failed {target} ({file_id}): {error}", flush=True)
                continue
            if result == "downloaded":
                downloaded += 1
                completed_by_id[file_id] = target
                print(f"downloaded {target}", flush=True)
            else:
                skipped += 1
                completed_by_id[file_id] = target
            break
        else:
            failed += 1
            print(f"failed {target}: {last_error}", flush=True)
    return downloaded, skipped, failed


def download(manifest: dict, repo_root: Path, overwrite: bool) -> tuple[int, int]:
    downloaded = 0
    skipped = 0
    for item in manifest["downloadables"]:
        target = repo_root / OUT_DIR / item["path"]
        if target.exists() and not overwrite:
            skipped += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f"downloading {target}", flush=True)
        request = Request(request_url(item["download_url"]), headers={"User-Agent": "machine-learning-study-resource-sync/1.0"})
        tmp_target = target.with_suffix(target.suffix + ".part")
        with urlopen(request, timeout=60) as response:
            with tmp_target.open("wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    file.write(chunk)
        tmp_target.replace(target)
        downloaded += 1
        print(f"downloaded {target}", flush=True)
    return downloaded, skipped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="download manifest files into resources/2021-spring/downloads")
    parser.add_argument("--sync-upstream", action="store_true", help="clone or update the official ML2021-Spring GitHub mirror")
    parser.add_argument("--download-datasets", action="store_true", help="download public Google Drive exercise assets from official notebooks")
    parser.add_argument("--manifest-only", action="store_true", help="refresh manifest without downloading files")
    parser.add_argument("--overwrite", action="store_true", help="replace existing downloaded files")
    args = parser.parse_args()

    repo_root = Path.cwd()
    if args.sync_upstream:
        sync_upstream(repo_root)

    manifest = build_manifest()
    write_manifest(manifest)
    write_catalog(manifest)
    print(f"wrote {MANIFEST_PATH} ({len(manifest['downloadables'])} downloadable files)")

    dataset_manifest = None
    if (repo_root / UPSTREAM_DIR).exists():
        dataset_manifest = parse_gdown_assets(repo_root)
        write_dataset_manifest(dataset_manifest)
        print(f"wrote {DATASET_MANIFEST_PATH} ({len(dataset_manifest['assets'])} detected assets)")

    if args.download and not args.manifest_only:
        downloaded, skipped = download(manifest, repo_root, args.overwrite)
        print(f"downloaded={downloaded} skipped={skipped}")
    if args.download_datasets and not args.manifest_only:
        if dataset_manifest is None:
            raise RuntimeError("Missing dataset manifest. Run with --sync-upstream or clone the upstream mirror first.")
        downloaded, skipped, failed = download_datasets(dataset_manifest, repo_root, args.overwrite)
        print(f"dataset_downloaded={downloaded} dataset_skipped={skipped} dataset_failed={failed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
