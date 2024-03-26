CREATE TABLE IF NOT EXISTS awsl_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    user_email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password TEXT NOT NULL,
    active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS awsl_oauth_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_type TEXT NOT NULL,
    user_name TEXT NOT NULL,
    user_email TEXT NOT NULL,
    web3_account TEXT,
    origin_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS awsl_oauth_users_unique_index ON awsl_oauth_users (login_type, user_email);
