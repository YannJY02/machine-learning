# ML2021 Spring Resources

This folder manages structured resources from the official [Machine Learning 2021 Spring](https://speech.ee.ntu.edu.tw/~hylee/ml/2021-spring.php) page.

## Files

- `manifest.json`: structured index of lectures, homework, videos, platforms, and downloadable files.
- `catalog.md`: human-readable table of PDF resources and local mirror paths.
- `dataset-manifest.json`: structured index of public Google Drive exercise assets detected in official notebooks.
- `datasets.md`: human-readable table of detected exercise assets.
- `downloads/`: local mirror of PDF files. This folder is ignored by git.
- `datasets/`: local mirror of exercise assets and datasets. This folder is ignored by git.
- `upstream/`: shallow local mirror of the official GitHub repository. This folder is ignored by git.

## Sync

Refresh the manifest:

```sh
python3 scripts/sync_ml2021_resources.py --manifest-only
```

Refresh the manifest and download local files:

```sh
python3 scripts/sync_ml2021_resources.py --download
```

Clone or update the official GitHub mirror and detect exercise assets:

```sh
python3 scripts/sync_ml2021_resources.py --sync-upstream --manifest-only
```

Download public Google Drive exercise assets detected in the official notebooks:

```sh
python3 -m pip install --user gdown
python3 scripts/sync_ml2021_resources.py --sync-upstream --download-datasets
```

The script downloads and indexes PDF files for slides and assignments. Colab notebooks, YouTube videos, Kaggle pages, and large datasets stay as links in `manifest.json`; PPT/PPTX files are ignored. Kaggle assets require a Kaggle account and accepting competition rules, so they are treated as manual follow-up unless local credentials are available.
