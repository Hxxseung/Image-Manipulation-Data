import numpy as np
import cv2
from PIL import Image


def Binary(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Binary 변조

    다양한 이진화(Binarization) 기법을 적용하여 이미지를 흑백으로 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 고정 임계값 이진화 (Global Threshold, Threshold=127)
    level 2: Otsu 자동 임계값 이진화 (Otsu's Binarization)
    level 3: 적응형 이진화 - 평균 (Adaptive Threshold Mean)
    level 4: 적응형 이진화 - 가우시안 (Adaptive Threshold Gaussian)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    width, height = image.size

    # PIL Image -> Grayscale Numpy Array 변환
    target_gray = image.convert("L")
    img_gray = np.array(target_gray)

    # ========================================================
    # Level별 이진화(Binarization) 처리
    # ========================================================

    if level == 1:
        # 고정 임계값 이진화
        _, binary_array = cv2.threshold(
            img_gray, 127, 255, cv2.THRESH_BINARY
        )

    elif level == 2:
        # Otsu 알고리즘 기반 자동 임계값 이진화
        _, binary_array = cv2.threshold(
            img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

    elif level == 3:
        # 적응형 이진화 (Mean)
        binary_array = cv2.adaptiveThreshold(
            img_gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=2,
        )

    elif level == 4:
        # 적응형 이진화 (Gaussian)
        binary_array = cv2.adaptiveThreshold(
            img_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=2,
        )

    # ========================================================
    # RGB 변환 및 Resize 처리
    # ========================================================

    # 1채널 흑백 이미지를 3채널 RGB로 복원 후 PIL Image 생성
    binary_rgb = cv2.cvtColor(binary_array, cv2.COLOR_GRAY2RGB)
    binary_image = Image.fromarray(binary_rgb)

    resized = binary_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized