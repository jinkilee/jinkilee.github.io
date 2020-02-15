1. linux 설치
아래의 경로를 목적에 맞게 설정해주어야 함.

설치 목적에 따른 OS 설치 위치
--------------
- 개인서버: SSD/HDD 관계 없음
- ML서버: 고속 데이터 access가 필요하다면 OS는 HDD에 설치하기를 권장
- 웹/DB서버:
- 개발서버: SSD/HDD 관계 없음
단, swap 영역이 SSD에 mount되지 않도록 주의해야 함.

포멧 및 파티션 생성
--------------
부팅 과정에서는 파티션을 자유롭게 할 수 없기 때문에 mount 포인트 설정 작업을 하기 전에 파티션을 해결하는 것이 좋다.([**link**](https://ubuntu.com/tutorials/try-ubuntu-before-you-install#2-boot-from-dvd) 참고) 실제 설치 전에 GUI/Shell 등을 통해 `fdisk` 명령어를 이용해서 파티션을 해야한다.

shell에서 포멧하는 방법과 파티션하는 방법은 아래와 같다.
- 포멧
```
sudo mkfs.ext4 -f /dev/XXX
```
- 파티션: [**link**](https://www.manualfactory.net/10607) 참고

파티션 설정
--------------
아래 폴더에 대해서 ext4 파일 시스템으로 파티션해주자. 
`/boot=512M`
`/=32G`
`/boot/efi=256M` (`EFI boot partition`을 선택하면 됨. 따로 fs type이 지정되지 않음)
`/home=32G`
`(optional)/opt=512G`
위의 설정을 끝낸 후 남은 파티션은 mount point를 지정하지 말고 ext4로 포맷만시켜두고, OS 설치 후에 따로 mount해줄 것. mount하는 명령어는 아래와 같다.
```
sudo fdisk /dev/XXX /폴더
```

이후 해야할 것들
--------------
- static IP로 설정
- 아래의 tool 설치
```
apt-get install ssh
apt-get install net-tools
apt-get install git
apt-get install vim
apt-get install curl
```
- 아래의 alias 등록
```
alias old='cd ${OLDPWD}'
alias wd='grep -R'
alias fn='find ./ -name'
alias vi='vim'
```

CUDA 설치
--------------
모니터를 GPU 슬롯에서 제거하고 `reboot`후에 아래의 내용을 수행하자.
[**cuda.sh**](https://github.com/jinkilee/jinkilee.github.io/blob/master/script/ubuntu/cuda.sh)를 이용해서 CUDA를 설치할 수 있다.
위 스크립트 상단에 CUDA 10.1 설치를 위한 기본 값이 설정돼 있다. 다른 버전을 설치하고자 할 경우, 관련 폴더명 또는 파일명을 적절하게 변경해서 사용해야 함.
- cuda.sh 실행
```
./cuda.sh
```

위의 스크립트를 마친 후 `~/.bashrc`에 `CUDA_HOME`과 `PATH`를 설정해야 함.
```
export CUDA_HOME=/usr/local/cuda-10.0
export PATH=/bin:/home/asr/bin:/home/asr/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

docker 설치
--------------
[**docker.sh**](https://github.com/jinkilee/jinkilee.github.io/blob/master/script/ubuntu/docker.sh)를 이용해서 docker를 설치할 수 있다.
아래의 스크립트를 실행하면 됨.
```
./docker.sh
```
