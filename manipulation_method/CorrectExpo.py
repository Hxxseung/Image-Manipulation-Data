import random
import numpy as np
from PIL import Image


def CorrectExpo(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    CorrectExpo 변조

    이미지의 exposure(노출)를 보정한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 노출 보정 (EV = -0.3 ~ +0.3)
    level 2: 약한 노출 보정 (EV = -0.7 ~ +0.7)
    level 3: 중간 노출 보정 (EV = -1.2 ~ +1.2)
    level 4: 강한 노출 보정 (EV = -2.0 ~ +2.0)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 Exposure Value(EV) 조절 범위 설정
    # ========================================================

    ev_ranges = {
        1: (-0.3, 0.3),
        2: (-0.7, 0.7),
        3: (-1.2, 1.2),
        4: (-2.0, 2.0),
    }

    ev_min, ev_max = ev_ranges[level]
    ev_shift = random.uniform(ev_min, ev_max)
    width, height = image.size

    # Target 이미지 numpy 배열 변환 (float32)
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.float32)

    # ========================================================
    # Exposure Adjustment 적용 (Scale Factor = 2 ^ EV)
    # ========================================================

    # EV 변화에 따른 배율 계산 (예: +1 EV는 2배 밝게, -1 EV는 0.5배 밝게)
    scale_factor = 2.0 ** ev_shift
    exposed_array = img_array * scale_factor

    # 값 범위 클리핑 (0~255) 및 uint8 변환
    exposed_array = np.clip(exposed_array, 0, 255).astype(np.uint8)

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    exposed_image = Image.fromarray(exposed_array)

    resized = exposed_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized