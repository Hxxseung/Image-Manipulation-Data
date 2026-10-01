# 두 이미지를 patch grid로 나눈 뒤 번갈아 배치하여 interweave하는 PatchInter 코드
'''예시처럼 체커보드/격자 interweave 느낌이 강하게 보이도록 수정했습니다.
- level 기준: patch grid 밀도
  - 1 → 4×4
  - 2 → 6×6
  - 3 → 8×8
  - 4 → 10×10'''

from PIL import Image


def PatchInter(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:
    """
    PatchInter 변조

    두 이미지를 patch로 나눈 뒤
    checkerboard 방식으로 interweave한다.

    level 기준:
    - grid 크기
      level 1 -> 4x4
      level 2 -> 6x6
      level 3 -> 8x8
      level 4 -> 10x10
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    if aux_image is None:
        raise ValueError("PatchInter는 aux_image가 필요합니다.")

    image = image.convert("RGB")
    aux_image = aux_image.convert("RGB").resize(image.size)

    width, height = image.size

    grid_size = {
        1: 4,
        2: 6,
        3: 8,
        4: 10,
    }[level]

    cell_w = width // grid_size
    cell_h = height // grid_size

    result = Image.new("RGB", (width, height))

    for row in range(grid_size):
        for col in range(grid_size):
            left = col * cell_w
            top = row * cell_h
            right = width if col == grid_size - 1 else left + cell_w
            bottom = height if row == grid_size - 1 else top + cell_h

            source = image if (row + col) % 2 == 0 else aux_image
            patch = source.crop((left, top, right, bottom))
            result.paste(patch, (left, top))

    return result