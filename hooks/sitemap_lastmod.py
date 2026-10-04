"""Replace MkDocs build dates in sitemap.xml with Git revision dates."""

from __future__ import annotations

import gzip
import logging
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urljoin


LOG = logging.getLogger("mkdocs.hooks.sitemap_lastmod")
SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
PAGES_BY_URL: dict[str, Path] = {}
REPOSITORY_ROOT: Path | None = None


def on_files(files, *, config):
    """Remember the source file corresponding to each generated page URL."""
    global REPOSITORY_ROOT

    REPOSITORY_ROOT = Path(config.config_file_path).resolve().parent
    site_url = f"{str(config.site_url).rstrip('/')}/"

    PAGES_BY_URL.clear()
    for file in files.documentation_pages():
        PAGES_BY_URL[urljoin(site_url, file.url)] = Path(file.abs_src_path).resolve()


def on_post_build(*, config):
    """Write accurate per-page modification dates to both sitemap variants."""
    if REPOSITORY_ROOT is None:
        raise RuntimeError("Sitemap page mapping was not initialized")

    sitemap_path = Path(config.site_dir) / "sitemap.xml"
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespace = {"sitemap": SITEMAP_NAMESPACE}

    ET.register_namespace("", SITEMAP_NAMESPACE)

    for url_element in root.findall("sitemap:url", namespace):
        location_element = url_element.find("sitemap:loc", namespace)
        if location_element is None or not location_element.text:
            raise RuntimeError("Sitemap entry is missing its location")

        page_url = location_element.text
        source_path = PAGES_BY_URL.get(page_url)
        if source_path is None:
            raise RuntimeError(f"No Markdown source found for sitemap URL: {page_url}")

        last_modified = _git_last_modified(source_path)
        lastmod_element = url_element.find("sitemap:lastmod", namespace)

        if last_modified is None:
            if lastmod_element is not None:
                url_element.remove(lastmod_element)
            LOG.warning("No Git revision date for %s; omitted sitemap lastmod", source_path)
            continue

        if lastmod_element is None:
            lastmod_element = ET.SubElement(
                url_element,
                f"{{{SITEMAP_NAMESPACE}}}lastmod",
            )
        lastmod_element.text = last_modified

    ET.indent(tree, space="  ")
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)
    _write_gzip_copy(sitemap_path)


def _git_last_modified(source_path: Path) -> str | None:
    relative_path = source_path.relative_to(REPOSITORY_ROOT)
    result = subprocess.run(
        [
            "git",
            "log",
            "-1",
            "--follow",
            "--format=%cs",
            "--",
            str(relative_path),
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() or None


def _write_gzip_copy(sitemap_path: Path) -> None:
    compressed_path = sitemap_path.with_suffix(f"{sitemap_path.suffix}.gz")
    with compressed_path.open("wb") as destination:
        with gzip.GzipFile(fileobj=destination, mode="wb", mtime=0) as archive:
            archive.write(sitemap_path.read_bytes())
