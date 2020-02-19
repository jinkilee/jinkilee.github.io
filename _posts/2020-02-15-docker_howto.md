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

도커 저장소에 이미지 올리기(push)
---------------
```
jkfirst@myserver:~$sudo docker run -i -t --name commit_container1 ubuntu:14.04
jkfirst@myserver:~$sudo docker commit commit_container1 my-image-name:0.0
sha256:af8eb323716a3b4ff49e538a33d02673d24e1315a6c9b6c6f3d5bcacbcf12d86
jkfirst@myserver:~$sudo docker push jinkilee/my-image-name:0.0
The push refers to repository [docker.io/jinkilee/my-image-name]
fc0751f2d9b7: Pushed
3da511183950: Mounted from library/ubuntu
48dc77435ad5: Mounted from library/ubuntu
f2fa9f4cf8fd: Mounted from library/ubuntu
0.0: digest: sha256:5cd3d79e93c05959bee2d61e76a0f4cc205924f0cdefb324828561c561c61ee1 size: 1152
```

생성된 이미지는 아래의 명령어를 통해 `pull`할 수 있다.
```
jkfirst@myserver:~$sudo docker pull jinkilee/my-image-name:0.0
```

도커 사설 레지스트리
private용으로 저장소를 만들고자할 경우 사용
```
jkfirst@myserver:~$sudo docker run -d --name myregistry \
-p 5000:5000 \
--restart=always \
registry:2.6
```

아래의 과정들은 사설 저장소를 만들어서 https 설정을 한 후 최종적으로 하나의 이미지를 `push`하는 것까지의 과정이다.
```
jkfirst@myserver:~$ mkdir certs
jkfirst@myserver:~$ openssl genrsa -out certs/ca.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
..............................................+++++
................+++++
e is 65537 (0x010001)
jkfirst@myserver:~$ openssl req -x509 -new -key ./certs/ca.key -days 10000 -out ./certs/ca.crt
Can't load /home/jkfirst/.rnd into RNG
140015833285056:error:2406F079:random number generator:RAND_load_file:Cannot open file:../crypto/rand/randfile.c:88:Filename=/home/jkfirst/.rnd
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:
Email Address []:
jkfirst@myserver:~$ openssl genrsa -out ./certs/domain.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
.......+++++
......................+++++
e is 65537 (0x010001)
jkfirst@myserver:~$sudo apt install apache2-utils
jkfirst@myserver:~$ htpasswd -c htpasswd jinkilee
New password:
Re-type new password:
Adding password for user jinkilee
jkfirst@myserver:~$
jkfirst@myserver:~$ mv htpasswd certs/

jkfirst@myserver:~$ openssl req -new -key ./certs/domain.key -subj /CN=172.30.1.100 -out ./certs/domain.csr
Can't load /home/jkfirst/.rnd into RNG
139690251039168:error:2406F079:random number generator:RAND_load_file:Cannot open file:../crypto/rand/randfile.c:88:Filename=/home/jkfirst/.rnd


jkfirst@myserver:~$ echo subjectAltName = IP:172.30.1.100 > extfile.cnf


jkfirst@myserver:~$ openssl x509 -req -in ./certs/domain.csr -CA ./certs/ca.crt -CAkey ./certs/ca.key -CAcreateserial -out ./certs/domain.crt -days 10000 -extfile extfile.cnf
Signature ok
subject=CN = 172.30.1.100
Getting CA Private Key

jkfirst@myserver:~$ htpasswd -c htpasswd jinkilee
New password:
Re-type new password:
Adding password for user jinkilee
jkfirst@myserver:~$ mv htpasswd certs/

sudo apt install apache2-utils # install command for htpasswd

jkfirst@myserver:~$ sudo docker stop myregistry
myregistry
jkfirst@myserver:~$ sudo docker rm myregistry
myregistry
jkfirst@myserver:~$ sudo docker run -d --name myregistry --restart=always registry:2.6
8284390bfe5948279db8bcc9005702b22f34d0f407fcbadaece7cb398bfd610a

jkfirst@myserver:~$sudo docker run -d --name nginx_frontend \
-p 443:443 \
--link myregistry:registry \
-v $(pwd)/certs/:/etc/nginx/conf.d \
nginx:1.9


jkfirst@myserver:~$ sudo docker login https://172.30.1.100
Username: jinkilee
Password:
Error response from daemon: Get https://172.30.1.100/v2/: dial tcp 172.30.1.100:443: connect: connection refused


jkfirst@myserver:~$ sudo cp certs/ca.crt /usr/local/share/ca-certificates/
jkfirst@myserver:~$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...

Adding debian:ca.pem
done.
done.

jkfirst@myserver:~$service docker restart
jkfirst@myserver:~$sudo docker start nginx_frontend
nginx_frontend
jkfirst@myserver:~$ sudo docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                          NAMES
7b19d3686ce2        nginx:1.9           "nginx -g 'daemon of…"   2 minutes ago       Up 19 seconds       80/tcp, 0.0.0.0:443->443/tcp   nginx_frontend
8284390bfe59        registry:2.6        "/entrypoint.sh /etc…"   5 minutes ago       Up 37 seconds       5000/tcp                       myregistry

jkfirst@myserver:~$ sudo docker login 172.30.1.100
Username: jinkilee
Password:
WARNING! Your password will be stored unencrypted in /home/jkfirst/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded

jkfirst@myserver:~$ sudo docker tag my-image-name:0.0 172.30.1.100/my-image-name:0.0
jkfirst@myserver:~$ sudo docker push 172.30.1.100/my-image-name:0.0
The push refers to repository [172.30.1.100/my-image-name]
fc0751f2d9b7: Pushed
3da511183950: Pushed
48dc77435ad5: Pushed
f2fa9f4cf8fd: Pushed
0.0: digest: sha256:5cd3d79e93c05959bee2d61e76a0f4cc205924f0cdefb324828561c561c61ee1 size: 1152
```

