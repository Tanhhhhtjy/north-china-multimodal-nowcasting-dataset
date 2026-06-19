# 华北多模态短临降水数据集

**Language**: [English](README.md) | **中文**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Region: North China](https://img.shields.io/badge/region-North%20China-blue.svg)](#空间范围)
[![Period: May-Aug 2023](https://img.shields.io/badge/period-May--Aug%202023-blue.svg)](#时间覆盖)
[![Modalities: 5+2](https://img.shields.io/badge/modalities-5%20+%202%20reanalysis-green.svg)](#数据模态)

面向华北地区的多模态雷达短临降水数据集，覆盖 2023 年 5–8 月，时间分辨率 6 分钟，空间分辨率约 1 km。包含**五路同位物理观测**（雷达反射率、GNSS 反演的可降水量 PWV、地面气温、地面相对湿度、地面气压）以及**两路 ERA5 再分析变量**（925 hPa 低空温度与比湿），全部在时间和空间上对齐到统一的 661 × 701 网格。

本数据集面向两类用途：

1. **训练**：用于训练受益于异质多模态输入的深度学习短临降水预报模型。
2. **分析与可视化**：用于研究强对流事件中水汽场与雷达回波的演变关系等多模态气象上下文。

---

## 📑 目录

- [快速开始](#快速开始)
- [下载](#下载)
- [数据概览](#数据概览)
- [数据模态](#数据模态)
- [文件结构](#文件结构)
- [Schema（`.npz`）](#schema-npz)
- [归一化统计](#归一化统计)
- [数据切分](#数据切分)
- [空间范围](#空间范围)
- [时间覆盖](#时间覆盖)
- [方法说明](#方法说明)
- [使用须知（如实声明）](#使用须知如实声明)
- [引用](#引用)
- [许可证](#许可证)
- [联系方式](#联系方式)

---

## 快速开始

下载并解压任意一个压缩包后：

```python
import numpy as np

# 加载一帧 (≈ 8.6 MB)
data = np.load("dataset_for_team/npz/2023-07-30T09-00-00.npz", allow_pickle=True)

# 雷达（dense）：形状 (661, 701)，float32，单位 mm/h
radar = data["radar_mmh"]
print(radar.shape, radar.dtype, radar.min(), radar.max())
# (661, 701) float32 0.017 ~135

# PWV（dense，插值后）：形状 (661, 701)，float32，单位 kg/m²
pwv_dense = data["pwv_dense"]

# PWV（sparse，站点原始观测）：形状 (176,)
pwv_value  = data["pwv_sparse_value"]
pwv_lonlat = data["pwv_sparse_lonlat"]   # (176, 2)
pwv_mask   = data["pwv_sparse_mask"]     # (176,) — 1 表示有效，0 表示缺测
```

---

## 下载

数据托管于**百度网盘**，提供三个压缩包：

| 压缩包 | 大小 | 内容 | 链接 | 提取码 |
|---|---:|---|---|---|
| **全套目录**（推荐） | — | README + MVP + 全集 | [pan.baidu.com](https://pan.baidu.com/s/1nWOoV7uWI426z5uc-450tg) | `39b4` |
| **MVP 子集** | 5.3 GB | 4 天强对流 + 全部可视化 | [pan.baidu.com](https://pan.baidu.com/s/1oukwTGS5tLwVQYvtWFudng) | `0717` |
| **全集** | 106.15 GB | 2023 年 5–8 月全部 13 500 帧 | [pan.baidu.com](https://pan.baidu.com/s/1PyyRZ4wLqewo9FrtjhRpSQ) | `6c29` |

分享链接自 2026-06-20 起 **30 天有效**，过期后请 [联系维护者](#联系方式) 重新生成。

### 命令行下载

```bash
pip install bypy
bypy info     # 按浏览器提示完成授权
bypy downdir /pluvian-multimodal-dataset/full/
```

---

## 数据概览

| 属性 | 取值 |
|---|---|
| **区域** | 华北地区（经度 113.00°E – 120.00°E，纬度 36.00°N – 42.60°N） |
| **空间网格** | 661 × 701 像元，分辨率 0.01°（约 1 km） |
| **时间分辨率** | 6 分钟 |
| **覆盖时段** | 2023-05-01 至 2023-08-31（共 123 个自然日，94 天有有效雷达） |
| **总帧数** | 13 536 |
| **模态数** | 5 路物理观测 + 2 路再分析变量 = 7 路 |
| **单帧大小** | 约 8.6 MB（压缩 `.npz`，含 dense + sparse 数组 + 7 张灰度 PNG） |
| **全集体积** | 约 106 GB |

---

## 数据模态

每帧提供 7 路通道：前 5 路为物理观测，后 2 路为 925 hPa 的 ERA5 再分析。

| # | 名称（npz 键） | 来源 | 单位 | 原生形态 | 稠密形态 |
|---|---|---|---|---|---|
| 1 | `radar_mmh` | S 波段雷达拼图 | mm/h | 661 × 701 原生网格 | 相同 |
| 2 | `pwv_dense` / `pwv_sparse_*` | 176 个 GNSS 站点 | kg/m² | 稀疏站点，30 分钟 | IDW 插值 |
| 3 | `tem_dense` / `tem_sparse_*` | 289 个地面气象站 | °C | 稀疏站点，1 小时 | IDW 插值 |
| 4 | `rhu_dense` / `rhu_sparse_*` | 289 个地面气象站 | % | 稀疏站点，1 小时 | IDW 插值 |
| 5 | `prs_dense` / `prs_sparse_*` | 289 个地面气象站 | hPa | 稀疏站点，1 小时 | IDW 插值 |
| 6 | `era5_t_925` | ERA5 再分析 | K | 0.25° 网格，1 小时 | 双线性上采样 |
| 7 | `era5_q_925` | ERA5 再分析 | kg/kg | 0.25° 网格，1 小时 | 双线性上采样 |

雷达反射率（dBZ）到降水率（mm/h）的换算采用中国业务版 Z–R 关系
R = (Z / 300)^(1 / 1.4)。

逐模态的全局统计量（用于 `.png` 可视化）见
[`schema/normalize_stats.json`](schema/normalize_stats.json)。

---

## 文件结构

解压 `dataset_full.zip`（或 `dataset_mvp_v2.zip`）后得到：

```
dataset_for_team/                       (或 dataset_for_team_mvp/)
├── run_log.json                        流水线运行摘要
├── npz/                                ★ 训练就绪的数组
│   └── 2023-07-30T09-00-00.npz         每帧一个文件（8.6 MB）
└── png/                                逐模态 8-bit 灰度（可视化 + 作为图像训练用）
    ├── radar/                          雷达经 log1p + jet 配色后存为灰度
    ├── pwv_dense/
    ├── tem_station_dense/
    ├── rhu_station_dense/
    ├── prs_station_dense/
    ├── era5_t_925/
    └── era5_q_925/                     MVP 各 572 文件，全集各 13 500 文件
```

**MVP 压缩包**额外包含：

```
dataset_for_team_mvp/
├── mosaic/                             每帧 7 模态 + 元数据合成图（572 文件）
├── stations_overlay/                   雷达底图叠加 176 PWV + 289 地面站点位置
│                                       （3 个代表性强对流时刻）
└── samples/
    ├── case_2023-07-30_storm_evolution.pdf   8 时刻 × 7 模态的矢量时序图
    └── case_2023-07-30_radar.gif             40 帧雷达演变动画 @ 5 fps
```

各子集的目录清单镜像在
[`schema/directory_listing_mvp.txt`](schema/directory_listing_mvp.txt) 与
[`schema/directory_listing_full.txt`](schema/directory_listing_full.txt)。

---

## Schema (`.npz`)

每个 `.npz` 是一个压缩字典，包含以下键：

| 键 | 形状 | dtype | 单位 | 说明 |
|---|---|---|---|---|
| `timestamp` | `()`（标量） | `<U19` | ISO-8601 | 如 `'2023-07-30T09:00:00'` |
| `radar_mmh` | `(661, 701)` | `float32` | mm/h | 雷达反演的降水率 |
| `pwv_dense` | `(661, 701)` | `float32` | kg/m² | PWV 插值到网格 |
| `pwv_sparse_value` | `(176,)` | `float32` | kg/m² | 各站点 PWV 原始值 |
| `pwv_sparse_lonlat` | `(176, 2)` | `float32` | 度 | 站点坐标（经度, 纬度） |
| `pwv_sparse_mask` | `(176,)` | `float32` | 0/1 | 1 表示该站观测有效 |
| `tem_dense` | `(661, 701)` | `float32` | °C | 气温插值场 |
| `tem_sparse_value` | `(289,)` | `float32` | °C | 289 个地面站原始值 |
| `tem_sparse_mask` | `(289,)` | `float32` | 0/1 | 各站有效性 |
| `rhu_dense` | `(661, 701)` | `float32` | % | 相对湿度插值场 |
| `rhu_sparse_value` | `(289,)` | `float32` | % | 各站原始值 |
| `rhu_sparse_mask` | `(289,)` | `float32` | 0/1 | 各站有效性 |
| `prs_dense` | `(661, 701)` | `float32` | hPa | 地面气压插值场 |
| `prs_sparse_value` | `(289,)` | `float32` | hPa | 各站原始值 |
| `prs_sparse_mask` | `(289,)` | `float32` | 0/1 | 各站有效性 |
| `station_sparse_lonlat` | `(289, 2)` | `float32` | 度 | 地面站坐标（TEM/RHU/PRS 共用） |
| `era5_t_925` | `(661, 701)` | `float32` | K | ERA5 925 hPa 气温，上采样后 |
| `era5_q_925` | `(661, 701)` | `float32` | kg/kg | ERA5 925 hPa 比湿，上采样后 |

机器可读的 schema 见 [`schema/schema.json`](schema/schema.json)。

---

## 归一化统计

逐模态完整统计量（p2、p50、p98、min、max）由约 101 万采样像元统计得到，详见
[`schema/normalize_stats.json`](schema/normalize_stats.json)。关键数值：

| 模态 | p2 | p50 | p98 | 是否 log1p 预处理 |
|---|---:|---:|---:|---|
| 雷达 (mm/h) | 0.02 | 0.02 | 0.96 (log1p) | **是**（重尾分布） |
| PWV (kg/m²) | 9.07 | 33.97 | 67.50 | 否 |
| 地面气温 (°C) | 12.29 | 24.20 | 34.33 | 否 |
| 地面相对湿度 (%) | 19.13 | 69.83 | 97.72 | 否 |
| 地面气压 (hPa) | 853.01 | 980.60 | 1011.21 | 否 |
| ERA5 925 hPa 气温 (K) | 287.27 | 296.25 | 303.43 | 否 |
| ERA5 925 hPa 比湿 (kg/kg) | 0.0028 | 0.0113 | 0.0188 | 否 |

以上**仅用于可视化流水线**。模型训练时建议在自己的训练子集上做 per-batch 标准化。

---

## 数据切分

帧按自然日分组。切分标签与上游短临项目（`pipeline/manifest.csv`）一致：

| 切分 | 天数 | 帧数 | 说明 |
|---|---:|---:|---|
| `train` | 74 | 10 656 | 主训练集 |
| `val` | 8 | 1 152 | 验证集 |
| `test_robust` | 8 | 1 152 | 非强对流留出集 |
| `event_test` | 4 | 576 | **强对流过程日**（2023-07-29 – 08-01） |

逐切分的日期清单见 [`schema/manifest.csv`](schema/manifest.csv)。

**MVP** 压缩包仅包含 `event_test` 切分（4 个强对流日 × 144 帧 = 572 个文件，因 4 帧边界雷达缺测被剔除）。

---

## 空间范围

```
经度范围：113.00°E – 120.00°E（701 格 × 0.01°）
纬度范围： 36.00°N –  42.60°N（661 格 × 0.01°）
网格间距：约 1 km
```

每个像元的坐标可按下式重建：

```python
import numpy as np
lon = np.round(np.arange(113.00, 120.00 + 1e-6, 0.01), 2)  # 长度 701
lat = np.round(np.arange( 36.00,  42.60 + 1e-6, 0.01), 2)  # 长度 661
```

---

## 时间覆盖

- **时段**：2023-05-01 00:00 至 2023-08-31 23:54 UTC
- **间隔**：6 分钟（每天名义 144 帧）
- **帧时间戳**：`timestamp` 键中的 ISO-8601 字符串
- 因雷达数据质量问题剔除了 29 个自然日（详见 `run_log.json`）

---

## 方法说明

### 时间对齐
所有非雷达模态在时间维度线性插值到雷达的 6 分钟时间网格。PWV（30 分钟原生）在前后两帧之间线性插值；地面站（1 小时原生）同理；ERA5（1 小时原生）使用上游流水线的标准线性插值核（`pipeline.utils.linear_time_interp`）。

### 空间对齐
- 雷达本身就是 661 × 701 原生网格。
- PWV / 气温 / 湿度 / 气压采用反距离加权（IDW，k = 8 个邻居，幂指数 = 2）从站点插值到雷达网格。
- ERA5（0.25°）双线性上采样到 0.01°（`pipeline.utils.bilinear_interp_to_radar`）。

### 单位换算
雷达反射率经 R = (Z / 300)^(1/1.4) 换算成降水率，其中 Z = 10^(dBZ/10)。这是中国业务版 Z–R 关系。ERA5 字段保持原生单位（K，kg/kg）。

### 稀疏与稠密配对
对每路非雷达物理模态，数据集**同时**提供稠密插值场（`*_dense`）与底层稀疏站点观测（`*_sparse_value`、`*_sparse_lonlat`、`*_sparse_mask`）。用户可根据自己的模型选择对应表示。

### 可复现脚本
生成每帧数据的流水线作为上游 Pluvian 项目的一部分开源。详见 [引用](#引用) 段落。

---

## 使用须知（如实声明）

训练或解读结果前请务必阅读本节。

1. **稀疏到稠密的插值会引入人为结构。** 四路非雷达物理模态（PWV、TEM、RHU、PRS）按构造方式即在空间上平滑，因为是从站点观测插值出来的。远离站点的像元是插值得到的，不是观测得到的。若需要严格意义的观测真值，请使用 `*_sparse_value` / `*_sparse_lonlat`，而非 `*_dense`。

2. **ERA5 上采样不增信息。** ERA5 再分析在 925 hPa 的原生分辨率是 0.25°（约 25 km），双线性上采样到 1 km 后看似高分辨，但有效分辨率仍是 25 km。

3. **单雷达源、单一区域。** 雷达为华北业务 S 波段拼图，不验证向其他区域、非 5–8 月时段或其他雷达网的泛化能力。

4. **PNG 量化损失。** `.png` 文件是 8-bit 灰度，按 `normalize_stats.json` 中全数据集的 p2 / p98 做逐模态线性拉伸。仅供可视化和快速 sanity check，**不**建议作为主要训练目标，训练请使用 `.npz` 数组。

5. **分享链接 30 天过期。** 上述百度网盘链接有效期至 2026-07-20，过期后请 [联系维护者](#联系方式) 重新生成或申请更长期托管方案。

---

## 引用

如在学术工作中使用本数据集，请引用：

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

本数据集是 Pluvian 短临降水预报研究工作的配套产物。上游代码库在发布时仍为私有，如需访问请联系维护者。

---

## 许可证

数据集采用
[知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议（CC BY-NC-SA 4.0）](https://creativecommons.org/licenses/by-nc-sa/4.0/)
发布。

本数据集卡片以及仓库中的脚手架脚本采用 [MIT 许可证](LICENSE) 发布。

---

## 联系方式

维护者：**田锦煜（Tian Jinyu）**，北京航空航天大学第六学院
GitHub：[@Tanhhhhtjy](https://github.com/Tanhhhhtjy)

如遇 bug、链接失效或数据质量问题，请在本仓库提 Issue。
