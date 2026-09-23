# 동일 이미지를 여러 개의 tile로 반복 배치하여 반복 패턴 이미지를 생성하는 코드

# 동일 이미지를 무작위 rows×cols 형태로 여러 번 축소·반복 배치하는 Repeat 변조 코드

from PIL import Image
import random


def Repeat(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    width, height = image.size

    # level별 반복 grid 크기 범위
    # 값이 커질수록 동일 이미지가 더 많이 반복됨
    grid_range = {
        1: (1, 2),
        2: (2, 3),
        3: (2, 4),
        4: (3, 5),
    }

    min_grid, max_grid = grid_range[level]

    # 가로/세로 반복 개수를 각각 무작위 선택
    rows = rng.randint(min_grid, max_grid)
    cols = rng.randint(min_grid, max_grid)

    # 최소 2개 이상 반복되도록 보정
    if rows == 1 and cols == 1:
        cols = 2

    tile_w = max(1, width // cols)
    tile_h = max(1, height // rows)

    # 원본 이미지를 각 cell 크기에 맞게 축소
    tile = image.resize(
        (tile_w, tile_h),
        Image.Resampling.LANCZOS
    )

    result = Image.new(
        "RGB",
        (width, height)
    )

    # 동일 이미지를 반복 배치
    for row in range(rows):
        for col in range(cols):

            x = col * tile_w
            y = row * tile_h

            # 마지막 행/열의 남는 pixel까지 채우기 위한 크기 보정
            current_w = (
                width - x
                if col == cols - 1
                else tile_w
            )

            current_h = (
                height - y
                if row == rows - 1
                else tile_h
            )

            current_tile = tile.resize(
                (current_w, current_h),
                Image.Resampling.LANCZOS
            )

            result.paste(
                current_tile,
                (x, y)
            )

    return result

'''
from PIL import Image


def Repeat(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    image = image.convert("RGB")

    width, height = image.size

    # 한 방향의 반복 개수
    grid_size = {
        1: 2,
        2: 3,
        3: 4,
        4: 5,
    }[level]

    tile_w = max(1, width // grid_size)
    tile_h = max(1, height // grid_size)

    tile = image.resize((tile_w, tile_h))

    result = Image.new("RGB", (width, height))

    for row in range(grid_size):
        for col in range(grid_size):
            result.paste(
                tile,
                (col * tile_w, row * tile_h)
            )

    return result
'''