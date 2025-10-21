import pytest

from pathlib import Path

@pytest.fixture
def test_data_folder():
    data_folder = Path(__file__).parent.parent / "data"
    data_folder = data_folder.resolve()
    assert data_folder.exists() == True
    return data_folder

def test_present_mappings(test_data_folder):
    data_mappings = test_data_folder / "mappings_finalised.json"
    data_mappings = data_mappings.resolve()
    assert data_mappings.exists() == True

def test_present_towns(test_data_folder):
    data_towns = test_data_folder / "towns.txt"
    data_towns = data_towns.resolve()
    assert data_towns.exists() == True
