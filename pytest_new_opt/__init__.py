"""
pytest_new_opt - Enhanced pytest UI automation framework with custom fixtures and best practices.
"""

__version__ = "0.1.0"
__author__ = "walkzzz"
__email__ = "your-email@example.com"

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
