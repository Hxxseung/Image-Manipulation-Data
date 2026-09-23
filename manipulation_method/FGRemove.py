# OpenCV GrabCut으로 foreground를 추정한 뒤 해당 영역을 제거하는 코드
# 조금만 더 살려볼까??

from PIL import Image
import numpy as np
import cv2


def FGRemove(
    image: Image.Image,
    level: int,
    aux_image: Image.Image | None = None,
    seed: int | None = None
) -> Image.Image:

    if level not in {1, 2, 3, 4}:
        raise ValueError("level은 1~4 중 하나여야 합니다.")

    image = image.convert("RGB")

    arr = np.array(image)
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

    height, width = bgr.shape[:2]

    # 이미지 가장자리 일부를 background라고 가정ㅔㅑㅔ 
    margin_ratio = {
        1: 0.20, # 가장자리 20% 제외
        2: 0.15, # 가장자리 15% 제외
        3: 0.10, # 가장자리 10% 제외
        4: 0.05,
    }

    margin = margin_ratio[level]

    x = int(width * margin)
    y = int(height * margin)

    rect = (
        x,
        y,
        max(1, width - 2 * x),
        max(1, height - 2 * y)
    )

    mask = np.zeros((height, width), np.uint8)

    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    cv2.grabCut(
        bgr,
        mask,
        rect,
        bg_model,
        fg_model,
        5,
        cv2.GC_INIT_WITH_RECT
    )

    foreground_mask = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        1,
        0
    ).astype(np.uint8)

    result = arr.copy()

    # foreground를 흰색으로 제거
    result[foreground_mask == 1] = [255, 255, 255]

    return Image.fromarray(result)