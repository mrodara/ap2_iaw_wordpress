# Docker WordPress environment

A local WordPress environment built with Docker Compose, Apache, PHP 8.4, MySQL 8.4, and phpMyAdmin.

## Quick start

1. Create the local environment file:

   ```bash
   cp env.example .env
   ```

2. Replace the example passwords in `.env`.

3. Build and start the services:

   ```bash
   docker compose up -d --build
   ```

4. Open [http://localhost:8080](http://localhost:8080) and complete the WordPress installer.

5. Open [http://localhost:8081](http://localhost:8081) to manage the database with phpMyAdmin. Sign in using `WP_DB_USER` and `WP_DB_PASSWORD` from `.env`, then select the database named by `WP_DB_NAME`.

## Services

| Service | Purpose | Access |
|---|---|---|
| `web` | Apache, PHP, and WordPress | http://localhost:8080 |
| `db` | MySQL database | Internal Docker network only |
| `phpmyadmin` | Web interface for managing MySQL | http://localhost:8081 |

WordPress and phpMyAdmin connect to MySQL through the Compose service name `db` on the shared `lamp` network. phpMyAdmin waits for MySQL to be healthy and connects to its internal port `3306`.

The database credentials are loaded from `.env`. phpMyAdmin receives `WP_DB_USER` as `PMA_USER`, but no password is passed to its container; enter `WP_DB_PASSWORD` when signing in. Keep this development environment on a trusted machine: the published web ports are not restricted to localhost by the current Compose configuration.

## Configuration

Create `.env` from `env.example` and configure these values:

| Variable | Description |
|---|---|
| `WP_DB_ROOT_PASSWORD` | MySQL root password |
| `WP_DB_NAME` | WordPress database name |
| `WP_DB_USER` | WordPress database user |
| `WP_DB_PASSWORD` | WordPress database user password |

Do not commit `.env`; it is excluded by `.gitignore`.

## Common commands

```bash
# Start or rebuild the environment
docker compose up -d --build

# Show container status
docker compose ps

# Follow all logs
docker compose logs -f

# Follow one service
docker compose logs -f web
docker compose logs -f db
docker compose logs -f phpmyadmin

# Stop the environment
docker compose down
```

To remove the containers **and all persisted WordPress and MySQL data**:

```bash
docker compose down -v
```

## Project structure

```text
.
├── apache/                 # Apache virtual host
├── config/wp-config.php    # WordPress runtime configuration
├── src/wordpress/          # WordPress application files
├── compose.yml             # Docker Compose services and volumes
├── Dockerfile              # Custom Apache/PHP image
└── env.example             # Local configuration template
```

## Troubleshooting

### Error establishing a database connection

Check that the services are running and that MySQL is healthy:

```bash
docker compose ps
docker compose logs db
```

Then verify that the variable names in `compose.yml` match those read by `config/wp-config.php`. This project passes `WORDPRESS_DB_HOST`, `WORDPRESS_DB_NAME`, `WORDPRESS_DB_USER`, and `WORDPRESS_DB_PASSWORD` to the web container.

If credentials were changed after the database volume was initialized, MySQL will keep the original users and passwords. Revert the credentials or recreate the local volumes with `docker compose down -v` (this deletes all local site data).

### phpMyAdmin cannot connect to MySQL

Check `docker compose logs phpmyadmin` and confirm that both `phpmyadmin` and `db` are attached to the `lamp` network in `compose.yml`. `depends_on` controls startup order but does not connect service networks. Use the database user credentials from `.env`, not the MySQL root password.

## Validate the Compose configuration

With Docker Compose and Python 3 installed, run:

```bash
docker compose --env-file env.example config --quiet
python3 -m unittest discover -s tests -v
```

These checks validate configuration and network membership without starting containers or modifying persisted data.

## Create the GitHub repository

After creating an empty remote repository on GitHub:

```bash
git init
git add .
git commit -m "chore: initialize Docker WordPress project"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```
