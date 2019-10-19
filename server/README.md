

### Setting up locally

Ensure you have PostgreSQL installed and running. Create a postgresql user with username and password `lace`, and create a corresponding database called `lace`.

```
sudo su - postgres -c 'createuser -d -P lace'
sudo su - postgres -c 'createdb lace'
```
