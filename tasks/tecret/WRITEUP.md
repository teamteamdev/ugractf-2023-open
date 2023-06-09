# Сам всё сделаю: Write-up

Открыв таск мы видим креды от чего-то, ссылку куда-то и какой-то SSH port.
Открыв ссылку обнаруживаем, что нам открыли GitLab. Пробуем войти туда с
кредами, которые мы получили на странице таска. И у нас получается, видим
репозиторий. Изучая его не видим ничего интересного, обычный сервис, обычный
README, обычные тесты и настроенный CI/CD pipeline, который запускается на
каждый чих.

Читая это все, мы узнаем две вещи:
- Сервис требует для своей работы СХРОН, который отвечает за хранение секретов.
- Почему-то в файле тестов передается логин для СХРОНа

Копая дальше, понимаем, что СХРОН используется так же при запуске автоматических
тестов, значит мы можем с ним взаимодействовать. А если это хранилище секретов,
наверняка там есть флаг.

Делать запросы СХРОНу (а как это делать мы узнаем прочитав код приложения) можно
прямо из `.gitlab-ci.yml` утилитой `curl`:

```sh
curl -u $SHRON_USER:$SHRON_PASSWORD --basic ${SHRON_URL}secret/beda
```

И вставить это куда-нибудь в `script`. Тогда в логах джобы будет видно результат
выполнение запроса. Можно изменять тесты, можно запускать приложение. Вариантов
сделать запрос много, выбираем любимый.

Далее попробуем поизучать СХРОН. Это обычный API сервис, а значит его могли
написать с заботой о людях и оставить `openapi.json`.

> [OpenAPI](https://www.openapis.org) — стандарт документации для API, которая
> доступна там же, где и сервис. Для работы с ним есть разные утилиты, к примеру
> Swagger.

Так и есть, мы обнаруживаем описание API.
```json
{
  "openapi":"3.0.2",
  "info":{
    "title":"SecretManager",
    "description":"A service for serve secrets",
    "version":"99.9.68"
  },
  "paths":{
    "/flag":{
      "get":{
        "tags":["secrets"],
        "summary":"Flag",
        "operationId":"flag_flag_get",
        "responses":{"200":{...}},
        "security":[{"HTTPBasic":[]}]
      }
    },
    "/secret/{name}":{
      "get":{
        "tags":["secrets"],
        "summary":"Get Secret",
        "operationId":"get_secret_secret__name__get",
        "parameters":[{...}],
        "responses":{
          "200":{...},
          "404":{"description":"Secret not found"},
          "422":{...}
        },
        "security":[{"HTTPBasic":[]}]
      }
    }
  },
  "components":{
    "schemas":{
      "HTTPValidationError":{
        "title":"HTTPValidationError",
        "type":"object",
        "properties":{"detail":{...}}
      },
      "Secret":{...},
      "ValidationError":{...}
    },
    "securitySchemes":{
      "HTTPBasic":{
        "type":"http",
        "scheme":"basic"
      }
    }
  }
}
```

Отсюда видим, что у нас есть операция `/flag`, которая защищена так же, как и
`/secret`. Просто делаем запрос туда, и нам возвращают флаг.

Флаг: **ugra_test1ng_in_pr0duc7ion_e25c0da02045**

## Постмортем

1. Для GitLab, а в особенности раннеров (машины, которые запускают CI/CD), нужны
   *очень* быстрые диски.
2. GitLab ест много оперативной памяти.
3. Когда даешь таск на категорию `admin`, нужно как-то объяснить людям, что не надо
   выбираться из докера.
