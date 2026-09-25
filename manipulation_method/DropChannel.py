import random
import numpy as np
from PIL import Image


def DropChannel(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    DropChannel 변조

    이미지의 color channel 중 일부를 무작위로 제거(0으로 변경)한 뒤
    원래 이미지 크기로 resize한다.

    level 1: R, G, B 중 1개 채널 무작위 제거 (가장 보편적)
    level 2: R, G, B 중 1개 채널 무작위 제거
    level 3: R, G, B 중 1~2개 채널 무작위 제거
    level 4: R, G, B 중 2개 채널 무작위 제거 (단일 채널만 남김)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    width, height = image.size

    # Target 이미지 numpy 배열 변환 (RGB)
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.uint8)

    # ========================================================
    # Level별 제거할 채널 수 결정 및 제거 처리
    # ========================================================

    # 채널 인덱스: 0 = Red, 1 = Green, 2 = Blue
    channels = [0, 1, 2]

    if level in {1, 2}:
        drop_count = 1
    elif level == 3:
        drop_count = random.choice([1, 2])
    else:  # level 4
        drop_count = 2

    # 무작위로 제거할 채널 인덱스 선택
    drop_indices = random.sample(channels, drop_count)

    # 선택된 채널의 값을 0으로 설정하여 제거
    for idx in drop_indices:
        img_array[:, :, idx] = 0

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    dropped_image = Image.fromarray(img_array)

    resized = dropped_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized