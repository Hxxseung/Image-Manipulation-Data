# 한 이미지의 여러 부분을 서로 다른 크기로 잘라 랜덤하게 배치하는 PartsCollage 코드
'''예시처럼 같은 이미지의 여러 부분이 서로 다른 크기로 겹치며 collage되게 바꿨습니다.
이전 grid 방식보다 예시에 더 가깝습니다.
- level 기준:
  - 사용할 patch 개수 증가
  - patch 크기 다양성 증가'''

# 한 이미지의 서로 다른 random 부분을 crop하여 빈 공간 없는 직사각형 collage로 재배치하는 코드

from PIL import Image
import random


def PartsCollage(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    PartsCollage 변조

    하나의 이미지에서 서로 다른 random region을 crop한 뒤,
    모든 cell을 채워 하나의 rectangular collage를 생성한다.

    level 기준:
    - collage grid 크기
      level 1 -> 2x2
      level 2 -> 3x3
      level 3 -> 4x4
      level 4 -> 5x5
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError(
            "level은 1~4 중 하나여야 합니다."
        )

    rng = random.Random(seed)

    image = image.convert("RGB")

    width, height = image.size

    grid_size = {
        1: 2,
        2: 3,
        3: 4,
        4: 5,
    }[level]

    cell_w = width // grid_size
    cell_h = height // grid_size

    result = Image.new(
        "RGB",
        (width, height)
    )

    for row in range(grid_size):

        for col in range(grid_size):

            # ----------------------------------------
            # 원본 이미지에서 random crop 크기 설정
            # cell보다 약간 큰 영역을 random crop
            # ----------------------------------------

            crop_scale = rng.uniform(
                1.0,
                2.0
            )

            crop_w = min(
                width,
                max(
                    cell_w,
                    int(cell_w * crop_scale)
                )
            )

            crop_h = min(
                height,
                max(
                    cell_h,
                    int(cell_h * crop_scale)
                )
            )

            # ----------------------------------------
            # 원본에서 random 위치 선택
            # ----------------------------------------

            src_x = rng.randint(
                0,
                max(
                    0,
                    width - crop_w
                )
            )

            src_y = rng.randint(
                0,
                max(
                    0,
                    height - crop_h
                )
            )

            patch = image.crop(
                (
                    src_x,
                    src_y,
                    src_x + crop_w,
                    src_y + crop_h
                )
            )

            # ----------------------------------------
            # collage cell 크기로 resize
            # ----------------------------------------

            target_left = (
                col * cell_w
            )

            target_top = (
                row * cell_h
            )

            target_w = (
                width - target_left
                if col == grid_size - 1
                else cell_w
            )

            target_h = (
                height - target_top
                if row == grid_size - 1
                else cell_h
            )

            patch = patch.resize(
                (
                    target_w,
                    target_h
                ),
                Image.Resampling.LANCZOS
            )

            # ----------------------------------------
            # 빈 공간 없이 rectangular collage에 배치
            # ----------------------------------------

            result.paste(
                patch,
                (
                    target_left,
                    target_top
                )
            )

    return result