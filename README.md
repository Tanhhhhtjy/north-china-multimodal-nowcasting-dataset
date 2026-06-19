# North China Multimodal Nowcasting Dataset

**Language**: **English** | [中文](README_zh.md)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Region: North China](https://img.shields.io/badge/region-North%20China-blue.svg)](#spatial-domain)
[![Period: May-Aug 2023](https://img.shields.io/badge/period-May--Aug%202023-blue.svg)](#temporal-coverage)
[![Modalities: 5+2](https://img.shields.io/badge/modalities-5%20+%202%20reanalysis-green.svg)](#data-modalities)

A multimodal radar nowcasting dataset for North China, covering May–August 2023 at
6-minute cadence and 1 km spatial resolution, with **five co-located physical
observation streams** (radar reflectivity, GNSS-derived precipitable water
vapour, surface temperature, surface relative humidity, surface pressure) and
**two ERA5 reanalysis channels** (low-level temperature and specific humidity at
925 hPa) all temporally and spatially aligned to a common 661 × 701 grid.

This dataset is designed for two complementary uses:

1. **Training** deep-learning short-term precipitation nowcasting models that
   benefit from heterogeneous multimodal input.
2. **Analysis / visualisation** of multimodal weather context (e.g. comparing
   moisture fields against radar evolution during convective events).

---

## 📑 Table of Contents

- [Quick Start](#quick-start)
- [Download](#download)
- [Data Overview](#data-overview)
- [Data Modalities](#data-modalities)
- [File Layout](#file-layout)
- [Schema (`.npz`)](#schema-npz)
- [Normalization Statistics](#normalization-statistics)
- [Splits](#splits)
- [Spatial Domain](#spatial-domain)
- [Temporal Coverage](#temporal-coverage)
- [Methodology](#methodology)
- [Honest Caveats](#honest-caveats)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)

---

## Quick Start

After downloading and extracting one of the archives below:

```python
import numpy as np

# Load one frame (≈ 8.6 MB)
data = np.load("dataset_for_team/npz/2023-07-30T09-00-00.npz", allow_pickle=True)

# Radar (dense): shape (661, 701), float32, units mm/h
radar = data["radar_mmh"]
print(radar.shape, radar.dtype, radar.min(), radar.max())
# (661, 701) float32 0.017 ~135

# PWV (dense, interpolated): shape (661, 701), float32, units kg/m²
pwv_dense = data["pwv_dense"]

# PWV (sparse, ground truth at stations): shape (176,)
pwv_value  = data["pwv_sparse_value"]
pwv_lonlat = data["pwv_sparse_lonlat"]   # (176, 2)
pwv_mask   = data["pwv_sparse_mask"]     # (176,) — 1 = valid, 0 = missing
```

---

## Download

The dataset is hosted on **Baidu Netdisk**. Three archives are provided:

| Archive | Size | Contents | Link | Code |
|---|---:|---|---|---|
| **Full directory** (recommended) | — | README + MVP + Full set | [pan.baidu.com](https://pan.baidu.com/s/1nWOoV7uWI426z5uc-450tg) | `39b4` |
| **MVP subset** | 5.3 GB | 4 convective storm days + all visualisations | [pan.baidu.com](https://pan.baidu.com/s/1oukwTGS5tLwVQYvtWFudng) | `0717` |
| **Full set** | 106.15 GB | All 13 500 frames spanning May–Aug 2023 | [pan.baidu.com](https://pan.baidu.com/s/1PyyRZ4wLqewo9FrtjhRpSQ) | `6c29` |

Sharing links are valid for **30 days** from 2026-06-20. After expiry please
[contact us](#contact) to regenerate.

### Downloading via CLI

```bash
pip install bypy
bypy info     # follow the browser auth prompt
bypy downdir /pluvian-multimodal-dataset/full/
```

---

## Data Overview

| Property | Value |
|---|---|
| **Region** | North China (lon 113.00°E – 120.00°E, lat 36.00°N – 42.60°N) |
| **Spatial grid** | 661 × 701 pixels at 0.01° (≈ 1 km) |
| **Temporal cadence** | 6 minutes |
| **Period covered** | 2023-05-01 to 2023-08-31 (123 calendar days, 94 with valid radar) |
| **Total frames** | 13 536 |
| **Modalities** | 5 physical observations + 2 reanalysis channels = 7 total |
| **Single-frame size** | ≈ 8.6 MB (compressed `.npz` with dense + sparse arrays + 7 grayscale PNG) |
| **Full archive** | ≈ 106 GB |

---

## Data Modalities

Seven channels are provided per frame. The first five are physical observations,
the last two are ERA5 reanalysis at 925 hPa.

| # | Name (npz key) | Source | Unit | Native form | Dense form |
|---|---|---|---|---|---|
| 1 | `radar_mmh` | S-band radar mosaic | mm/h | 661 × 701 grid (native) | identical |
| 2 | `pwv_dense` / `pwv_sparse_*` | 176 GNSS sites | kg/m² | sparse stations, 30 min | IDW interpolation |
| 3 | `tem_dense` / `tem_sparse_*` | 289 surface stations | °C | sparse stations, 1 h | IDW interpolation |
| 4 | `rhu_dense` / `rhu_sparse_*` | 289 surface stations | % | sparse stations, 1 h | IDW interpolation |
| 5 | `prs_dense` / `prs_sparse_*` | 289 surface stations | hPa | sparse stations, 1 h | IDW interpolation |
| 6 | `era5_t_925` | ERA5 reanalysis | K | 0.25° grid, 1 h | bilinear upsampled |
| 7 | `era5_q_925` | ERA5 reanalysis | kg/kg | 0.25° grid, 1 h | bilinear upsampled |

The radar field is converted from reflectivity (dBZ) to rain rate (mm/h) via
the operational China Z–R relation R = (Z / 300)^(1 / 1.4).

Per-modality global statistics (used for the `.png` visualisations) are listed
in [`schema/normalize_stats.json`](schema/normalize_stats.json).

---

## File Layout

After extracting `dataset_full.zip` (or `dataset_mvp_v2.zip`) you get:

```
dataset_for_team/                       (or dataset_for_team_mvp/)
├── run_log.json                        Pipeline run summary
├── npz/                                ★ Training-ready arrays
│   └── 2023-07-30T09-00-00.npz         One file per frame (8.6 MB)
└── png/                                Per-modality 8-bit grayscale (visualisation + training-as-image)
    ├── radar/                          radar in log1p + jet colormap (stored as gray)
    ├── pwv_dense/
    ├── tem_station_dense/
    ├── rhu_station_dense/
    ├── prs_station_dense/
    ├── era5_t_925/
    └── era5_q_925/                     572 files each in MVP, 13 500 files each in Full
```

The **MVP archive** additionally contains:

```
dataset_for_team_mvp/
├── mosaic/                             7-modality + metadata composite per frame (572 files)
├── stations_overlay/                   Radar with 176 PWV + 289 surface station locations
│                                       overlaid (3 representative storm timestamps)
└── samples/
    ├── case_2023-07-30_storm_evolution.pdf   Vector multi-modal time series, 8 × 7 panel
    └── case_2023-07-30_radar.gif             Animated radar evolution, 40 frames @ 5 fps
```

Directory listings for each subset are mirrored under
[`schema/directory_listing_mvp.txt`](schema/directory_listing_mvp.txt) and
[`schema/directory_listing_full.txt`](schema/directory_listing_full.txt).

---

## Schema (`.npz`)

Each `.npz` file is a compressed dictionary with the following keys:

| Key | Shape | Dtype | Units | Description |
|---|---|---|---|---|
| `timestamp` | `()` (scalar) | `<U19` | ISO-8601 | e.g. `'2023-07-30T09:00:00'` |
| `radar_mmh` | `(661, 701)` | `float32` | mm/h | Radar-derived rain rate |
| `pwv_dense` | `(661, 701)` | `float32` | kg/m² | PWV interpolated to grid |
| `pwv_sparse_value` | `(176,)` | `float32` | kg/m² | Raw PWV at each station |
| `pwv_sparse_lonlat` | `(176, 2)` | `float32` | degrees | Station coords (lon, lat) |
| `pwv_sparse_mask` | `(176,)` | `float32` | 0/1 | 1 = observation valid |
| `tem_dense` | `(661, 701)` | `float32` | °C | Temperature interpolated |
| `tem_sparse_value` | `(289,)` | `float32` | °C | Raw values at 289 surface stations |
| `tem_sparse_mask` | `(289,)` | `float32` | 0/1 | Validity per station |
| `rhu_dense` | `(661, 701)` | `float32` | % | Relative humidity, interpolated |
| `rhu_sparse_value` | `(289,)` | `float32` | % | Raw at stations |
| `rhu_sparse_mask` | `(289,)` | `float32` | 0/1 | Validity per station |
| `prs_dense` | `(661, 701)` | `float32` | hPa | Surface pressure, interpolated |
| `prs_sparse_value` | `(289,)` | `float32` | hPa | Raw at stations |
| `prs_sparse_mask` | `(289,)` | `float32` | 0/1 | Validity per station |
| `station_sparse_lonlat` | `(289, 2)` | `float32` | degrees | Surface-station coords (shared by TEM/RHU/PRS) |
| `era5_t_925` | `(661, 701)` | `float32` | K | ERA5 temperature at 925 hPa, upsampled |
| `era5_q_925` | `(661, 701)` | `float32` | kg/kg | ERA5 specific humidity at 925 hPa, upsampled |

A machine-readable schema is at [`schema/schema.json`](schema/schema.json).

---

## Normalization Statistics

The full normalization statistics (p2, p50, p98, min, max) per modality are
provided in [`schema/normalize_stats.json`](schema/normalize_stats.json),
computed over ≈ 1.01 M sample pixels. Headline values:

| Modality | p2 | p50 | p98 | log1p preprocess? |
|---|---:|---:|---:|---|
| Radar (mm/h) | 0.02 | 0.02 | 0.96 (log1p) | **Yes** (heavy-tailed) |
| PWV (kg/m²) | 9.07 | 33.97 | 67.50 | No |
| Surface temperature (°C) | 12.29 | 24.20 | 34.33 | No |
| Surface relative humidity (%) | 19.13 | 69.83 | 97.72 | No |
| Surface pressure (hPa) | 853.01 | 980.60 | 1011.21 | No |
| ERA5 T @ 925 hPa (K) | 287.27 | 296.25 | 303.43 | No |
| ERA5 q @ 925 hPa (kg/kg) | 0.0028 | 0.0113 | 0.0188 | No |

These are statistics **for the visualisation pipeline only**. For model training
we recommend per-batch standardisation against your training subset.

---

## Splits

Frames are grouped by calendar date. The split labels match the parent
nowcasting project (`pipeline/manifest.csv`):

| Split | # Days | # Frames | Notes |
|---|---:|---:|---|
| `train` | 74 | 10 656 | Main training set |
| `val` | 8 | 1 152 | Validation |
| `test_robust` | 8 | 1 152 | Non-storm hold-out |
| `event_test` | 4 | 576 | **Strong convective storm days** (2023-07-29 – 08-01) |

The list of days per split is in [`schema/manifest.csv`](schema/manifest.csv).

The **MVP** archive contains only the `event_test` split (4 storm days × 144
frames = 572 files after dropping 4 boundary frames with missing radar).

---

## Spatial Domain

```
Longitude bounds: 113.00°E – 120.00°E (701 cells × 0.01°)
Latitude  bounds:  36.00°N –  42.60°N (661 cells × 0.01°)
Grid spacing:     ≈ 1 km
```

Coordinates of every pixel can be reconstructed as:

```python
import numpy as np
lon = np.round(np.arange(113.00, 120.00 + 1e-6, 0.01), 2)  # length 701
lat = np.round(np.arange( 36.00,  42.60 + 1e-6, 0.01), 2)  # length 661
```

---

## Temporal Coverage

- **Period**: 2023-05-01 00:00 to 2023-08-31 23:54 UTC
- **Cadence**: 6 minutes (144 nominal frames per day)
- **Frame timestamps**: ISO-8601 string in `timestamp` key
- 29 calendar days are excluded due to radar data quality issues (see `run_log.json`)

---

## Methodology

### Temporal alignment
All non-radar modalities are linearly interpolated in time to the radar 6-min
grid. PWV (30 min) interpolates between bracketing frames; surface stations
(1 h) similarly; ERA5 (1 h) uses the standard linear interpolation kernel from
the parent pipeline (`pipeline.utils.linear_time_interp`).

### Spatial alignment
- Radar is native 661 × 701.
- PWV / temperature / humidity / pressure are interpolated from station
  locations to the radar grid via inverse-distance weighting (IDW with k = 8
  neighbours, power = 2).
- ERA5 (0.25°) is bilinearly upsampled to 0.01° (`pipeline.utils.bilinear_interp_to_radar`).

### Unit conversions
Radar reflectivity is converted to rain rate via R = (Z / 300)^(1/1.4) where
Z = 10^(dBZ/10). This is the Chinese operational Z–R relation. ERA5 fields
are kept in their native units (K, kg/kg).

### Sparse-versus-dense pairing
For every non-radar physical modality the dataset provides **both** the dense
interpolated field (`*_dense`) and the underlying sparse station observations
(`*_sparse_value`, `*_sparse_lonlat`, `*_sparse_mask`). Users can pick whichever
representation matches their model.

### Reproducibility scripts
The pipeline that produces each frame is open-source as part of the parent
Pluvian project. See [Citation](#citation) for repository pointers.

---

## Honest Caveats

Please read this section before training or interpreting results.

1. **Sparse-to-dense interpolation injects artificial structure.** The four
   non-radar physical modalities (PWV, TEM, RHU, PRS) are spatially smooth by
   construction because they are interpolated from station observations.
   Pixels far from any station are interpolation, not measurement. To work
   with truth-only observations, use the `*_sparse_value` / `*_sparse_lonlat`
   keys instead of `*_dense`.

2. **ERA5 upsampling smooths structure.** ERA5 reanalysis at 925 hPa is
   delivered on a 0.25° (≈ 25 km) grid, then bilinearly upsampled to 1 km. The
   apparent high resolution is interpolation; the effective resolution remains
   25 km.

3. **Single radar source, single region.** The radar is the operational S-band
   mosaic over North China only. Generalisation to other regions, seasons
   outside May–August, or other radar networks is not validated.

4. **PNG quantisation.** The `.png` files are 8-bit grayscale rescaled per
   modality using the dataset-wide p2 / p98 statistics in `normalize_stats.json`.
   They are intended for visualisation and quick sanity checks, **not** as the
   primary training target. Use the `.npz` arrays for training.

5. **Sharing links expire in 30 days.** The Baidu Netdisk links above are
   valid until 2026-07-20. Please [contact us](#contact) if you need a
   regenerated link or a more permanent host.

---

## Citation

If you use this dataset in academic work, please cite:

```bibtex
@misc{tian2026_north_china_multimodal_nowcasting,
  title  = {North China Multimodal Nowcasting Dataset:
            Co-located radar, GNSS PWV, surface meteorology and ERA5 over
            North China, 6-minute cadence, May–August 2023},
  author = {Tian, Jinyu},
  year   = {2026},
  note   = {Companion dataset to the Pluvian multimodal nowcasting framework},
  url    = {https://github.com/Tanhhhhtjy/north-china-multimodal-nowcasting-dataset}
}
```

The dataset was produced as part of the Pluvian short-term precipitation
nowcasting research line. The parent codebase is private at the time of
release; please contact the maintainer for access.

---

## License

The dataset is released under
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
(CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

This dataset card and the layout scripts in this repository are released under
the [MIT License](LICENSE).

---

## Contact

Maintainer: **Tian Jinyu (田锦煜)**, Department 6, Beihang University
GitHub: [@Tanhhhhtjy](https://github.com/Tanhhhhtjy)

Please open an issue on this repository for bug reports, broken links, or
dataset-quality questions.
