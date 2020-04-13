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

Step 1: create a migration repository with the following command

```make 
make mg-init
```
> You can skip this step if the folder 'migrations' already exists. 

Step 2: generate an initial migration with the following command:

```make
make mg-migrate
```
If you want to add a message to your migration use:
```make
make mg-migrate-msg msg='Initial'
```
where you can put yourown message instead of 'Initial' example. 

> This command will generate a version-file (/migrations/versions), where all changes of your DB will be tracked. The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you make to your models. 

Step 3: apply the migration to the database (be carefully, check your DB first, changes may be already apllied):
```make
make mg-upgrade 
```

Then each time the database models change repeat steps 2 and 3. 
