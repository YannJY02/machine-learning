#!/usr/bin/env python3
"""Build and optionally download the ML2021 Spring resource manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urljoin, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover - local setup guard
    print("Missing dependency: beautifulsoup4. Install it with `python3 -m pip install beautifulsoup4`.", file=sys.stderr)
    raise


COURSE_URL = "https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php"
OUT_DIR = Path("resources/2021-spring")
MANIFEST_PATH = OUT_DIR / "manifest.json"
CATALOG_PATH = OUT_DIR / "catalog.md"


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
    parser.add_argument("--manifest-only", action="store_true", help="refresh manifest without downloading files")
    parser.add_argument("--overwrite", action="store_true", help="replace existing downloaded files")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest = build_manifest()
    write_manifest(manifest)
    write_catalog(manifest)
    print(f"wrote {MANIFEST_PATH} ({len(manifest['downloadables'])} downloadable files)")

    if args.download and not args.manifest_only:
        downloaded, skipped = download(manifest, repo_root, args.overwrite)
        print(f"downloaded={downloaded} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
