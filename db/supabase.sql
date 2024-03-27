create table public.awsl_users (
    id bigint generated by default as identity,
    user_name text not null,
    user_email text not null,
    created_at timestamp without time zone not null default now(),
    updated_at timestamp without time zone not null default now(),
    password text not null,
    active boolean not null default true,
    constraint awsl_users_pkey primary key (id),
    constraint awsl_users_user_email_key unique (user_email)
);

create table public.awsl_oauth_users (
    id bigint generated by default as identity,
    login_type text not null,
    user_name text not null,
    user_email text not null,
    web3_account text null,
    origin_data json null,
    created_at timestamp without time zone not null default now(),
    updated_at timestamp without time zone not null default now(),
    constraint awsl_oauth_users_pkey primary key (id),
    constraint awsl_oauth_users_id_key unique (id)
);

create unique index awsl_oauth_users_unique_index on public.awsl_oauth_users using btree (login_type, user_email) tablespace pg_default;