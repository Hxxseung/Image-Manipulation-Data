import random
from PIL import Image


def Dislocation(image: Image.Image, level: int) -> Image.Image:
    """
    Dislocation 변조

    level 1~4에 따라 image patch의 분할 개수 및 위치 변경(swap) 비율을 
    다르게 적용한 뒤 원래 이미지 크기로 resize한다.

    level 1: 2x2 패치, 2개 패치 무작위 위치 변경
    level 2: 3x3 패치, 4개 패치 무작위 위치 변경
    level 3: 4x4 패치, 8개 패치 무작위 위치 변경
    level 4: 5x5 패치, 12개 패치 무작위 위치 변경
    """

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    # level별 패딩/격자 분할 수 및 섞을 패치 수 설정
    configs = {
        1: {"grid": 2, "swaps": 2},
        2: {"grid": 3, "swaps": 4},
        3: {"grid": 4, "swaps": 8},
        4: {"grid": 5, "swaps": 12},
    }

    config = configs[level]
    grid_size = config["grid"]
    num_swaps = config["swaps"]

    width, height = image.size
    patch_w = width // grid_size
    patch_h = height // grid_size

    # 1. 패치 잘라내기
    patches = []
    positions = []
    for i in range(grid_size):
        for j in range(grid_size):
            left = i * patch_w
            top = j * patch_h
            right = width if i == grid_size - 1 else (i + 1) * patch_w
            bottom = height if j == grid_size - 1 else (j + 1) * patch_h
            
            box = (left, top, right, bottom)
            patch = image.crop(box)
            
            patches.append(patch)
            positions.append(box)

    # 2. 지정된 개수만큼 패치 위치 무작위 셔플 (Dislocation)
    shuffled_patches = patches.copy()
    swap_indices = random.sample(range(len(patches)), min(num_swaps, len(patches)))
    shuffled_selected = [shuffled_patches[idx] for idx in swap_indices]
    random.shuffle(shuffled_selected)

    for idx, new_patch in zip(swap_indices, shuffled_selected):
        shuffled_patches[idx] = new_patch

    # 3. 캔버스에 재배치
    canvas = Image.new(image.mode, (width, height))
    for patch, box in zip(shuffled_patches, positions):
        w = box[2] - box[0]
        h = box[3] - box[1]
        resized_patch = patch.resize((w, h), Image.Resampling.LANCZOS)
        canvas.paste(resized_patch, (box[0], box[1]))

    resized = canvas.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    return resized