# 전체 이미지 면적의 일정 비율에 해당하는 랜덤 영역을 지우는 Random Erasing 코드


from PIL import Image, ImageDraw
import random
import math


def Erasing(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB").copy()

    width, height = image.size

    # 전체 이미지 면적 대비 erase 영역 비율
    area_ratio = {
        1: 0.05,
        2: 0.10,
        3: 0.15,
        4: 0.20,  # 전체 이미지 면적의 약 20%를 erase
    }

    target_area = (
        width
        * height
        * area_ratio[level]
    )

    # 원본 aspect ratio를 고려한 patch 크기
    erase_w = int(
        math.sqrt(
            target_area * width / height
        )
    )

    erase_h = int(
        target_area / max(1, erase_w)
    )

    erase_w = min(width, max(1, erase_w))
    erase_h = min(height, max(1, erase_h))

    x = rng.randint(
        0,
        max(0, width - erase_w)
    )

    y = rng.randint(
        0,
        max(0, height - erase_h)
    )

    # Random Erasing 영역을 랜덤 색상으로 채움
    fill_color = (
        rng.randint(0, 255),
        rng.randint(0, 255),
        rng.randint(0, 255)
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(
        [
            x,
            y,
            x + erase_w,
            y + erase_h
        ],
        fill=fill_color
    )

    return image