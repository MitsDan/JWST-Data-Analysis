import pytest

from jwst_galaxy_analysis.validation import require_columns


class MiniTable:
    colnames = ["a", "b"]


def test_require_columns_passes():
    require_columns(MiniTable(), ["a"], context="mini")


def test_require_columns_raises_for_missing():
    with pytest.raises(ValueError, match="Missing required columns"):
        require_columns(MiniTable(), ["a", "c"], context="mini")
