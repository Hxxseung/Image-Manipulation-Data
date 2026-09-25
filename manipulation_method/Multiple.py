import random
import numpy as np
from PIL import Image


def Multiple(
    image: Image.Image,
    level: int,
    aux_image: Image.Image = None,
    **kwargs
) -> Image.Image:
    """
    Multiple 변조

    distribution에서 추출한 random 값을 image pixel 값에 곱한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 곱셈 노이즈 (std = 0.05)
    level 2: 약한 곱셈 노이즈 (std = 0.10)
    level 3: 중간 곱셈 노이즈 (std = 0.20)
    level 4: 강한 곱셈 노이즈 (std = 0.30)
    """

    # ========================================================
    # 입력 확인
    # ========================================================

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # ========================================================
    # Level별 분포 노이즈 표준편차(std) 설정
    # ========================================================

    std_map = {
        1: 0.05,
        2: 0.10,
        3: 0.20,
        4: 0.30,
    }

    std = std_map[level]
    width, height = image.size

    # Target 이미지 numpy 배열 변환 (float32)
    target = image.convert("RGB")
    img_array = np.array(target, dtype=np.float32)

    # ========================================================
    # Distribution(정규분포) 기반 Random Multipliers 생성 및 적용
    # ========================================================

    # 평균 1.0, 표준편차 std를 갖는 가우시안 랜덤 분포에서 픽셀별 스케일 계수 추출
    noise_distribution = np.random.normal(1.0, std, size=img_array.shape)

    # Pixel 값에 random factor 곱하기
    multiplied_array = img_array * noise_distribution

    # 값 범위 클리핑 (0~255) 및 uint8 변환
    multiplied_array = np.clip(multiplied_array, 0, 255).astype(np.uint8)

    # ========================================================
    # PIL Image 변환 및 Resize
    # ========================================================

    multiplied_image = Image.fromarray(multiplied_array)

    resized = multiplied_image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized