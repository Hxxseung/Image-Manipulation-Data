# Image Manipulation Data

이미지 변조 데이터 생성을 위한 코드입니다.

## Project Structure

```text
Image-Manipulation-Data/
├── config.py
├── manipulation_main1.py
├── mapping_loader.py
├── runner.py
├── manipulation_mapping/
│   ├── webtoon_mapping.py
│   └── webtoon_mapping.xlsx
├── manipulation_method/
│   └── ResizeCrop.py
├── data/
│   └── manipulation name/
│       └── generated_images.png
└── README.md
```

## Output Structure
예를 들어 ResizeCrop 변조를 적용한 경우:
```text
data_manipulation/
└── ResizeCrop/
│   ├── WT001_EP002_CUT001_origin.png
│   ├── WT001_EP002_CUT001_lv1.png
│   ├── WT001_EP002_CUT001_lv2.png
│   ├── WT001_EP002_CUT001_lv3.png
│   ├── WT001_EP002_CUT001_lv4.png
│   ├── ...
│   └── ...
```
![Generated images](./images/generated_images.png)

**변조 방법 스크립트**(예: `ResizeCrop.py`, `Flip.py`)는  
`manipulation_method/` 폴더에 추가해주세요.
`manipulation_method/` 폴더에는 최종적으로 약 **120개의 이미지 변조 방법**이 구현될 예정입니다.