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



