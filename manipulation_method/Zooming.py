from PIL import Image, ImageOps


def Zooming(image: Image.Image, level: int) -> Image.Image:
    """
    Zooming 변조

    level 1~4에 따라 Zoom In/Out 배율을 다르게 적용한 뒤
    원래 이미지 크기로 resize한다.

    level 1: 미세 Zoom In (1.1배 확대 후 크롭)
    level 2: 중간 Zoom In (1.3배 확대 후 크롭)
    level 3: 미세 Zoom Out (0.8배 축소 후 검은 여백)
    level 4: 중간 Zoom Out (0.6배 축소 후 검은 여백)
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    width, height = image.size

    # level 1, 2: Zoom In (확대 후 중앙 크롭)
    if level in {1, 2}:
        factors = {1: 1.1, 2: 1.3}
        factor = factors[level]

        # 이미지 확대
        new_w, new_h = int(width * factor), int(height * factor)
        zoomed = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # 원래 크기로 중앙 크롭
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        right = left + width
        bottom = top + height

        cropped = zoomed.crop((left, top, right, bottom))
        return cropped

    # level 3, 4: Zoom Out (축소 후 패딩)
    else:
        factors = {3: 0.8, 4: 0.6}
        factor = factors[level]

        # 이미지 축소
        new_w, new_h = int(width * factor), int(height * factor)
        zoomed = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # 원래 크기 캔버스 중앙에 배치
        pad_w = (width - new_w) // 2
        pad_h = (height - new_h) // 2

        canvas = Image.new(image.mode, (width, height), color="black")
        canvas.paste(zoomed, (pad_w, pad_h))
        return canvas