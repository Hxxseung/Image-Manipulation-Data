import random
from PIL import Image, ImageOps


def ChangeChan(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    ChangeChan 변조

    level 1~4에 따라 이미지의 RGB channel을 무작위로 shift, swap 또는 invert한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 채널 무작위 Swap (순서 재배치)
    level 2: 채널 무작위 Invert (일부 채널 반전)
    level 3: 채널 무작위 Shift 및 Swap (픽셀 위치 이동 + 순서 재배치)
    level 4: 복합 변형 (Shift, Swap, Invert 전면 적용)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    width, height = image.size
    rng = random.Random()

    # RGB 채널 분리
    r, g, b = image.split()
    channels = [r, g, b]

    # 1. Invert (채널 반전)
    if level in {2, 4}:
        # level 2는 1~2개 채널 반전, level 4는 2~3개 채널 반전
        invert_count = rng.randint(1, 2) if level == 2 else rng.randint(2, 3)
        target_indices = rng.sample(range(3), invert_count)
        for idx in target_indices:
            channels[idx] = ImageOps.invert(channels[idx])

    # 2. Shift (채널 픽셀 공간 이동)
    if level in {3, 4}:
        max_shift = int(width * (0.02 if level == 3 else 0.05))
        shifted_channels = []
        for ch in channels:
            dx = rng.randint(-max_shift, max_shift)
            dy = rng.randint(-max_shift, max_shift)
            # 채널별 평행이동 변환
            shifted_ch = ch.transform(
                (width, height),
                Image.AFFINE,
                (1, 0, dx, 0, 1, dy),
                Image.Resampling.BICUBIC
            )
            shifted_channels.append(shifted_ch)
        channels = shifted_channels

    # 3. Swap (채널 순서 재배치)
    if level in {1, 3, 4}:
        rng.shuffle(channels)

    # 채널 병합
    changed_image = Image.merge("RGB", channels)

    resized = changed_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized