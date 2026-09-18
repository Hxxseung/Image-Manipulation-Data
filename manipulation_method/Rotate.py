from PIL import Image


def Rotate(image: Image.Image, level: int) -> Image.Image:
    """
    Rotate 변조

    level 1~4에 따라 회전 각도를 다르게 적용한다.
    (360도를 5등분한 기준, 72도씩 증가)

    level 1: 72도 회전
    level 2: 144도 회전
    level 3: 216도 회전
    level 4: 288도 회전
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 회전 각도 (72도씩 증가)
    angles = {
        1: 72,
        2: 144,
        3: 216,
        4: 288,
    }

    angle = angles[level]
    width, height = image.size

    # 이미지 회전 (expand=True로 잘림 방지, BICUBIC 보간법 적용)
    rotated = image.rotate(
        angle,
        resample=Image.Resampling.BICUBIC,
        expand=True
    )

    # 회전 후 커진 이미지를 원래 크기로 복원
    resized = rotated.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized