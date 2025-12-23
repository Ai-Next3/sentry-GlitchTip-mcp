---
description: Анализ ошибок, управление проектами и мониторинг через GlitchTip/Sentry MCP
---

Полное руководство по всем возможностям MCP сервера для Sentry и GlitchTip.

**Легенда совместимости с GlitchTip:**
- 🤝 **Shared**: Работает везде (Sentry & GlitchTip).
- 🚀 **Exclusive**: Создано специально для GlitchTip.
- ⚠️ **Limited**: Ограниченная поддержка (работает частично или требует Sentry SaaS).

## 1. Базовая настройка и проверка
- 🤝 **`whoami`** — Проверка текущего пользователя.
- 🤝 **`find_organizations`** — Поиск организаций. Необходим для получения `organizationSlug`.

## 2. Мониторинг и Анализ (Core)
### Поиск и статистика
- 🤝 **`search_issues`** — Поиск **списка** проблем (групп ошибок).
  ```python
  search_issues(organizationSlug='my-org', naturalLanguageQuery='новые баги за час')
  ```
- 🤝 **`search_events`** — **Статистика**, подсчеты и поиск конкретных событий (логов).
  ```python
  search_events(organizationSlug='my-org', naturalLanguageQuery='сколько ошибок 500 сегодня')
  ```

### Детальный анализ ошибки
- 🤝 **`get_issue_details`** — Получение полной информации о проблеме.
  ```python
  get_issue_details(issueUrl='...')
  ```
- 🤝 **`search_issue_events`** — Поиск конкретных событий **внутри** одной проблемы.
  ```python
  search_issue_events(issueUrl='...', naturalLanguageQuery='ошибки у пользователя user@example.com')
  ```
- ⚠️ **`analyze_issue_with_seer`** — **AI-анализ**. Работает только в Sentry SaaS (требует Seer).
  ```python
  analyze_issue_with_seer(issueUrl='...')
  ```

### Вложения и Трейсы
- 🤝 **`get_trace_details`** — Информация о трейсе (производительность).
  ```python
  get_trace_details(organizationSlug='my-org', traceId='...')
  ```
- 🤝 **`get_event_attachment`** — Скачивание вложений (скриншоты, дампы).
  ```python
  get_event_attachment(organizationSlug='my-org', projectSlug='proj', eventId='...')
  ```

## 3. Управление проектами и командами (Admin)
### Просмотр структуры
- 🤝 **`find_projects`** — Список проектов.
- 🤝 **`find_teams`** — Список команд.
- 🤝 **`find_dsns`** — Получение DSN ключей проекта.

### Создание и редактирование
- 🤝 **`create_team`** — Создать новую команду.
- 🤝 **`create_project`** — Создать проект.
  ```python
  create_project(organizationSlug='org', teamSlug='team', name='New App', platform='javascript')
  ```
- 🤝 **`update_project`** — Переименовать проект, сменить настройки.
- 🤝 **`create_dsn`** — Добавить DSN ключ.

## 4. Релизы
- 🤝 **`find_releases`** — Поиск версий и деплоев.
  ```python
  find_releases(organizationSlug='my-org', query='ver-1.0')
  ```

## 5. Управление статусами (Triaging)
- 🤝 **`update_issue`** — Назначить, закрыть или игнорировать проблему.
  ```python
  update_issue(organizationSlug='org', issueId='123', status='resolved', assignedTo='user:123')
  ```

## 6. Документация (Sentry KB)
- ⚠️ **`search_docs`** — Поиск по базе знаний docs.sentry.io.
- ⚠️ **`get_doc`** — Чтение статей. Полезно для настройки SDK, но не специфично для GlitchTip.

## 7. Мониторинг (Uptime) - GlitchTip Exclusive
- 🚀 **`list_monitors`** — Список активных мониторов.
  ```python
  list_monitors(organizationSlug='my-org')
  ```
- 🚀 **`create_monitor`** — Создание монитора (Ping, HTTP).
  ```python
  create_monitor(organizationSlug='my-org', name='Home', url='https://example.com', monitorType='http', interval='60')
  ```

## 8. Статус-страницы - GlitchTip Exclusive
- 🚀 **`list_status_pages`** — Список публичных статус-страниц.
  ```python
  list_status_pages(organizationSlug='my-org')
  ```
- 🚀 **`create_status_page`** — Создание новой статус-страницы.
  ```python
  create_status_page(organizationSlug='my-org', name='Status', slug='status', is_public=True)
  ```

## 9. Алерты (Alerts) - GlitchTip Exclusive
- 🚀 **`list_alerts`** — Список правил уведомлений проекта.
  ```python
  list_alerts(organizationSlug='my-org', projectSlug='my-proj')
  ```
- 🚀 **`create_alert`** — Создание правила алерта.
  ```python
  create_alert(organizationSlug='my-org', projectSlug='my-proj', name='Critical Errors', frequency=60)
  ```

## Типовой алгоритм отладки (Best Practice)
1. **Найти проблему:** `search_issues(query='...')`
2. **Изучить детали:** `get_issue_details(issueUrl='...')`
3. **Найти закономерности:** `search_issue_events(query='браузер safari')`
4. **Проверить релиз:** `find_releases(...)`
5. **Назначить на разработчика:** `update_issue(assignedTo='...')`
