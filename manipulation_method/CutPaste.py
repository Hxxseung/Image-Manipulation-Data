# 입력 이미지의 일부 영역을 잘라 이미지 내부의 다른 위치에 붙이는 CutPaste 변조 코드
# Randomly change two parts in an image. requires_aux": False
# pip install opencv-python scikit-image
# 2군데 붙임

from PIL import Image
import random


def CutPaste(
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

    patch_ratio = {
        1: 0.10,
        2: 0.15,
        3: 0.20,
        4: 0.25,
    }

    ratio = patch_ratio[level]

    patch_w = max(1, int(width * ratio))
    patch_h = max(1, int(height * ratio))
    
    # 두 개의 patch를 잘라 이미지 내부의 다른 위치에 붙임
    for _ in range(2):

        # 잘라낼 위치
        src_x = rng.randint(0, max(0, width - patch_w))
        src_y = rng.randint(0, max(0, height - patch_h))

        patch = image.crop(
            (
                src_x,
                src_y,
                src_x + patch_w,
                src_y + patch_h
            )
        )

        # 붙일 위치
        dst_x = rng.randint(0, max(0, width - patch_w))
        dst_y = rng.randint(0, max(0, height - patch_h))

        image.paste(
            patch,
            (dst_x, dst_y)
        )
        
    """
    # 잘라낼 위치
    src_x = rng.randint(0, max(0, width - patch_w))
    src_y = rng.randint(0, max(0, height - patch_h))

    patch = image.crop(
        (
            src_x,
            src_y,
            src_x + patch_w,
            src_y + patch_h
        )
    )

    # 붙일 위치
    dst_x = rng.randint(0, max(0, width - patch_w))
    dst_y = rng.randint(0, max(0, height - patch_h))

    image.paste(patch, (dst_x, dst_y)) """
    
    return image