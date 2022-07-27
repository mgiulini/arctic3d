from pathlib import Path

import pytest

from arctic3d.modules.pdb import (
    fetch_pdbrenum,
    get_best_pdb,
    keep_atoms,
    occ_pdb,
    selchain_pdb,
    tidy_pdb,
    validate_api_hit,
)

from . import golden_data


@pytest.fixture
def inp_pdb():
    return Path(golden_data, "1rypB_r_b.pdb")


def test_fetch_pdbrenum():
    pdb = fetch_pdbrenum("1crn")
    assert pdb.exists()
    pdb.unlink()


def test_selchain_pdb(inp_pdb):
    pdb = selchain_pdb(inp_pdb, "B")
    assert pdb.exists()
    pdb.unlink()


def test_tidy_pdb(inp_pdb):
    pdb = tidy_pdb(inp_pdb)
    assert pdb.exists()
    pdb.unlink()


def test_occ_pdb(inp_pdb):
    pdb = occ_pdb(inp_pdb)
    assert pdb.exists()
    pdb.unlink()


def test_keep_atoms(inp_pdb):
    pdb = keep_atoms(inp_pdb)
    assert pdb.exists()
    pdb.unlink()


def test_validate_api_hit():
    hit = {
        "end": 951,
        "chain_id": "A",
        "pdb_id": "2gsx",
        "start": 1,
        "unp_end": 971,
        "coverage": 0.939,
        "unp_start": 21,
        "resolution": None,
        "experimental_method": "X-ray solution scattering",
        "tax_id": 9606,
    }

    pdb, dict = validate_api_hit([hit])
    assert pdb is None
    assert dict is None

    hit["resolution"] = 1.0
    pdb, dict = validate_api_hit([hit])
    assert pdb.name == "2gsx.pdb"
    assert dict == hit


def test_get_best_pdb():
    pdb = get_best_pdb("P20023")
    assert pdb is None