import random
import numpy as np
from PIL import Image


def ToneCurve(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    ToneCurve 변조

    Tone Curve(톤 커브)를 무작위로 조절하여 이미지의 밝고 어두운 영역을 변환한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 톤 변환 (최대 변형 폭 15)
    level 2: 약한 톤 변환 (최대 변형 폭 30)
    level 3: 중간 톤 변환 (최대 변형 폭 50)
    level 4: 강한 톤 변환 (최대 변형 폭 70)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 톤 커브 변형 강도(Max Offset) 설정
    # ========================================================

    intensity_map = {
        1: 15,
        2: 30,
        3: 50,
        4: 70,
    }

    max_offset = intensity_map[level]
    width, height = image.size

    # ========================================================
    # 무작위 LUT(Look-Up Table) 톤 커브 생성
    # ========================================================

    # 컨트롤 포인트 (0, 64, 128, 192, 255) 기준 offset 생성
    x_points = np.array([0, 64, 128, 192, 255], dtype=float)
    y_points = np.array(
        [
            0,
            64 + random.randint(-max_offset, max_offset),
            128 + random.randint(-max_offset, max_offset),
            192 + random.randint(-max_offset, max_offset),
            255,
        ],
        dtype=float,
    )

    # 0~255 범위를 벗어나지 않도록 클리핑
    y_points = np.clip(y_points, 0, 255)

    # 1차원 보간을 통해 256개 픽셀 값 매핑 LUT 작성
    x_all = np.arange(256)
    lut = np.interp(x_all, x_points, y_points).astype(np.uint8)

    # ========================================================
    # 톤 커브 LUT 적용
    # ========================================================

    target_rgb = image.convert("RGB")
    img_array = np.array(target_rgb)

    # LUT 적용
    curved_array = lut[img_array]
    curved_image = Image.fromarray(curved_array)

    # ========================================================
    # Resize 처리
    # ========================================================

    resized = curved_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized