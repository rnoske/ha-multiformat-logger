import subprocess
import sys


def test_main_runs():
    result = subprocess.run([sys.executable, 'multiformat_logger/src/main.py', '--message', 'test', '--level', 'debug'], capture_output=True)
    assert result.returncode == 0