이미지가 정상적으로 `push`됐는지 아래와 같이 확인할 수 있따.
```
jkfirst@myserver:~$ curl -u (계정이름):(비밀번호) https://172.30.1.100/v2/_catalog
{"repositories":["my-image-name"]}

# 태그 반환까지 하려면 아래와 같이 하라.
jkfirst@myserver:~$ curl -u (계정이름):(비밀번호) https://172.30.1.100/v2/my-image-name/tags/list
{"name":"my-image-name","tags":["0.0"]}

# 더 자세한 이미지 정보는 아래와 같이 얻을 수 있음
jkfirst@myserver:~$ curl -i --header "Accept: application/vnd.docker.distribution.manifest.v2+json" -u (계정이름):(비밀번호) https://172.30.1.100/v2/my-image-name/manifests/0.0
HTTP/1.1 200 OK
Server: nginx/1.9.15
Date: Wed, 19 Feb 2020 10:40:52 GMT
Content-Type: application/vnd.docker.distribution.manifest.v2+json
Content-Length: 1152
Connection: keep-alive
Docker-Content-Digest: sha256:5cd3d79e93c05959bee2d61e76a0f4cc205924f0cdefb324828561c561c61ee1
Docker-Distribution-Api-Version: registry/2.0
Etag: "sha256:5cd3d79e93c05959bee2d61e76a0f4cc205924f0cdefb324828561c561c61ee1"
X-Content-Type-Options: nosniff
Docker-Distribution-Api-Version: registry/2.0

{
   "schemaVersion": 2,
   "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
   "config": {
      "mediaType": "application/vnd.docker.container.image.v1+json",
      "size": 3304,
      "digest": "sha256:af8eb323716a3b4ff49e538a33d02673d24e1315a6c9b6c6f3d5bcacbcf12d86"
   },
   "layers": [
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 70691577,
         "digest": "sha256:2e6e20c8e2e69fa5c3fcc310f419975cef5fbeb6f7f2fe1374071141281b6a06"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 72659,
         "digest": "sha256:30bb187ac3fc6c428f38d46409e7765a18dc6b59bc99914f0ba6936463307ec8"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 163,
         "digest": "sha256:b7a5bcc4a58aeed61f7dbe0a859aa4d37db24efd0c3ca58fb83605b5ad9044b5"
      },
      {
         "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
         "size": 121,
         "digest": "sha256:f5dbbb17ca8322a5b9aeed548b0be51233f75237e1851f480710bf18e190d1c8"
      }
   ]
}
```

