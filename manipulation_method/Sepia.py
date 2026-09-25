import numpy as np
from PIL import Image


def Sepia(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Sepia 변조

    이미지를 sepia style(세피아 톤)로 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 약한 세피아 효과 (25% 혼합)
    level 2: 중간 세피아 효과 (50% 혼합)
    level 3: 강한 세피아 효과 (75% 혼합)
    level 4: 완전한 세피아 효과 (100% 혼합)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 세피아 혼합 비율(Blend Factor) 설정
    # ========================================================

    blend_factors = {
        1: 0.25,
        2: 0.50,
        3: 0.75,
        4: 1.00,
    }

    factor = blend_factors[level]
    width, height = image.size

    # PIL Image -> Numpy (float 타입으로 변환)
    target_rgb = image.convert("RGB")
    img_array = np.array(target_rgb, dtype=np.float32)

    # ========================================================
    # Standard Sepia Matrix 적용
    # ========================================================

    # 세피아 변환 행렬
    # R' = 0.393R + 0.769G + 0.189B
    # G' = 0.349R + 0.686G + 0.168B
    # B' = 0.272R + 0.534G + 0.131B
    sepia_matrix = np.array(
        [
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131],
        ]
    )

    # 행렬 곱으로 세피아 톤 계산
    sepia_array = np.dot(img_array, sepia_matrix.T)
    sepia_array = np.clip(sepia_array, 0, 255)

    # level 강도에 따른 원본과 세피아 이미지 블렌딩
    blended_array = (1 - factor) * img_array + factor * sepia_array
    blended_array = np.clip(blended_array, 0, 255).astype(np.uint8)

    sepia_image = Image.fromarray(blended_array)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = sepia_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized