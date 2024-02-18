import os

# Ensure running as root
if not os.getuid() == 0:
    raise SystemExit("Error: Must Run As Root")


from .config import Config
from .create import create
from .remove import remove

__all__ = ["Config", "create", "remove"]
