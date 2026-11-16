"""Tag the wheel for one platform; it carries native libraries."""

from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    """Set `Root-Is-Purelib: false` and a `py3-none-<platform>` tag."""

    def initialize(self, _version: str, build_data: dict[str, Any]) -> None:
        """Override hatchling's pure-Python defaults."""
        build_data["pure_python"] = False
        build_data["tag"] = f"py3-none-{self.config['platform-tag']}"
