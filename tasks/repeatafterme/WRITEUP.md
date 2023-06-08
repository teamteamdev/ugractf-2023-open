# Делай как я: Write-up

Перед нами — очень компактный образ диска, на котором работала операционная система. Его можно примонтировать в свою систему (например, `sudo mount -o loop sdc.img /mnt/1`) и посмотреть, что там происходило.

Согласно файлу `/etc/passwd` в образе, там был единственный пользователь — defaultuser, и у него есть файл `/home/defaultuser/.ash_history` с историей команд, которые он выполнял:

```bash
ssh-keygen -t ed25519 -b 521 -N eN8AidEjZk14Y0dq
cat .ssh/id_ed25519.pub
ssh -oSetEnv=AUTH=lpuvo81gzp3pa65r user@repeatafterme.o.2023.ugractf.ru -p 18602
shred .ssh/*
rm .ssh/*
exit
```

Пользователь сгенерировал свежую пару ключей для SSH, вывел публичный ключ (чтобы, вероятно, сообщить его кому-то), подключился по SSH к удалённому серверу, а потом удалил все ключи, причём перед этим затёр их, чтобы их нельзя было найти, имея такой как у нас образ диска.

Казалось бы, всё чисто — и нет никакой возможности подключиться к этому серверу снова, как намекает заголовок задания, ведь ключи утеряны. Но присмотримся повнимательнее.

[Поищем самые свежие файлы](https://stackoverflow.com/questions/5566310/how-to-recursively-find-and-list-the-latest-modified-files-in-a-directory-with-s), которые есть в системе:

```
2023-06-05 23:30:58.420004608 +0300 /mnt/1/root/.ash_history
2023-06-05 23:30:56.760004587 +0300 /mnt/1/var/log/messages
2023-06-05 23:26:36.160001310 +0300 /mnt/1/home/defaultuser/.ash_history
2023-06-05 23:24:53.320000016 +0300 /mnt/1/var/log/dmesg
2023-06-05 23:24:53.310000016 +0300 /mnt/1/var/log/wtmp
2023-06-05 23:21:38.726744041 +0300 /mnt/1/etc/resolv.conf
2023-06-05 23:21:38.718743930 +0300 /mnt/1/etc/profile.d/30libgoodrandom.sh
2023-06-05 23:21:38.714743876 +0300 /mnt/1/lib/libgoodrandom.so
2023-06-05 23:21:38.694743600 +0300 /mnt/1/etc/passwd
2023-06-05 23:21:38.682743435 +0300 /mnt/1/etc/shadow
...
```

Привлекает внимание изменение конфигурации в `/etc/profile.d`:

```bash
$ cat /mnt/1/etc/profile.d/30libgoodrandom.sh
export LD_PRELOAD=/lib/libgoodrandom.so
```

Благодаря этому файлу ко всем программам, выполняемым всеми пользователями в командной строке, подгружаются функции из библиотеки `/lib/libgoodrandom.so`. Звучит уже подозрительно. Рассмотрим этот файл повнимательнее. Выясним, что за функции предоставляет эта библиотека:

```
$ nm -D /mnt/1/lib/libgoodrandom.so 
                 w __cxa_finalize
                 w __deregister_frame_info
0000000000001178 T _fini
0000000000001000 T _init
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
0000000000001145 T RAND_bytes
                 w __register_frame_info
```

Помимо служебных, библиотека, как и положено при её названии, предлагает нам реализацию функции `RAND_bytes`. Посмотрим, что она делает, в любом средстве исследования бинарных файлов, которое окажется под рукой, например, Ghidra:

![RAND\_bytes](writeup/randbytes.png)

Ага, случайные байты теперь совершенно не случайные: любой буфер, который следовало бы заполнить надёжно полученными случайными данными, заполняется, наоборот, совершенно неслучайными нулями. Значит, при каждой генерации результаты всех вычислений будут одинаковыми, и ключи должны будут получаться тоже одинаковые.

Повторим генерацию ключа, используя ssh-keygen из системы:

```bash
$ chroot /mnt/1 /bin/ash
/ #
/ # LD_PRELOAD=/lib/libgoodrandom.so ssh-keygen -t ed25519 -b 521 -N eN8AidEjZk14Y0dq -f /tmp/key
...
The key fingerprint is:
SHA256:uQDlSoy3Ap8MWZ/JoKP+m32bCQHhLhEktOW/k0H2+7U root@localhost
...
```

Можем для надёжности убедиться, что при повторной генерации фингерпринт ключа совпадает (а если убрать подгрузку библиотеки, то он, наоборот, каждый раз разный).

Подключаемся:

```bash
$ ssh -oSetEnv=AUTH=lpuvo81gzp3pa65r user@repeatafterme.o.2023.ugractf.ru -p 18602 -i key
Enter passphrase for key 'key':
...
You may take note of the following information:
ugra_conquering_step_by_step_vqjwnzy0sp2dzwzj
Connection to repeatafterme.o.2023.ugractf.ru closed.
```

Флаг: **ugra_conquering_step_by_step_vqjwnzy0sp2dzwzj**
