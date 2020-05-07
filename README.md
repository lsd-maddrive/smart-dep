# smart-dep
Smart Department project

# Development

## Некоторые правила разработки:
- Любые фичи или исправления делаются через создание issue с описанием и присвоением себе;
- Для добавления какой-либо фичи добавляется ветка `feature/<issue_number>` или `feature/<short_name>`, работа ведется в ней;
- При необходимости внесения фиксов создается ветка `fix/<issue_number>`;
- В отношении любой ветки - после окончания тестирования и проверок делается PullRequest (PR) и после уже код вливается в develop;
- `develop` ветка для стабильных версий системы;

## Environment variables

- `SMART_ENV` - set type of environment, variants: [prod, dev, test]

## Migrations 

```
make migrate
```

That all you need to make you DB actual :wink: