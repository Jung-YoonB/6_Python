"""
    공통 설정
"""
from pathlib import Path

ENCODING = 'utf-8-sig'

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def path(name):
    return DATA_DIR / name