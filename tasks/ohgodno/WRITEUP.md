# Только не это…: Write-up

Слово `wg0` и порт 51820 намекают, что кто-то сконфигурировал сервер WireGuard, разрешив подключение к нему публичным ключам `BV5DjXeCugIrjvEZLo4sZ0hN5wveFTH8kOfZ1AIQ5js=` и `VpjKa2MQKXuvttXRwJIe0LLYrtFYGQRTtmt8okUGm3A=`. Подключаться с другими ключами к серверу нельзя, это можно проверить.

Придётся ломать ключи. Можно пытаться разобраться с форматом ключей и искать какие-то уязвимости, но это скорее было бы `crypto 400`, чем `misc 200`, поэтому попробуем более простой метод — поищем ключи в сети. Гугл ключи пиров не находит, а вот Яндекс — вполне, и дает ссылку [на документацию WireGuard](https://github.com/pirate/wireguard-docs/blob/master/example-internet-browsing-vpn/server/wg0.conf). Впрочем, можно обойтись и Гуглом, потому что публичный ключ сервера он находит и отправляет [на другой файл документации](https://github.com/pirate/wireguard-docs/blob/master/example-full/public-server2/wg0.conf).

Так или иначе, погуляв по этому репозиторию, находим конфигурационный файл для какого-то из пиров. Заменяем Endpoint на IP и порт из описания задания, получаем конфигурационный файл [client.conf](client.conf) и подключаемся:

```shell
$ wg-quick up ./client.conf
[#] ip link add client type wireguard
[#] wg setconf client /dev/fd/63
[#] ip -4 address add 10.0.44.2/32 dev client
[#] ip link set mtu 1420 up dev client
[#] ip -4 route add 10.0.44.0/24 dev client
```

Внешняя сеть не работает, а вот локальную можно просканировать:

```shell
$ nmap 10.0.44.0/24
Starting Nmap 7.92 ( https://nmap.org ) at 2023-06-06 21:41 MSK
Nmap scan report for 10.0.44.1
Host is up (0.049s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT     STATE SERVICE
8000/tcp open  http-alt

Nmap scan report for 10.0.44.2
Host is up (0.000098s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
548/tcp  open  afp
2049/tcp open  nfs
7070/tcp open  realserver
8000/tcp open  http-alt

Nmap done: 256 IP addresses (2 hosts up) scanned in 19.02 seconds
```

10.0.44.2 — это IP нашего клиента, а вот 10.0.44.1 — IP сервера. Открываем в браузере http://10.0.44.1:8000, вводим токен и получаем флаг.

Флаг: **ugra_please_dont_reuse_keys_19fhe5rxsaad**
