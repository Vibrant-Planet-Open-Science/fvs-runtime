# fvs-runtime

fvs-runtime provides a thin Python package for distributing prebuilt shared libraries of the US variants of the [Forest Vegetation Simulator](https://github.com/USDAForestService/ForestVegetationSimulator) (FVS). It exists so FVS shared libraries can be easily installed with `pip` for major operating systems and can be pinned by version like any other dependency. 

fvs-runtime currently supports Linux x86_64 and aarch64 (glibc 2.28+), macOS arm64 (15.0+), and Windows x64. If you have another operating system or architecture not represented here, let us know by [raising an issue](https://github.com/Vibrant-Planet-Open-Science/fvs-runtime/issues).

fvs-runtime is minimal by design. It installs the FVS libraries and tells you where they are. That is all.  Running simulations, reading keyword files and other work with FVS belong in packages such as [fvs2py](https://github.com/Vibrant-Planet-Open-Science/fvs2py) and [rFVS](https://github.com/USDAForestService/ForestVegetationSimulator-Interface/tree/main/rFVS).


```sh
pip install fvs-runtime      # all 22 US variants
```

fvs-runtime relies upon [fvs-build](https://github.com/Vibrant-Planet-Open-Science/fvs-build) for reproducible workflows that build FVS from source. Binaries produced by fvs-build come with provenance info about the build which can be reported by fvs-runtime.

```python
import fvs_runtime

fvs_runtime.variants()  # ["pn", ...]
fvs_runtime.library_path("pn")  # Path to FVSpn.so (FVSpn.dll on Windows)
fvs_runtime.provenance("pn")  # fvs-build provenance for that library
```

## Use in Python (fvs2py)

Load an FVS shared library with [fvs2py](https://github.com/Vibrant-Planet-Open-Science/fvs2py), by having fvs-runtime locate the installed library for your variant of interest:

```python
import fvs_runtime
from fvs2py import FVS
from fvs2py.enums import FvsVariant

VARIANT = FvsVariant.PACIFIC_COAST

fvs = FVS(lib_path=fvs_runtime.library_path(VARIANT))
```

## Use in R (rFVS)

Install the same wheels with [reticulate](https://rstudio.github.io/reticulate/) (1.41+) and load the library with `rFVS`:

```r
variant <- "pn"

reticulate::py_require("fvs-runtime==2027.1.0.*")
lib <- reticulate::import("fvs_runtime")$library_path(variant)$as_posix()
rFVS::fvsLoad(fvsProgram = paste0("FVS", variant), bin = dirname(lib))
```

## Acknowledgment and disclaimer

FVS is developed and maintained by the USDA Forest Service, and this project builds on the source code and documentation the Forest Service publishes. fvs-runtime is an independent project of Vibrant Planet and is not affiliated with or endorsed by the USDA Forest Service. Any opinions, findings, conclusions, or recommendations expressed here are those of the authors and should not be construed to represent any official USDA or U.S. Government determination or policy. The use of trade or firm names is for reader information and does not imply endorsement by the U.S. Department of Agriculture of any product or service.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
