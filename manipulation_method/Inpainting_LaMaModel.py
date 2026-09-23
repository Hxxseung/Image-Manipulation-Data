# LaMa pretrained model을 사용하여 선택된 hole 영역을 plausible content로 복원하는 Inpainting 코드
# pip install simple-lama-inpainting

from PIL import Image, ImageDraw
from simple_lama_inpainting import SimpleLama
import random
import math


_LAMA_MODEL = None


def _get_lama_model():
    """
    LaMa 모델을 최초 1회만 로드하고,
    이후에는 재사용한다.
    """
    global _LAMA_MODEL

    if _LAMA_MODEL is None:
        _LAMA_MODEL = SimpleLama()

    return _LAMA_MODEL


def _make_inpainting_mask(
    width: int,
    height: int,
    level: int,
    rng: random.Random
) -> Image.Image:
    """
    level에 따라 inpainting 대상 hole mask를 생성한다.

    - 검은색(0): 유지 영역
    - 흰색(255): inpainting 대상 영역
    """

    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # 전체 이미지 면적 대비 inpainting 대상 비율
    # LaMa를 쓰더라도 너무 크게 잡으면 웹툰에서는 부자연스러울 수 있어
    # 적당한 크기로 설정
    area_ratio = {
        1: 0.04,   # 2%
        2: 0.08,   # 4%
        3: 0.12,   # 6%
        4: 0.16,   # 8%
    }

    target_area = width * height * area_ratio[level]

    # level이 올라갈수록 hole 개수 증가
    num_shapes = {
        1: 1,
        2: 2,
        3: 3,
        4: 4,
    }[level]

    remaining_area = target_area

    for i in range(num_shapes):
        # 남은 면적을 남은 shape 수로 나눠 배분
        shape_area = remaining_area / (num_shapes - i)

        shape_type = rng.choice(["ellipse", "rectangle", "line"])

        if shape_type == "line":
            # watermark/선 가리기 느낌의 hole
            length = max(10, int(math.sqrt(shape_area) * rng.uniform(2.0, 3.5)))
            thickness = max(4, int(math.sqrt(shape_area) * 0.18))

            x1 = rng.randint(0, max(0, width - 1))
            y1 = rng.randint(0, max(0, height - 1))

            angle = rng.uniform(0, 2 * math.pi)

            x2 = int(x1 + length * math.cos(angle))
            y2 = int(y1 + length * math.sin(angle))

            # 이미지 범위 안으로 보정
            x2 = max(0, min(width - 1, x2))
            y2 = max(0, min(height - 1, y2))

            draw.line((x1, y1, x2, y2), fill=255, width=thickness)

        else:
            aspect = rng.uniform(0.6, 1.8)

            shape_w = max(12, int(math.sqrt(shape_area * aspect)))
            shape_h = max(12, int(math.sqrt(shape_area / aspect)))

            shape_w = min(shape_w, width)
            shape_h = min(shape_h, height)

            x1 = rng.randint(0, max(0, width - shape_w))
            y1 = rng.randint(0, max(0, height - shape_h))
            x2 = x1 + shape_w
            y2 = y1 + shape_h

            if shape_type == "ellipse":
                draw.ellipse((x1, y1, x2, y2), fill=255)
            else:
                radius = max(2, min(shape_w, shape_h) // 8)
                draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, fill=255)

        remaining_area -= shape_area

    return mask


def Inpainting(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    LaMa 기반 Inpainting 변조

    이미지의 region 또는 hole을 만든 뒤,
    pretrained LaMa 모델을 이용해 plausible content로 복원한다.

    정의:
    - 이미지의 region 또는 hole을 plausible content로 채움
    - 정보 은닉이나 visible watermark 제거에도 사용 가능

    level 기준:
    - 전체 이미지 면적 대비 inpainting 대상 hole 비율
    - level이 커질수록 hole의 총 면적과 개수가 증가
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    image = image.convert("RGB")

    # 재현성 보존
    base_seed = 0 if seed is None else seed
    rng = random.Random(base_seed + level * 1000)

    width, height = image.size

    # inpainting 대상 mask 생성
    mask = _make_inpainting_mask(
        width=width,
        height=height,
        level=level,
        rng=rng
    )

    # LaMa 모델 로드
    lama = _get_lama_model()

    # Inpainting 수행
    result = lama(image, mask)

    return result.convert("RGB")