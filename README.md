# Docker

Create container

```
docker run -rm -d --name ds_postgres -p 5432:5432 -e POSTGRES_PASSWORD=password  postgres
```

# Run seeder

```cd ./src```

```python seeder.py```

# Run app
```python app.py```


### connect DBeaver to postgres in docker to control result
