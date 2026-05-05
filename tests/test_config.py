from pathlib import Path

from jwst_galaxy_analysis.config import load_config


def test_load_config_resolves_paths(tmp_path):
    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    cfg_file = cfg_dir / "default.toml"
    cfg_file.write_text(
        """
[paths]
ceers_catalog = "data/ceers.fits"
uncover_catalog = "data/uncover.fits"
output_dir = "outputs"

[plotting]
figsize = [7.0, 5.0]
""",
        encoding="utf-8",
    )
    config = load_config(cfg_file)
    assert config.paths.ceers_catalog == (tmp_path / "data/ceers.fits").resolve()
    assert config.paths.uncover_catalog == (tmp_path / "data/uncover.fits").resolve()
    assert config.paths.output_dir == (tmp_path / "outputs").resolve()
    assert config.plotting.figsize == (7.0, 5.0)
