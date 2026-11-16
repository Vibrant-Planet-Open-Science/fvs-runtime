import hashlib
import json
import zipfile

import pytest

from pack import pack


@pytest.fixture
def bundle_path(tmp_path):
    """Lay out a one-variant fvs-build bundle built from `FS2026.3`."""
    bundle_path = tmp_path / "bundle"
    (bundle_path / "provenance" / "per-variant").mkdir(parents=True)
    (bundle_path / "provenance" / "manifest.json").write_text(
        json.dumps({"source": {"ref": "FS2026.3"}})
    )
    lib_path = bundle_path / "FVSzz.so"
    lib_path.write_bytes(b"not really a library")
    record = {
        "variant": "zz",
        "shared_library": lib_path.name,
        "shared_library_sha256": hashlib.sha256(
            lib_path.read_bytes()
        ).hexdigest(),
    }
    (bundle_path / "provenance" / "per-variant" / "FVSzz.json").write_text(
        json.dumps(record)
    )
    return bundle_path


def test_pack(bundle_path, tmp_path):
    wheel_path = pack(bundle_path, 1, "linux_x86_64", tmp_path / "dist")

    assert wheel_path.name == "fvs_runtime-2026.3.0.1-py3-none-linux_x86_64.whl"
    with zipfile.ZipFile(wheel_path) as zf:
        names = zf.namelist()
        meta = zf.read("fvs_runtime-2026.3.0.1.dist-info/WHEEL").decode()
    assert "fvs_runtime/lib/FVSzz.so" in names
    assert "fvs_runtime/provenance/FVSzz.json" in names
    assert "Root-Is-Purelib: false" in meta
    assert "Tag: py3-none-linux_x86_64" in meta


def test_refuses_library_that_differs_from_provenance(bundle_path, tmp_path):
    (bundle_path / "FVSzz.so").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="FVSzz.so: SHA-256"):
        pack(bundle_path, 0, "linux_x86_64", tmp_path / "dist")
