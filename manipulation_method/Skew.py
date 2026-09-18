from PIL import Image
import math


def Skew(image: Image.Image, level: int) -> Image.Image:
    """
    Skew 변조

    level 1~4에 따라 이미지 비틀기(Skew) 강도를 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세하게 비틀기 (각도 2.5도)
    level 2: 약하게 비틀기 (각도 5도)
    level 3: 중간으로 비틀기 (각도 10도)
    level 4: 강하게 비틀기 (각도 15도)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 비틀기 각도 (도)
    skew_angles = {
        1: 2.5,
        2: 5,
        3: 10,
        4: 15,
    }

    angle_deg = skew_angles[level]
    angle_rad = math.radians(angle_deg)
    
    width, height = image.size

    # Affine 변환 행렬 계수 계산 (X축 방향 Skew)
    # (1, tan(a), 0, 0, 1, 0)
    coeffs = (1, math.tan(angle_rad), 0, 0, 1, 0)

    # 이미지 비틀기 (expand=True로 잘림 방지)
    skewed = image.transform(
        (width * 2, height),  # 비틀기로 커질 영역을 감안해 임시로 크기 확장
        Image.AFFINE,
        coeffs,
        Image.Resampling.BICUBIC
    )

    # 비틀기 후 커진 이미지를 원본 크기로 복원
    resized = skewed.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized