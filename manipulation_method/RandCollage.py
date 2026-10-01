# level별로 6장, 7장, 9장, 10장의 이미지를 사용하여 rectangular collage를 생성하는 RandCollage 코드

from PIL import Image
import random


def _random_crop(
    img: Image.Image,
    rng: random.Random,
    crop_scale_range=(0.6, 1.0)
) -> Image.Image:
    """
    이미지에서 random crop을 수행한다.
    """
    img = img.convert("RGB")
    width, height = img.size

    scale = rng.uniform(*crop_scale_range)

    crop_w = max(1, int(width * scale))
    crop_h = max(1, int(height * scale))

    x = rng.randint(0, max(0, width - crop_w))
    y = rng.randint(0, max(0, height - crop_h))

    return img.crop((x, y, x + crop_w, y + crop_h))


def _get_layout_boxes(width: int, height: int, level: int):
    """
    level에 따라 collage box들을 반환한다.

    반환값:
    - [(left, top, right, bottom), ...]
    """

    if level == 1:
        # 6장 = 2 x 3
        rows, cols = 2, 3
        boxes = []

        cell_w = width // cols
        cell_h = height // rows

        for row in range(rows):
            for col in range(cols):
                left = col * cell_w
                top = row * cell_h
                right = width if col == cols - 1 else left + cell_w
                bottom = height if row == rows - 1 else top + cell_h
                boxes.append((left, top, right, bottom))

        return boxes

    elif level == 2:
        # 7장 = irregular rectangular layout
        # 2 x 4 느낌이지만 마지막 줄에서 하나를 크게 사용
        w1 = width // 4
        w2 = width // 2
        h1 = height // 2

        boxes = [
            # 윗줄 4개
            (0, 0, w1, h1),
            (w1, 0, 2 * w1, h1),
            (2 * w1, 0, 3 * w1, h1),
            (3 * w1, 0, width, h1),

            # 아랫줄 3개
            (0, h1, w2, height),
            (w2, h1, w2 + w1, height),
            (w2 + w1, h1, width, height),
        ]
        return boxes

    elif level == 3:
        # 9장 = 3 x 3
        rows, cols = 3, 3
        boxes = []

        cell_w = width // cols
        cell_h = height // rows

        for row in range(rows):
            for col in range(cols):
                left = col * cell_w
                top = row * cell_h
                right = width if col == cols - 1 else left + cell_w
                bottom = height if row == rows - 1 else top + cell_h
                boxes.append((left, top, right, bottom))

        return boxes

    elif level == 4:
        # 10장 = 2 x 5
        rows, cols = 2, 5
        boxes = []

        cell_w = width // cols
        cell_h = height // rows

        for row in range(rows):
            for col in range(cols):
                left = col * cell_w
                top = row * cell_h
                right = width if col == cols - 1 else left + cell_w
                bottom = height if row == rows - 1 else top + cell_h
                boxes.append((left, top, right, bottom))

        return boxes

    else:
        raise ValueError("level은 1~4 중 하나여야 합니다.")


def RandCollage(
    image: Image.Image,
    level: int,
    aux_images: list[Image.Image] | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    RandCollage 변조

    level별로 서로 다른 개수의 image를 사용하여 collage를 생성한다.

    level 기준:
    - level 1 -> 6장
    - level 2 -> 7장
    - level 3 -> 9장
    - level 4 -> 10장

    최소 절반은 원본 이미지에서,
    나머지는 random aux image에서 가져온다.
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_images is None or len(aux_images) == 0:
        raise ValueError("RandCollage는 aux_images가 필요합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    width, height = image.size

    boxes = _get_layout_boxes(width, height, level)
    total_cells = len(boxes)

    # 최소 절반 이상을 원본 이미지에서 사용
    num_original_cells = total_cells // 2
    if total_cells % 2 != 0:
        num_original_cells += 1

    original_positions = set(
        rng.sample(range(total_cells), k=num_original_cells)
    )

    crop_scale_range = {
        1: (0.80, 1.00),
        2: (0.70, 0.95),
        3: (0.60, 0.90),
        4: (0.50, 0.85),
    }[level]

    result = Image.new("RGB", (width, height), (255, 255, 255))

    for idx, (left, top, right, bottom) in enumerate(boxes):

        target_w = right - left
        target_h = bottom - top

        if idx in original_positions:
            patch = _random_crop(
                image,
                rng,
                crop_scale_range=crop_scale_range
            )
        else:
            aux_img = rng.choice(aux_images).convert("RGB")
            patch = _random_crop(
                aux_img,
                rng,
                crop_scale_range=crop_scale_range
            )

        patch = patch.resize(
            (target_w, target_h),
            Image.Resampling.LANCZOS
        )

        result.paste(patch, (left, top))

    return result