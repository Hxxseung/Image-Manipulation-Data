import random
from PIL import Image, ImageEnhance


def ColorJitter(image: Image.Image, level: int, aux_image: Image.Image = None, **kwargs) -> Image.Image:
    """
    ColorJitter 변조

    level 1~4에 따라 brightness, contrast, saturation, hue를 무작위로 변경한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 색상 무작위 변화 (변동 폭 ±10%, hue ±0.05)
    level 2: 약한 색상 무작위 변화 (변동 폭 ±20%, hue ±0.10)
    level 3: 중간 색상 무작위 변화 (변동 폭 ±30%, hue ±0.15)
    level 4: 강한 색상 무작위 변화 (변동 폭 ±40%, hue ±0.20)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 색상 변화 허용 강도
    jitter_limits = {
        1: (0.10, 0.05),
        2: (0.20, 0.10),
        3: (0.30, 0.15),
        4: (0.40, 0.20),
    }

    factor, hue_factor = jitter_limits[level]
    width, height = image.size

    # 재현성을 보장하면서도 무작위성을 부여하기 위한 시드 설정 (선택적 사용 가능)
    rng = random.Random()

    # 1. Brightness (밝기)
    b_factor = rng.uniform(1.0 - factor, 1.0 + factor)
    jittered = ImageEnhance.Brightness(image).enhance(b_factor)

    # 2. Contrast (대비)
    c_factor = rng.uniform(1.0 - factor, 1.0 + factor)
    jittered = ImageEnhance.Contrast(jittered).enhance(c_factor)

    # 3. Saturation (채도)
    s_factor = rng.uniform(1.0 - factor, 1.0 + factor)
    jittered = ImageEnhance.Color(jittered).enhance(s_factor)

    # 4. Hue (색상)
    if hue_factor > 0:
        h_shift = rng.uniform(-hue_factor, hue_factor)
        # HSV 모드로 변환하여 H(Hue) 채널 변형
        hsv_image = jittered.convert("HSV")
        h, s, v = hsv_image.split()
        
        # PIL의 H 채널은 0~255 범위
        h = h.point(lambda p: (p + int(h_shift * 255)) % 256)
        jittered = Image.merge("HSV", (h, s, v)).convert("RGB")

    resized = jittered.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized