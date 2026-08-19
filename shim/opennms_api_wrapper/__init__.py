"""Deprecated alias for the ``opennms`` package (python-opennms)."""
import sys
import warnings

import opennms
import opennms.types

from opennms import *  # noqa: F401,F403
from opennms import __version__  # noqa: F401

sys.modules[__name__ + ".types"] = opennms.types

warnings.warn(
    "opennms-api-wrapper has been renamed to python-opennms; "
    "use 'import opennms' instead of 'import opennms_api_wrapper'.",
    DeprecationWarning,
    stacklevel=2,
)
