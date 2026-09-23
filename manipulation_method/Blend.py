# 두 이미지를 level별 transparency 비율로 겹쳐 하나의 blended image를 생성하는 코드
# 지금 하나의 이미지를 가지고 Blend 함. 다양한 이미지(random)하게 뽑아 썪자.  1: (0.10, 0.20),에서 왼,오 숫자 의미? 뭐가 원본??

from PIL import Image
import random


def Blend(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_image is None:
        raise ValueError("Blend는 aux_image가 필요합니다.")

    rng = random.Random(seed)

    image = image.convert("RGB")
    aux_image = aux_image.convert("RGB").resize(image.size)

    # 최종 이미지에서 aux_image가 차지하는 transparency 비율
    alpha_range = {
        1: (0.05, 0.14),  # aux_image가 10~20% 정도만 섞이도록 랜덤하게 뽑는다는 뜻
        2: (0.15, 0.24),
        3: (0.25, 0.34),
        4: (0.35, 0.45),
    } # 0.5를 넘기지 않는 이유는 그러면 원본보다 aux 이미지가 더 지배적이 되기 때문

    alpha = rng.uniform(*alpha_range[level])

    return Image.blend(image, aux_image, alpha)