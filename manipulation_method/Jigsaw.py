# 이미지를 작은 조각으로 나누고 퍼즐처럼 흰 간격을 둔 채 재배치하는 Jigsaw 코드
'''
level 기준: grid 크기- 1 → 6×6
- 2 → 7×7
- 3 → 8×8
- 4 → 9×9'''

# 원본 이미지의 위치 관계는 유지하면서 각 영역을 jigsaw puzzle 조각 형태로 표현하는 코드

from PIL import Image, ImageDraw
import random


def _make_jigsaw_mask(
    width: int,
    height: int,
    row: int,
    col: int,
    grid_size: int,
    rng: random.Random
) -> Image.Image:
    """
    각 cell 크기에 맞는 jigsaw 형태의 mask를 생성한다.
    """

    mask = Image.new(
        "L",
        (width, height),
        0
    )

    draw = ImageDraw.Draw(mask)

    # 조각 사이의 작은 간격
    margin = max(
        1,
        int(min(width, height) * 0.05)
    )

    draw.rectangle(
        (
            margin,
            margin,
            width - margin - 1,
            height - margin - 1
        ),
        fill=255
    )

    # 퍼즐 돌출부 크기
    radius = max(
        2,
        int(min(width, height) * 0.13)
    )

    cx = width // 2
    cy = height // 2

    # 위쪽 tab
    if row > 0:
        if (row + col) % 2 == 0:
            draw.ellipse(
                (
                    cx - radius,
                    0,
                    cx + radius,
                    2 * radius
                ),
                fill=255
            )

    # 아래쪽 tab
    if row < grid_size - 1:
        if (row + col) % 2 == 1:
            draw.ellipse(
                (
                    cx - radius,
                    height - 2 * radius,
                    cx + radius,
                    height
                ),
                fill=255
            )

    # 왼쪽 tab
    if col > 0:
        if (row + col) % 2 == 1:
            draw.ellipse(
                (
                    0,
                    cy - radius,
                    2 * radius,
                    cy + radius
                ),
                fill=255
            )

    # 오른쪽 tab
    if col < grid_size - 1:
        if (row + col) % 2 == 0:
            draw.ellipse(
                (
                    width - 2 * radius,
                    cy - radius,
                    width,
                    cy + radius
                ),
                fill=255
            )

    return mask


def Jigsaw(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    Jigsaw 변조

    이미지를 여러 cell로 나누되,
    각 cell의 원래 위치는 그대로 유지한다.

    각 영역을 jigsaw puzzle 조각처럼 표현한다.

    level 기준:
    - puzzle 조각 개수
      level 1 -> 6x6
      level 2 -> 8x8
      level 3 -> 10x10
      level 4 -> 12x12
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError(
            "level은 1~4 중 하나여야 합니다."
        )

    rng = random.Random(seed)

    image = image.convert("RGB")

    width, height = image.size

    grid_size = {
        1: 6,
        2: 8,
        3: 10,
        4: 12,
    }[level]

    cell_w = width // grid_size
    cell_h = height // grid_size

    # 흰 배경
    result = Image.new(
        "RGB",
        (width, height),
        (255, 255, 255)
    )

    for row in range(grid_size):

        for col in range(grid_size):

            left = col * cell_w
            top = row * cell_h

            right = (
                width
                if col == grid_size - 1
                else left + cell_w
            )

            bottom = (
                height
                if row == grid_size - 1
                else top + cell_h
            )

            patch = image.crop(
                (
                    left,
                    top,
                    right,
                    bottom
                )
            )

            patch_w, patch_h = patch.size

            mask = _make_jigsaw_mask(
                patch_w,
                patch_h,
                row,
                col,
                grid_size,
                rng
            )

            result.paste(
                patch,
                (left, top),
                mask
            )

    return result