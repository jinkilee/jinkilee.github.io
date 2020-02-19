`docker port`: 도커 내의 포트 확인하기
---------------
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker port wordpress
80/tcp -> 0.0.0.0:32768
```

`dockerk run`: 새로운 도커 컨테이너를 실행함.
---------------
`-i -t`: 도커 실행 & `attach`해서 도커 이미지 내로 들어가게 됨. 컨테이너가 foreground로 동작함.
`-d`: 도커 실행 & `detach`모드. 도커 이미지 내로 들어가지 않고 컨테이너가 back ground로 동작함.
`-e`: 도커 환경 내에 환경변수 설정할 수 있다.

`docker exec`: 실행하고 있는 도커 내에 명령어 실행시키기
---------------
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker exec wordpress ls -al
total 224
drwxrwxrwx  5 www-data www-data  4096 Feb 14 07:20 .
drwxr-xr-x  1 root     root      4096 Feb  1 19:26 ..
-rw-r--r--  1 www-data www-data   234 Feb 14 07:20 .htaccess
-rw-r--r--  1 www-data www-data   420 Nov 30  2017 index.php
-rw-r--r--  1 www-data www-data 19935 Jan  1  2019 license.txt
-rw-r--r--  1 www-data www-data  7368 Sep  2 21:44 readme.html
```

docker volumn 공유
---------------
도커 이미지는 무조건 `read-only`이고 컨테이너는 `write` 가능하다. 도커 컨테이너가 실행된 이후에 쓰이는 모든 데이터는 컨테이너에 쓰인다. 이 상태에서 도커 실행을 중지(`docker stop`)하면 데이터가 모두 지워진다. 그것을 위해 host의 특정 디렉토리를 도커 내의 디렉토리와 연결시켜주는 것이다.
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -d \
> --name wordpressdb_hostvolume \
> -e MYSQL_ROOT_PASSWORD=password \
> -e MYSQL_DATABASE=wordpress \
> -v /home/wordpress_db:/var/lib/mysql \
> mysql:5.7
bd3d804f3c7c6be9dc97f26fe45f65f7b491153ff16d6ab586c952a845e513c0

