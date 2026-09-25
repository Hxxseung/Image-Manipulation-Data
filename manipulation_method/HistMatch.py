import random
import numpy as np
from PIL import Image


def HistMatch(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    HistMatch 변조

    이미지 histogram을 random histogram에 맞도록 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 히스토그램 변형 (약한 스타일 변화)
    level 2: 약한 히스토그램 변형
    level 3: 중간 히스토그램 변형
    level 4: 강한 히스토그램 변형 (강한 톤/대비 변화)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 히스토그램 왜곡 강도 범위 설정 (Gamma 조절 폭)
    # ========================================================

    gamma_ranges = {
        1: (0.85, 1.15),
        2: (0.70, 1.30),
        3: (0.50, 1.60),
        4: (0.30, 2.00),
    }

    g_min, g_max = gamma_ranges[level]
    width, height = image.size

    # Target 이미지 numpy 배열 변환
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.uint8)

    # ========================================================
    # Random Target Histogram 및 Lookup Table(LUT) 생성
    # ========================================================

    # 각 채널(R, G, B)별로 랜던 감마 기반의 임의 히스토그램 LUT 생성
    matched_array = np.zeros_like(img_array)

    for ch in range(3):
        channel_data = img_array[:, :, ch]

        # 1. 원본 채널의 누적 분포 함수(CDF) 계산
        hist_src, _ = np.histogram(channel_data.flatten(), 256, [0, 256])
        cdf_src = hist_src.cumsum()
        cdf_src = cdf_src / cdf_src[-1]  # 정규화

        # 2. Random Target Histogram 생성을 위한 가상 분포(CDF) 빌드
        random_gamma = random.uniform(g_min, g_max)
        x = np.linspace(0, 1, 256)
        cdf_target = np.power(x, random_gamma)
        cdf_target = cdf_target / cdf_target[-1]

        # 3. CDF 매핑을 통한 Lookup Table(LUT) 매칭
        lookup_table = np.interp(cdf_src, cdf_target, np.arange(256))

        # 4. 원본 픽셀 값 매핑
        matched_array[:, :, ch] = lookup_table[channel_data].astype(np.uint8)

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    matched_image = Image.fromarray(matched_array)

    resized = matched_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized