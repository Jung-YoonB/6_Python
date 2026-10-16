"""
    한글 폰트, 출력 설정
"""
import platform

import matplotlib.pyplot as plt
from matplotlib import font_manager

# os 별 기본 한글 폰트
_CANDIDATES = {
    "Windows": ["Malgun Gothic"],
    "Darwin": ["AppleGothic"]
}

# 그 외의 후보 (리눅스, 도커 등)
_FALLBACK = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]

def find_korean_font():
    installed = {f.name for f in font_manager.fontManager.ttflist}

    for name in _CANDIDATES.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name

    return None

def setup(theme=True):
    # seaborn 테마를 적용할 때는 폰트 설정 전에 적용해야 함
    if theme:
        import seaborn as sns
        sns.set_theme(style="whitegrid")

    font = find_korean_font()
    if font:
        plt.rcParams["font.family"] = font

    # 마이너스 표시 설정
    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"
        