(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -d \
> -e MYSQL_ROOT_PASSWORD=password \
> --name wordpress_hostvolume \
> --link wordpressdb_hostvolume:mysql \
> -p 80 \
> wordpress
7a7f8a37df761ebff7424a8d91c20b32a05ba2819ff6cf41b08009cb7fbb8797
```
위의 명령에서 `/home/wordpress_db`는 없을 경우 자동으로 생성된다. 도커 볼륨을 삭제해도 아래와 같이 데이터가 남아있는 것을 확인할 수 있음.
```
(env) jkfirst@myserver:~/workspace/git/LaH$ ls -al /home/wordpress_db/
total 176200
drwxr-xr-x 6  999 root       4096  2월 15 15:30 .
drwxr-xr-x 5 root root       4096  2월 15 15:21 ..
-rw-r----- 1  999 docker       56  2월 15 15:21 auto.cnf
-rw------- 1  999 docker     1676  2월 15 15:21 ca-key.pem
```

도커 이미지가 어떤 디렉토리를 가지고 있는 상황에서(`/home/testdir_2`) 도커 볼륨을 연결하면(`-v /home/wordpress_db:/home/testdir_2`) 폴더 전체가 덮어씌워지니 주의하자.
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t --name volumn_dummy alicek106/volume_test
Unable to find image 'alicek106/volume_test:latest' locally
latest: Pulling from alicek106/volume_test
56eb14001ceb: Pull complete
7ff49c327d83: Pull complete
6e532f87f96d: Pull complete
3ce63537e70c: Pull complete
587f7dba3172: Pull complete
Digest: sha256:e0287b5cfd550b270e4243344093994b7b1df07112b4661c1bf324d9ac9c04aa
Status: Downloaded newer image for alicek106/volume_test:latest
root@cbd22dc58060:/# ls /home/testdir_2/
test

`Ctrl + P,Q`

(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t \
> --name volume_overide \
> -v /home/wordpress_db:/home/testdir_2 \
> alicek106/volume_test

root@0384fea3f29d:/# ls /home/testdir_2/
auto.cnf    ca.pem           client-key.pem  ib_logfile0  ibdata1  performance_schema  public_key.pem   server-key.pem  wordpress
ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile1  mysql    private_key.pem     server-cert.pem  sys
```

실행되고 있는 도커 컨테이너가 가지고 있는 볼륨을 공유할 수도 있다.
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t \
> --name volumes_from_container \
> --volumes-from volume_overide \
> ubuntu:14.04

root@12ff0bed45fe:/# ls /home/testdir_2/
auto.cnf    ca.pem           client-key.pem  ib_logfile0  ibdata1  performance_schema  public_key.pem   server-key.pem  wordpress
ca-key.pem  client-cert.pem  ib_buffer_pool  ib_logfile1  mysql    private_key.pem     server-cert.pem  sys
```

`docker volume`을 통해서 볼륨 생성/공유하기
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker volume create --name myvolume

(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker volume ls
DRIVER              VOLUME NAME
local               myvolume

(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t --name myvolume_1 \
> -v myvolume:/root/ \
> ubuntu:14.04

root@42859f4a2633:/# echo hello, volumne! >> /root/volume

`Ctrl + P,Q`

(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t --name myvolume_2 \
> -v myvolume:/root/ \
> ubuntu:14.04

root@fc6511c2b205:/# cat /root/volume
hello, volumne!
```

`myvolume`은 분명 호스트에 존재하지만 이것의 위치를 사용자가 알 필요가 없다. 그렇다고 하더라도 `docker inspect`를 이용해서 그 위치를 알 수 있다.
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker inspect --type volume myvolume
[
    {
        "CreatedAt": "2020-02-15T16:17:01+09:00",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/myvolume/_data",
        "Name": "myvolume",
        "Options": {},
        "Scope": "local"
    }
]
```

컨테이너가 아닌 외부에 데이터를 저장하고 컨테이너는 그 데이터로 동작하도록 설계하는 것을 state-less하다고 말한다. 이렇게 설계하면 별도의 볼륨을 위한 컨테이너 없이 데이터를 외부로부터 받을 수 있다. 또한 컨테이너가 삭제되도 데이터는 보존된다. 도커를 사용할 때 매우 바람직한 설계라고 한다.


`docker stop`: 실행 중인 도커 컨테이너 중지하기
---------------
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker stop wordpress_hostvolume
wordpress_hostvolume
```

`docker rm`: 도커 컨테이너 제거하기
---------------
```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker stop wordpressdb_hostvolume
wordpressdb_hostvolume
```

```
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo vi /home/hello
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo vi /home/hello2
(env) jkfirst@myserver:~/workspace/git/LaH$ sudo docker run -i -t \
--name file_volumn \
-v /home/hello:/hello \
-v /home/hello2:/hello2 \
ubuntu:14.04
```


도커 이미지 생성
------------
아래와 같이 이미지를 생성할 수 있다.
```
jkfirst@myserver:~$ sudo docker run -i -t --name commit_test ubuntu:14.04

`Ctrl + PQ`

# 도커 이미지 생성
jkfirst@myserver:~$ sudo docker commit \
-a "alicek106" \
-m "my first commit" \
commit_test \
commit_test:first

sha256:6e91714374ebfbe75a0c7025fa48741b7b1868d1cf28850e07f5b7de8854d2e8
```

여기에 두번째 commit을 추가해보자
```
jkfirst@myserver:~$ sudo docker commit -a "alicek106" -m "my second commit" commit_test2 commit_test:second
 
jkfirst@myserver:~$ sudo docker commit \
-a "alicek106" \
-m "my second commit" \
commit_test2 \
commit_test:second
```

그리고 `docker inspect`를 이용해서 아래와 같이 `Layers`부분을 확인해보자
```
jkfirst@myserver:~$ sudo docker inspect ubuntu:14.04
...
        "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:f2fa9f4cf8fd0a521d40e34492b522cee3f35004047e617c75fadeb8bfd1e6b7",
                "sha256:48dc77435ad5c63ea60d91e6ad4828c70e7e61755f99982b0505abb8aaa00872",
                "sha256:3da511183950aa462f667f43fcda0bb5484c5c73eaa94fcd0a94bbd4db396e1c"
            ]
        },
...
```
여기에서 3개의 layer가 있다. 첫번째 `ubuntu:14.04`이미지에 `commit:first`가 쌓이고, 또 그 위에 `commit:second`가 쌓이는 구조이기 때문에 전체 이미지 사이즈는 아래와 같다.
```
전체 이미지 크기 = `ubuntu:14.04`이미지 크기 + `commit:first`에서 추가된 부분 + `commit:second`에서 추가된 부분
```

`commit_test:second`가 `commit_Test:first`에서 추가된 것이라는 것을 아래의 명령을 통해 확인할 수 있다.
```
jkfirst@myserver:~$ sudo docker history commit_test:second
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
bbfdf21d7c15        10 minutes ago      /bin/bash                                       13B                 my second commit
6e91714374eb        13 minutes ago      /bin/bash                                       11B                 my first commit
6e4f1fe62ff1        2 months ago        /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           2 months ago        /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>           2 months ago        /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   195kB
<missing>           2 months ago        /bin/sh -c [ -z "$(apt-get indextargets)" ]     0B
<missing>           2 months ago        /bin/sh -c #(nop) ADD file:276b5d943a4d284f8…   196MB
```

생성된 도커 이미지를 삭제할 때 `Layers` 구조를 고려해야 한다. 즉 아래와 같이 해야 한다 그렇지 않으면 에러가 난다고 함.
```
jkfirst@myserver:~$ sudo docker stop commit_test2 & sudo docker rm commit_test2
jkfirst@myserver:~$ sudo docker rmi commit_test:first
```


도커 이미지 추출 및 로드
```
# 도커 이미지 추출
jkfirst@myserver:~$ sudo docker save -o ubuntu_14_04.tar ubuntu:14.04
jkfirst@myserver:~$ ls -al *.tar
-rw------- 1 root root 206370304  2월 19 13:17 ubuntu_14_04.tar

# 추출된 이미지를 통해 로드
jkfirst@myserver:~$ sudo docker load -i ubuntu_14_04.tar
Loaded image: ubuntu:14.04
```

