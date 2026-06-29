# ML2021 Spring Resources

This folder manages structured resources from the official [Machine Learning 2021 Spring](https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php) page.

## Files

- `manifest.json`: structured index of lectures, homework, videos, platforms, and downloadable files.
- `catalog.md`: human-readable table of PDF resources and local mirror paths.
- `downloads/`: local mirror of PDF files. This folder is ignored by git.

## Sync

Refresh the manifest:

```sh
python3 scripts/sync_ml2021_resources.py --manifest-only
```

Refresh the manifest and download local files:

```sh
python3 scripts/sync_ml2021_resources.py --download
```

The script downloads and indexes PDF files for slides and assignments. Colab notebooks, YouTube videos, Kaggle pages, and large datasets stay as links in `manifest.json`; PPT/PPTX files are ignored.
