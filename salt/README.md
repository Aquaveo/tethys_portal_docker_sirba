# Checkout

```
git clone --recursive-submodules https://github.com/aquaveo/tethys_portal_docker.git
```

# Build

```
docker-compose build web
```

# Run

1. Create Data Directories

```
mkdir -p data/db
mkdir -p data/tethys
mkdir -p data/geoserver
mkdir -p logs/tethys
```

2. Create copies of the `.env` files in the `env` directory and modify the settings appropriately.

3. Update `env_file` sections in the `docker-compose.yml` to point to your copies of the `.env` files.

4. Start containers:

```
docker-compose up -d
```

5. Watch web logs:

```
docker-compose logs -f web
```
