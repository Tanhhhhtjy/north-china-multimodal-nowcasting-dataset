"""Quick-start example: load one frame and visualise three modalities.

Run:
    pip install numpy matplotlib
    python load_single_frame.py path/to/2023-07-30T09-00-00.npz
"""
import sys
from pathlib import Path

import numpy as np


def main(npz_path: Path) -> None:
    """Load one frame, print summary, render a 3-modality preview if matplotlib is available."""
    data = np.load(npz_path, allow_pickle=True)

    print(f"=== {npz_path.name} ===")
    print(f"timestamp     : {data['timestamp']}")
    print(f"radar (mm/h)  : shape={data['radar_mmh'].shape} "
          f"min={data['radar_mmh'].min():.3f} max={data['radar_mmh'].max():.1f}")
    print(f"pwv (dense)   : shape={data['pwv_dense'].shape} "
          f"min={data['pwv_dense'].min():.2f} max={data['pwv_dense'].max():.2f} kg/m^2")
    print(f"pwv (sparse)  : {data['pwv_sparse_value'].shape[0]} stations, "
          f"{int(data['pwv_sparse_mask'].sum())} valid")
    print(f"tem (dense)   : shape={data['tem_dense'].shape} "
          f"min={data['tem_dense'].min():.1f} max={data['tem_dense'].max():.1f} C")
    print(f"rhu (dense)   : min={data['rhu_dense'].min():.1f} max={data['rhu_dense'].max():.1f} %")
    print(f"prs (dense)   : min={data['prs_dense'].min():.1f} max={data['prs_dense'].max():.1f} hPa")
    print(f"ERA5 t @ 925  : min={data['era5_t_925'].min():.1f} max={data['era5_t_925'].max():.1f} K")
    print(f"ERA5 q @ 925  : min={data['era5_q_925'].min():.5f} max={data['era5_q_925'].max():.5f} kg/kg")

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib not installed; skipping preview)")
        return

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(np.log1p(data['radar_mmh']), origin='lower',
                   extent=[113.0, 120.0, 36.0, 42.6], cmap='jet')
    axes[0].set_title('Radar (log1p mm/h)')

    axes[1].imshow(data['pwv_dense'], origin='lower',
                   extent=[113.0, 120.0, 36.0, 42.6], cmap='BrBG')
    axes[1].set_title('PWV (kg/m^2)')

    axes[2].imshow(data['era5_q_925'], origin='lower',
                   extent=[113.0, 120.0, 36.0, 42.6], cmap='viridis')
    axes[2].set_title('ERA5 q @ 925 hPa (kg/kg)')

    out = npz_path.with_suffix('.preview.png')
    plt.tight_layout()
    plt.savefig(out, dpi=100, bbox_inches='tight')
    print(f"\npreview saved -> {out}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python load_single_frame.py <path/to/frame.npz>")
    main(Path(sys.argv[1]))
