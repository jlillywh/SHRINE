from pathlib import Path

import pytest

from data.fileman import FileManager
from tests.path_fixtures import SRC_ROOT


@pytest.fixture
def file_manager(tmp_path: Path):
    data_dir = tmp_path / "data_external"
    data_dir.mkdir()
    (data_dir / "data.xlsx").write_text("test")
    return FileManager(data_dir), data_dir


class TestFileManager:
    def test_change_dir(self, file_manager):
        fm, _data_dir = file_manager
        fm.directory = SRC_ROOT / "geometry"
        assert fm.directory.exists()

    def test_file_does_not_exist(self, file_manager):
        fm, _data_dir = file_manager
        with pytest.raises(ValueError, match="not valid"):
            fm.add_file("data1.xlsx")

    def test_add_file(self, file_manager):
        fm, data_dir = file_manager
        file_name = "data.xlsx"
        fm.add_file(file_name)
        assert fm.get_file(file_name) == data_dir / file_name

    def test_get_file(self, file_manager):
        fm, data_dir = file_manager
        file_name = "data.xlsx"
        fm.add_file(file_name)
        assert fm.get_file(file_name) == data_dir / file_name

    def test_invalid_path(self, file_manager, tmp_path: Path):
        fm, _data_dir = file_manager
        invalid = tmp_path / "does-not-exist"
        with pytest.raises(Exception, match="does not exist"):
            fm.directory = invalid
