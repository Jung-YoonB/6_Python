"""
    차트 관련 설정
"""
import platform
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager

# ========================
#   한글 폰트
# ========================
# 운영체제(OS) 별로 기본 한글 폰트 (기본적으로 설치되어 있는 항목들)
_DEFAULT_FONT = {
    "Windows" : ["Malgun Gothic"],
    "Darwin" : ["AppleGothic"],         # platform.system() 의 결과가 macOS 부르는 명칭
}

# 그 외의 폰트들 (리눅스, 도커 등등)
_FALLBACK = ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]

def find_korean_font():
    """
    설치 된 폰트 중 한글을 표시할 수 있는 항목을 찾아 반환
    """
    # font_manager.fontManager.ttflist : matplotlib 에서 시스템을 훑어 만들어 둔 설치 된 폰트 목록
    installed = {f.name for f in font_manager.fontManager.ttflist}
    #   => set 구조로 폰드명 목록을 저장

    # 리스트 + 리스트 => 리스트
    for name in _DEFAULT_FONT.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name

    return None

# ========================
#   차트 이미지 저장 경로
# ========================
OUTPUT_DIR = Path(__file__).with_name("output")

def out(name):
    """ output/ 폴더 내의 파일 경로 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True)
    # 해당 경로가 존재하지 않으면 생성, 존재하면 넘어감(exist_ok=True)
    return OUTPUT_DIR / name

def saved_files():
    """ output/ 폴더에 저장 된 파일 이름 목록 반환 """
    OUTPUT_DIR.mkdir(exist_ok=True)

    # iterdir() : 폴더 안을 하나씩 돌면서 반환
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())

# ========================
#   설정
# ========================
def setup(theme=True):
    """
        한글 폰트 설정, 마이너스 기호 설정
            - seaborn 의 테마 설정을 먼저 해야 함
        Args:
            theme : seaborn 테마 설정 여부
    """
    if theme:
        # seaborn 테마 설정
        #   -> seaborn 이 설치 되지 않은 경우가 있을 수 있어, import를 if문 내부에 작성
        import seaborn as sns
        sns.set_theme(style="whitegrid")

    # 한글 폰트 설정
    font = find_korean_font()
    if font:
        # plt.rcParams  : 전역 기본값 표(dict)
        plt.rcParams["font.family"] = font

    # 마이너스 기호 설정
    plt.rcParams["axes.unicode_minus"] = False

    # 그래프 저장 시 축 라벨이 잘리는 현상 해결(방지)
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"