-- One Postgres instance for local dev simplicity; one schema per service so
-- no service can query another's tables. Each service's own SQLAlchemy
-- models create their tables inside their schema at startup.
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS workflow;
CREATE SCHEMA IF NOT EXISTS ai;
CREATE SCHEMA IF NOT EXISTS audit;
CREATE SCHEMA IF NOT EXISTS integration;