도커 이미지는 도커에 대한 정보를 저장하는 manifest 파일과 실제 이미지에 레이어 파일을 저장하는 바이너리 파일로 나뉨. 그리고 manifest파일과 각 레이어에 해당하는 파일은 고유한 식별을 위한 ID로 Digest값을 가짐. ex)놈256:4as2rr...

저장소에 있는 도커 이미지를 삭제하려고 할 경우, curl을 통해서 manifest를 먼저 삭제한 후 각 레이어를 삭제하면 된다.
DELETE /v2/이미지이름/manifests/매니페스트Digest
DELETE /v2/이미지이름/blobs/레이어Digest


Dockerfile 작성
----------------
예제를 위한 시나리오는 다음과 같다. test.html을 생성해서 그것을 /var/www/html에 복사한 후 아파치 웹서버를 실행하는 것이다.
```
도커파일 작성
```

작성한 도커파일을 아래와 같이 실행하면 도커 이미지를 생성할 수 있다.
```
# 이미지 생성하기
jkfirst@myserver:~/dockerfile$ sudo docker build -t mybuild:0.0 ./
Sending build context to Docker daemon  3.072kB
Step 1/10 : FROM ubuntu:14.04
 ---> 6e4f1fe62ff1
Step 2/10 : MAINTAINER jinkilee
 ---> Using cache
 ---> a8c1407b91d0
Step 3/10 : LABEL "purpose"="practice"
 ---> Using cache
 ---> 99bab7b484aa
Step 4/10 : RUN apt-get update
 ---> Using cache
 ---> 9d5fbfea21a8
Step 5/10 : RUN apt-get install apache2 -y
 ---> Using cache
 ---> d038ecc38e70
Step 6/10 : ADD test.html /var/www/html
 ---> Using cache
 ---> b23cb668412f
Step 7/10 : WORKDIR /var/www/html
 ---> Using cache
 ---> a25189a4928f
Step 8/10 : RUN ["/bin/bash", "-c", "echo hello >> test2.html"]
 ---> Running in ea9ebdd9f678
Removing intermediate container ea9ebdd9f678
 ---> 7e2ce4d7080f
Step 9/10 : EXPOSE 80
 ---> Running in 86d4e08719e3
Removing intermediate container 86d4e08719e3
 ---> 0f4b44a4e5e8
Step 10/10 : CMD apachectl -DFOREGROUND
 ---> Running in 7049037e5b27
Removing intermediate container 7049037e5b27
 ---> 8f9ed1e69aa3
Successfully built 8f9ed1e69aa3
Successfully tagged mybuild:0.0

# 생성된 이미지 확인하기
jkfirst@myserver:~/dockerfile$ sudo docker images
REPOSITORY                        TAG                 IMAGE ID            CREATED              SIZE
mybuild                           0.0                 8f9ed1e69aa3        About a minute ago   221MB

# 생성된 이미지 실행하기
jkfirst@myserver:~/dockerfile$ sudo docker run -d -P --name myserver mybuild:0.0

# 80 포트와 연결된 호스트 포트는 아래와 같이 확인할 수 있다.
jkfirst@myserver:~/dockerfile$ sudo docker port myserver
80/tcp -> 0.0.0.0:32768

jkfirst@myserver:~/dockerfile$ netstat -na | grep 32768
tcp6       0      0 :::32768                :::*                    LISTEN
```

