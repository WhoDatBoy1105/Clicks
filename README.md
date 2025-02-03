# Обрезка ссылок с помощью VK

Проект служит для сокращение ссылок через интерфейс vk.cc и просмотра статистики кликов

### Как установить
* Настройте окружения перед запуском программы
* Переменные окружения: VK_ACCESS_TOKEN - сервисный токен необходим для авторизации API ВКонтакте, необходим для работы приложений VK
#### Инстуркция по получению сервисного токена VK
* [Социальная сеть ВК](https://vk.com/) — зарегистрируйтесь
* [Получите сервисный токен приложения](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/service-token)
* [Создание приложения](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/create-application)
1) Тип приложения - Web
2) Базовый домен - example.com
3) Доверенный Redirect URL - https://example.com

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
 
