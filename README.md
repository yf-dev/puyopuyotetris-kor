# 뿌요뿌요 테트리스 Steam PC 한국어 패치 스크립트

[뿌요뿌요 테트리스(Steam, PC)](https://store.steampowered.com/app/546050/Puyo_PuyoTetris/)의 한국어 패치 파일 생성을 위한 스크립트입니다.

@nickworonekin 님께서 작성한 많은 스크립트에 도움을 받았습니다. 감사합니다.

## 사용법

### 1. 사전 준비사항

- 본 스크립트는 Windows 10 x64 환경에서만 테스트되었습니다.
- 본 스크립트를 실행하기 위해서는 [닷넷 프레임워크](https://www.microsoft.com/net/download/dotnet-framework-runtime) 4.6 이상이 필요합니다.
- 본 스크립트는 패치 파일을 원본 게임 데이터를 통해 생성합니다. 생성 작업을 위해 최대 20GB의 디스크 용량이 필요할 수 있습니다.

### 2. 필요한 파일 다운로드

먼저 패치 스크립트를 다음 링크에서 다운로드합니다.

[다운로드](https://github.com/yf-dev/puyopuyotetris-kor/releases/download/v0.0.2/ppt-kor-v0.0.2.zip)

다운로드 받은 패치 스크립트의 압축을 해제한 후, `ppt-kor-v0.0.2\lib` 디렉터리로 이동합니다.
`ppt-kor-v0.0.2\lib` 디렉터리에는 본 스크립트에서 추가로 필요한 프로그램들을 다운받아두어야 합니다. 필요한 프로그램들의 다운로드 링크는 다음과 같습니다.

- [ImageMagick-7.0.7-38-portable-Q16-x86](http://ftp.icm.edu.pl/packages/ImageMagick/binaries/ImageMagick-7.0.7-38-portable-Q16-x86.zip)
- [Narchive-1.0.1](https://github.com/nickworonekin/narchive/releases/download/v1.0.1/Narchive-1.0.1.zip)
- [PuyoTextEditor-1.0.1](https://github.com/nickworonekin/puyo-text-editor/releases/download/v1.0.1/PuyoTextEditor-1.0.1.zip)
- [TppkTool-1.0.1](https://github.com/nickworonekin/tppk-tool/releases/download/v1.0.1/TppkTool-1.0.1.zip)


위 파일들을 모두 다운로드 받아서 압축을 해제하여 `ppt-kor-v0.0.2\lib` 디렉터리에 다음과 같이 배치해두어야 합니다.

```
- ppt-kor-v0.0.2
    - lib
        - ImageMagick-7.0.7-38-portable-Q16-x86
            convert.exe
            magic.xml
            ...

        - Narchive-1.0.1
            Narchive.exe
            ...

        - PuyoTextEditor-1.0.1
            MtxToJson.exe
            ...

        - TppkTool-1.0.1
            TppkTool.exe
            ...
    ...
```

그 다음, 적절한 한국어 번역 데이터를 다운로드합니다.

현재 [공동 번역 구글 스프레드 시트](https://docs.google.com/spreadsheets/d/1Kg2Jxd6kqH5cLxLITU3AF19ufxCvn4-H7m_DI5et4ZE)에서 번역 데이터를 공유하고 있습니다.
위 링크에 접속하여 `파일 > 다른 이름으로 다운로드 > 쉼표로 구분된 값(.csv, 현재시트)` 를 클릭하여 csv 파일을 다운로드합니다.

다운로드 받은 파일의 이름을 `pptko-translation - data.csv`로 변경하여 `ppt-kor-v0.0.2\data` 디렉터리 안에 배치하고, `pptko-translation - data.csv` 파일을 메모장 등 텍스트 편집 프로그램으로 열어 **첫 줄을 지우고 저장**합니다.
이 과정을 통해 파일의 첫 줄이 빈 문장이 아닌 `Key,English,Japanese` 로 시작하도록 해야합니다.

### 3. 원본 게임 데이터 변환

본 스크립트는 원본 데이터를 기반으로 한글 패치를 생성하므로, 원본 데이터를 한글 패치를 생성할 수 있도록 변환하는 과정을 처음에 거쳐야 합니다.

이를 위해 우선 원본 게임 데이터를 `ppt-kor-v0.0.2\data\original` 디렉터리에 복사해야합니다.

뿌요뿌요 테트리스가 설치된 디렉터리 (일반적으로 `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris`) 에서 `data_steam` 디렉터리를 복사하여 `ppt-kor-v0.0.2\data\original`에 붙여넣습니다.

붙여넣은 결과 디렉터리는 다음과 같아야 합니다.

```
- ppt-kor-v0.0.2
    - data
        - original
            - data_steam
                ...
        ...
    ...
```

이후 `ppt-kor-v0.0.2\init_original.bat` 파일을 더블 클릭하여 실행합니다.
변환 과정은 약 20분 정도 소요될 수 있습니다.

### 4. 패치 파일 생성

변환된 게임 데이터에서 한국어 패치 파일을 생성합니다.

(현재 이미지 파일의 한글 패치 자료는 제공하지 않습니다. 추후 제공을 결정할 예정입니다.)

먼저 다음 내용에 따라 디렉터리들을 복사합니다.
`ppt-kor-v0.0.2\data\original`의 일부 디렉터리를 같은 경로의 `ppt-kor-v0.0.2\data\font_data`로 복사하게 됩니다.

- `ppt-kor-v0.0.2\data\original\data_steam\data\dlc\addcont016` -> `ppt-kor-v0.0.2\data\font_data\data_steam\data\dlc\addcont016`
- `ppt-kor-v0.0.2\data\original\data_steam\data\dlc\addcont017` -> `ppt-kor-v0.0.2\data\font_data\data_steam\data\dlc\addcont017`
- `ppt-kor-v0.0.2\data\original\data_steam\data\dlc\addcont018` -> `ppt-kor-v0.0.2\data\font_data\data_steam\data\dlc\addcont018`
- `ppt-kor-v0.0.2\data\original\data_steam\data\tenp\text` -> `ppt-kor-v0.0.2\data\font_data\data_steam\data\tenp\text`

이후 `ppt-kor-v0.0.2\create_patch.bat` 파일을 더블 클릭하여 실행합니다.
변환 과정은 약 15분 정도 소요될 수 있습니다.

### 5. 패치 파일 적용

`ppt-kor-v0.0.2\data\generated` 디렉터리에 생성된 `data_steam` 디렉터리를 뿌요뿌요 테트리스가 설치된 디렉터리 (일반적으로 `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris`)의 `data_steam` 디렉터리에 덮어씌우면 패치가 적용됩니다.

패치 파일을 적용하시기 전에 원본 data_steam 디렉터리를 백업하시길 권장합니다.
