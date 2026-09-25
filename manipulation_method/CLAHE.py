import numpy as np
import cv2
from PIL import Image


def CLAHE(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    CLAHE 변조

    Contrast Limited Adaptive Histogram Equalization을 적용하여 
    이미지의 국소 대비를 향상시킨 뒤 원래 이미지 크기로 resize한다.

    level 1: 약한 평탄화 (clipLimit = 2.0, grid = 8x8)
    level 2: 중간 평탄화 (clipLimit = 4.0, grid = 8x8)
    level 3: 강한 평탄화 (clipLimit = 6.0, grid = 16x16)
    level 4: 매우 강한 평탄화 (clipLimit = 10.0, grid = 16x16)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 CLAHE 파라미터 설정
    # ========================================================

    clahe_params = {
        1: {"clipLimit": 2.0, "tileGridSize": (8, 8)},
        2: {"clipLimit": 4.0, "tileGridSize": (8, 8)},
        3: {"clipLimit": 6.0, "tileGridSize": (16, 16)},
        4: {"clipLimit": 10.0, "tileGridSize": (16, 16)},
    }

    params = clahe_params[level]
    width, height = image.size

    # PIL Image -> Numpy (LAB 색상 공간 변환)
    # L(휘도) 채널에만 CLAHE를 적용하여 색상 왜곡 방지
    target_rgb = image.convert("RGB")
    img_array_rgb = np.array(target_rgb)
    img_lab = cv2.cvtColor(img_array_rgb, cv2.COLOR_RGB2LAB)

    l_channel, a_channel, b_channel = cv2.split(img_lab)

    # ========================================================
    # CLAHE 적용
    # ========================================================

    clahe_obj = cv2.createCLAHE(
        clipLimit=params["clipLimit"],
        tileGridSize=params["tileGridSize"]
    )
    cl_channel = clahe_obj.apply(l_channel)

    # 채널 병합 및 RGB 변환
    merged_lab = cv2.merge((cl_channel, a_channel, b_channel))
    clahe_rgb = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2RGB)

    clahe_image = Image.fromarray(clahe_rgb)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = clahe_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized