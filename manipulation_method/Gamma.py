import random
import numpy as np
from PIL import Image


def Gamma(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Gamma 변조

    Power-law function을 적용하여 이미지 luminance를 변경한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 감마 변화 (gamma = 0.85 ~ 1.15)
    level 2: 약한 감마 변화 (gamma = 0.70 ~ 1.30)
    level 3: 중간 감마 변화 (gamma = 0.50 ~ 1.60)
    level 4: 강한 감마 변화 (gamma = 0.30 ~ 2.00)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 Gamma 범위 설정
    # ========================================================

    gamma_ranges = {
        1: (0.85, 1.15),
        2: (0.70, 1.30),
        3: (0.50, 1.60),
        4: (0.30, 2.00),
    }

    g_min, g_max = gamma_ranges[level]
    gamma_val = random.uniform(g_min, g_max)
    width, height = image.size

    # Target 이미지 numpy 배열 변환 (0~1 float32 범위 정규화)
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.float32) / 255.0

    # ========================================================
    # Power-law Transformation (Gamma Correction) 적용
    # ========================================================

    # Power-law 연산: I_out = I_in ^ gamma
    gamma_corrected = np.power(img_array, gamma_val)

    # 값 범위 클리핑 (0~255) 및 uint8 변환
    gamma_corrected = np.clip(gamma_corrected * 255.0, 0, 255).astype(np.uint8)

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    gamma_image = Image.fromarray(gamma_corrected)

    resized = gamma_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized