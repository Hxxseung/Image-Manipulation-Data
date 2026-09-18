from PIL import Image


def GeometricTransform(image: Image.Image, level: int) -> Image.Image:
    """
    GeometricTransform 변조

    level 1~4에 따라 기하학적 변환(Geometric transformation)을 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세한 이동 및 전단 변환 (2% Shift, 2° Shear)
    level 2: 약한 이동 및 회전 변환 (5% Shift, 5° Rotation)
    level 3: 중간 복합 기하학 변환 (8% Shift, 8° Shear & Rotation)
    level 4: 강한 복합 기하학 변환 (12% Shift, 15° Shear & Rotation)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    width, height = image.size

    # level별 기하학 변환 행렬(Affine Transform) 매개변수 설정
    # (a, b, c, d, e, f) -> x' = ax + by + c, y' = dx + ey + f
    if level == 1:
        # 미세한 엑스/와이축 평행이동 및 비틀림
        affine_matrix = (1.0, 0.03, -width * 0.02, 0.03, 1.0, -height * 0.02)
    elif level == 2:
        # 약한 회전 및 이동
        affine_matrix = (0.98, 0.05, -width * 0.03, -0.05, 0.98, height * 0.02)
    elif level == 3:
        # 중간 수준의 전단 및 회전 복합 변환
        affine_matrix = (0.95, 0.10, -width * 0.05, -0.08, 0.95, -height * 0.03)
    elif level == 4:
        # 강한 복합 기하학적 왜곡
        affine_matrix = (0.90, 0.20, -width * 0.08, -0.15, 0.90, -height * 0.05)

    transformed = image.transform(
        (width, height),
        Image.AFFINE,
        affine_matrix,
        Image.Resampling.BICUBIC
    )

    resized = transformed.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized