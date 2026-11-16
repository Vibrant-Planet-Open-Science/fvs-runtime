"""Pack one fvs-build bundle into an fvs-runtime wheel."""

import argparse
import hashlib
import json
import shutil
import string
import subprocess
import tempfile
from pathlib import Path

from version import wheel_version

REPO_PATH = Path(__file__).resolve().parent.parent


def pack(
    bundle_path: Path, revision: int, platform_tag: str, out_dir_path: Path
) -> Path:
    """Build the fvs-runtime wheel for one fvs-build bundle.

    Args:
        bundle_path: Unpacked fvs-build bundle: `FVS<v>.<ext>` at the
            top, `provenance/` with `manifest.json` and `per-variant/`,
            and `sbom/fvs-native.spdx.json`.
        revision: fvs-runtime revision `R`; the rest of the version
            comes from the upstream tag the bundle was built from.
        platform_tag: Wheel platform tag before repair, e.g.
            `linux_x86_64`, `macosx_15_0_arm64` or `win_amd64`.
        out_dir_path: Directory the wheel is written to.

    Returns:
        Path to the wheel, tagged `py3-none-<platform_tag>`.

    Raises:
        ValueError: The bundle was not built from an FVS release tag, a
            library's SHA-256 differs from its provenance, or the wheel
            is larger than PyPI's 100 MB limit.
    """
    provenance_path = bundle_path / "provenance"
    manifest = json.loads(
        (provenance_path / "manifest.json").read_text(encoding="utf-8")
    )
    version = wheel_version(manifest["source"]["ref"], revision)

    with tempfile.TemporaryDirectory() as tmp_dir:
        stage_path = Path(tmp_dir)
        package_path = stage_path / "fvs_runtime"
        (package_path / "lib").mkdir(parents=True)
        shutil.copy(
            REPO_PATH / "src" / "fvs_runtime" / "__init__.py", package_path
        )
        shutil.copytree(
            provenance_path / "per-variant", package_path / "provenance"
        )
        for record_path in sorted(
            (provenance_path / "per-variant").glob("*.json")
        ):
            record = json.loads(record_path.read_text(encoding="utf-8"))
            lib_path = bundle_path / record["shared_library"]
            with lib_path.open("rb") as f:
                digest = hashlib.file_digest(f, "sha256").hexdigest()
            if digest != record["shared_library_sha256"]:
                msg = (
                    f"{lib_path.name}: SHA-256 {digest} differs from provenance"
                )
                raise ValueError(msg)
            shutil.copy(lib_path, package_path / "lib")

        for relative_path in (
            "README.md",
            "LICENSE",
            "templates/hatch_build.py",
        ):
            shutil.copy(REPO_PATH / relative_path, stage_path)
        shutil.copy(bundle_path / "sbom" / "fvs-native.spdx.json", stage_path)
        template = (
            REPO_PATH / "templates" / "fvs-runtime.pyproject.toml"
        ).read_text(encoding="utf-8")
        (stage_path / "pyproject.toml").write_text(
            string.Template(template).substitute(
                version=version, platform_tag=platform_tag
            ),
            encoding="utf-8",
        )
        subprocess.run(
            ["uv", "build", "--wheel", "--out-dir", out_dir_path, stage_path],
            check=True,
        )

    wheel_path = (
        out_dir_path / f"fvs_runtime-{version}-py3-none-{platform_tag}.whl"
    )
    if wheel_path.stat().st_size > 100 * 1024**2:
        msg = f"{wheel_path.name} is over PyPI's 100 MB limit"
        raise ValueError(msg)
    return wheel_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_path", type=Path)
    parser.add_argument("revision", type=int)
    parser.add_argument("platform_tag")
    args = parser.parse_args()
    pack(args.bundle_path, args.revision, args.platform_tag, Path("dist"))
