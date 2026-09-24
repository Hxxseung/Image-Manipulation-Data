from PIL import Image


def SplitRotate(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    SplitRotate 변조

    level 1~4에 따라 이미지를 분할한 후 
    각 영역별로 72도 단위 회전을 다르게 적용하고 원래 크기로 resize한다.

    level 1: 2분할, 1번 영역 72도 / 2번 영역 144도 회전
    level 2: 2분할, 1번 영역 144도 / 2번 영역 216도 회전
    level 3: 4분할, 각 영역 72도, 144도, 216도, 288도 회전
    level 4: 4분할, 각 영역 288도, 216도, 144도, 72도 회전
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 분할 수 및 각 영역 회전 각도 (72도 단위)
    configs = {
        1: {"splits": 2, "angles": [72, 144]},
        2: {"splits": 2, "angles": [144, 216]},
        3: {"splits": 4, "angles": [72, 144, 216, 288]},
        4: {"splits": 4, "angles": [288, 216, 144, 72]},
    }

    config = configs[level]
    num_splits = config["splits"]
    angles = config["angles"]

    width, height = image.size
    split_width = width // num_splits

    canvas = Image.new(image.mode, (width, height))

    for i in range(num_splits):
        # 분할 영역 설정 및 crop
        left = i * split_width
        right = width if i == num_splits - 1 else (i + 1) * split_width
        part = image.crop((left, 0, right, height))

        # 분할 조각 회전 (expand=True로 회전 시 영역 잘림 방지)
        part_rotated = part.rotate(
            angles[i],
            resample=Image.Resampling.BICUBIC,
            expand=True
        )

        # 회전된 조각을 해당 분할 크기에 맞게 resize 후 붙여넣기
        part_resized = part_rotated.resize(
            (right - left, height),
            Image.Resampling.LANCZOS
        )
        canvas.paste(part_resized, (left, 0))

    return canvas