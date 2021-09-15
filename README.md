# 뿌요뿌요 테트리스 Steam PC 한국어 패치

[![GitHub](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/yf-dev/puyopuyotetris-kor/blob/master/LICENSE)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/yf-dev/puyopuyotetris-kor.svg)](https://github.com/yf-dev/puyopuyotetris-kor/releases/latest)

![뿌요뿌요 테트리스 인트로 스크린샷](./screenshots/20181105221920_1.jpg)

[뿌요뿌요 테트리스(Steam, PC)](https://store.steampowered.com/app/546050/Puyo_PuyoTetris/)의 한국어 패치 파일 생성을 위한 스크립트입니다.

[@nickworonekin](https://github.com/nickworonekin) 님께서 작성한 많은 스크립트에 도움을 받았습니다. 감사합니다.

## 패치 다운로드 및 적용방법

1. 아래 패치 다운로드 링크에서 가장 최신의 `build-<날짜>.zip` 파일을 다운로드합니다.
2. 뿌요뿌요 테트리스가 설치된 디렉터리 (일반적으로 `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris`)로 이동합니다.
3. `data_steam\data` 디렉터리에 `build-<날짜>.zip` 파일의 압축 내용을 풀어 덮어 씌웁니다.

잘 모르겠으면, `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris\data_steam\data` 폴더에 `build-<날짜>.zip` 압축 파일 내용을 덮어 씌우면 됩니다.

[![패치 다운로드 링크](./download_link.png)](https://drive.google.com/drive/folders/1c9Dh3m79d_8HRg6tLMiDx4zzu8h0J5fY)

## 자주 묻는 질문

- Q1. 텍스트 앞에 `[1024]` 같이 이상한 숫자가 붙어서 나와요.
- A1. 패치 다운로드시 `build-<날짜>-debug.zip` 말고 `build-<날짜>.zip` 를 받아서 다시 패치하세요.
<!-- -->

## 스크린샷

![뿌요뿌요 테트리스 스크린샷 1](./screenshots/20181105221931_1.jpg)
![뿌요뿌요 테트리스 스크린샷 2](./screenshots/20181105221952_1.jpg)
![뿌요뿌요 테트리스 스크린샷 3](./screenshots/20181105222421_1.jpg)
![뿌요뿌요 테트리스 스크린샷 4](./screenshots/20181105222447_1.jpg)
![뿌요뿌요 테트리스 스크린샷 5](./screenshots/20181105222542_1.jpg)
![뿌요뿌요 테트리스 스크린샷 6](./screenshots/20181105222646_1.jpg)

## 직접 패치 생성 방법

아래의 내용은 직접 패치 파일을 처음부터 생성하기 위한 방법을 안내합니다.

(단순히 패치를 다운로드받아 적용하실 분들은 무시해주세요.)

### 1. 사전 준비사항

- 본 스크립트는 Windows 10 x64 환경에서만 테스트되었습니다.
- 본 스크립트를 실행하기 위해서는 파이썬 3.6 이상과 [Pipenv](https://github.com/pypa/pipenv)이 필요합니다.
- 본 스크립트를 실행하기 위해서는 [닷넷 프레임워크](https://www.microsoft.com/net/download/dotnet-framework-runtime) 4.6 이상이 필요합니다.
- 본 스크립트는 패치 파일을 원본 게임 데이터를 통해 생성합니다. 생성 작업을 위해 많은 디스크 용량이 필요할 수 있습니다.
- 본 스크립트를 처음부터 정상적으로 구동하기 위해서는 Nintendo Switch로 발매된 `뿌요뿌요 테트리스 S`의 데이터가 필요합니다.
- 텍스트 패치 이외의 이미지 패치는 본 프로젝트로 작업이 가능하지만, 패치를 위해 한국어로 수정한 이미지 데이터는 저작권 문제로 제공하지 않습니다.


### 2. 필요한 파일 다운로드 및 빌드 환경 준비

먼저 패치 스크립트(`ppt-kor.zip`)를 다음 링크에서 다운로드합니다.

[다운로드 페이지](https://github.com/yf-dev/puyopuyotetris-kor/releases/latest)

다운로드 받은 패치 스크립트의 압축을 해제한 후, `ppt-kor\lib` 디렉터리로 이동합니다.
`ppt-kor\lib` 디렉터리에는 본 스크립트에서 추가로 필요한 프로그램들을 다운받아두어야 합니다. 필요한 프로그램들의 다운로드 링크는 다음과 같습니다.

- [BNTX Extractor (master)](https://github.com/aboood40091/BNTX-Extractor/archive/master.zip)
- [ImageMagick-7.0.7-38-portable-Q16-x86](http://ftp.icm.edu.pl/packages/ImageMagick/binaries/ImageMagick-7.0.7-38-portable-Q16-x86.zip)
- [Narchive-1.0.1](https://github.com/nickworonekin/narchive/releases/download/v1.0.1/Narchive-1.0.1.zip)
- [PuyoTextEditor-1.0.1](https://github.com/nickworonekin/puyo-text-editor/releases/download/v1.0.1/PuyoTextEditor-1.0.1.zip)
- [QuickBMS generic files extractor and reimporter 0.9.0](https://aluigi.altervista.org/papers/quickbms.zip)
- [TppkTool-1.0.1](https://github.com/nickworonekin/tppk-tool/releases/download/v1.0.1/TppkTool-1.0.1.zip)
- [Wintee 1.0.1](https://github.com/WinLAFS/wintee/releases/download/v1.0.1/wtee.exe)


위 파일들을 모두 다운로드 받아서 압축을 해제하여 `ppt-kor\lib` 디렉터리에 다음과 같이 배치해두어야 합니다.

```
- ppt-kor
    - lib
        - BNTX-Extractor-master
            bntx_extract.py
            ...

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

        - quickbms
            quickbms.exe
            ...

        - TppkTool-1.0.1
            TppkTool.exe
            ...

        - wtee.exe
    ...
```

위와 같이 폴더가 준비됬다면, 텍스트 생성에 사용할 폰트 파일을 다운로드 받아야 합니다.
`ppt-kor\data\fonts` 디렉터리로 이동하고, 다음 링크에서 `빙그레체`(`빙그레체II` 아님)의 OTF 파일을 다운로드받습니다.

[빙그레 글꼴](http://www.bing.co.kr/story/contribute_font)

다운로드 받은 OTF 파일 중 `빙그레체 Bold`의 OTF 파일을 `ppt-kor\data\fonts\Binggrae-Bold.otf` 경로에 붙여넣습니다.

이후, pipenv를 정상적으로 설치한 후 명령 프롬프트를 열고 `ppt-kor` 폴더로 이동합니다.

그리고 다음 명령어를 통해 라이브러리를 설치하고, 스크립트의 실행을 준비합니다.

```
pipenv install
pipenv shell
```

그 다음, 적절한 한국어 번역 데이터를 다운로드합니다.

현재 [구글 스프레드 시트](https://docs.google.com/spreadsheets/d/1HfH5lQ81PYhAqj4qZVMdPtWC0zNBN78greQpCvs_g2A)에서 번역 데이터를 공유하고 있습니다.
위 링크에 접속하여 `파일 > 다른 이름으로 다운로드 > 쉼표로 구분된 값(.csv, 현재시트)` 를 클릭하여 csv 파일을 다운로드합니다.

다운로드 받은 파일의 이름을 `pptko-text - data.csv`로 변경하여 `ppt-kor\data` 디렉터리 안에 배치합니다.

### 3. 원본 게임 데이터 변환

본 스크립트는 원본 데이터를 기반으로 한글 패치를 생성하므로, 원본 데이터를 한글 패치를 생성할 수 있도록 변환하는 과정을 처음에 거쳐야 합니다.

원본 스팀 게임 데이터는 `ppt-kor\data\steam_data` 디렉터리에 복사해야 합니다.

뿌요뿌요 테트리스가 설치된 디렉터리 (일반적으로 `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris`) 에서 `data_steam\data` 디렉터리의 내용을 복사하여 `ppt-kor\data\steam_data`에 붙여넣습니다.

원본 스위치 게임 데이터는 `ppt-kor\data\switch_romfs` 디렉터리에 복사해야 합니다.

적절하게 덤프된 스위치 롬 카트리지의 `romfs`를 `ppt-kor\data\switch_romfs`에 붙여넣습니다.

붙여넣은 결과 디렉터리는 다음과 같아야 합니다.

```
- ppt-kor
    - data
        - steam_data
            - academy
            - adventure
            - arcade_select
            ...
        - switch_romfs
            - academy
            - adventure
            - arcade_select
            ...
        - "pptko-text - data.csv"
        ...
    ...
```

이후 `ppt-kor\extract_steam_all.bat`와 `extract_switch_all.bat` 명령을 pipenv shell이 구동중인 명령 프롬프트에서 실행합니다.
변환 과정은 약 40분 정도 소요될 수 있습니다.

### 4. 패치 파일 생성

변환된 게임 데이터에서 한국어 패치 파일을 생성합니다.

이를 위해 `ppt-kor\create_font_patch.bat`와 `ppt-kor\create_image_patch.bat` 명령을 pipenv shell이 구동중인 명령 프롬프트에서 실행합니다.
변환 과정은 약 30분 정도 소요될 수 있습니다.

### 5. 패치 파일 적용

`ppt-kor\data\build` 디렉터리와 `ppt-kor\data\build-images`에 생성된 디렉터리들을 뿌요뿌요 테트리스가 설치된 디렉터리 (일반적으로 `C:\Program Files (x86)\Steam\steamapps\common\PuyoPuyoTetris`)의 `data_steam\data` 디렉터리 내부에 덮어씌우면 패치가 적용됩니다.

패치 파일을 적용하시기 전에 원본 `data_steam` 디렉터리를 백업하시길 권장합니다.

## License

본 프로젝트는 [MIT License](./LICENSE) 하에 제공됩니다.
