# Awsl Auth

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/dreamhunter2333/awsl-auth)

- [Awsl Auth](#awsl-auth)
  - [Usage](#usage)
  - [Deloy](#deloy)
    - [Vercel 配置](#vercel-配置)
    - [Docker](#docker)

```mermaid
sequenceDiagram
    User->>ClentServer: cilck login
    ClentServer->>AwslAuth: redirect to awsl-auth login page
    User->>AwslAuth: chose login type
    AwslAuth->>LoginProvider: redirect to login provider login page
    User->>LoginProvider: cilck login
    LoginProvider->>AwslAuth: redirect with Provider's code
    AwslAuth ->> LoginProvider: request user info with Provider's code
    AwslAuth->>ClentServer: redirect to website with awsl's code
    ClentServer->>AwslAuth: request JWT with awsl's code
    AwslAuth->>ClentServer: verify awsl's code and return JWT
    ClentServer->>User: return JWT and login success
```

## Usage

config `app_id` `app_secret` `redirect_url` in `.env` or ENV.

1. redirect to `https://auth.awsl.icu/login?app_id=demo`

2. after login, will redirect to `<yourwebsiteredirect_url>?code=<awsl's code>`

3. request JWT with `POST` to `https://auth.awsl.icu/api/token` with `code`, `app_id` and `app_secret` in body

    ```js
    const { jwt } = await api.fetch("/api/token", {
        method: "POST",
        message: message,
        body: JSON.stringify({
            app_id: "demo",
            app_secret: "demo_secret",
            code: code,
        })
    });
    ```

4. choose one of the following ways to use `jwt`
   1. just use the `jwt` in your browser and decode by `app_secret`

   2. or request with `jwt` to get user info

    ```js
     user = await api.fetch(`/api/info?app_id=${app_id}`, {
            message: message,
            headers: {
                'Authorization': `Bearer ${jwtSession.value}`,
                'Content-Type': 'application/json',
            }
        });
     ```

## Deloy

### Vercel 配置

```dotenv
enabled_db=false
supabase_api_url=
supabase_api_key=

upstash_api_url=
upstash_api_token=

enabled_smtp=false
smtp_url=smtp://username:passwd@smtp.xxxx.com:587

cf_turnstile_site_key=
cf_turnstile_secret_key=

github_client_id=
github_client_secret=
google_client_id=
google_client_secret=
ms_client_id=
ms_client_secret=

app_settings__0__app_id=demo
app_settings__0__app_secret=demo_secret
app_settings__0__redirect_url=
app_settings__1__app_id=app2
app_settings__1__app_secret=app_secret2
app_settings__1__redirect_url=http://localhost:5000/callback
```

### Docker

使用 `docker-compose.yml` 部署

```yaml
services:
  awsl-auth:
    image: "gcr.io/dreamhunter2333/awsl-auth:latest"
    build:
      context: .
      dockerfile: dockerfile
    container_name: "awsl-auth"
    ports:
      - "8000:8000"
    volumes:
      - ./data:/data
      - /dev/null:/app/.env
    environment:
      # 数据库
      - enabled_db=true
      - db_client_type=sqlite
      - sqlite_db_url=sqlite:////data/db.sqlite3
      # Redis
      - token_client_type=redis
      - redis_url=redis://awsl-auth-redis:6379/0
      # 邮件注册
      - enabled_smtp=false
      # - smtp_url=smtp://username:passwd@smtp.xxxx.com:587
      # 邮件注册人机验证
      # - cf_turnstile_site_key=
      # - cf_turnstile_secret_key=
      # 第三方登录
      # - github_client_id=
      # - github_client_secret=
      # - google_client_id=
      # - google_client_secret=
      # - enabled_web3_client=true
      # - ms_client_id=
      # - ms_client_secret=
      # 登录App设置
      - app_settings__0__app_id=demo
      - app_settings__0__app_secret=demo_secret
      - app_settings__0__redirect_url=
      - app_settings__1__app_id=app2
      - app_settings__1__app_secret=app_secret2
      - app_settings__1__redirect_url=http://localhost:5000/callback

    depends_on:
      - awsl-auth-redis

  awsl-auth-redis:
    image: "redis:alpine"
    container_name: "awsl-auth-redis"
    ports:
      - "6379:6379"
```
