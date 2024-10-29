\c bank

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS "users"
(
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "email" character varying NOT NULL,
    "name" character varying NOT NULL,
    "created_at" date NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT "UQ_User_email" UNIQUE ("email"),
    CONSTRAINT "PK_User_id" PRIMARY KEY ("id")
);

ALTER TABLE "users" REPLICA IDENTITY FULL;

CREATE TABLE IF NOT EXISTS "accounts"
(
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "user_id" uuid NOT NULL,
    "currency" character varying NOT NULL,
    "balance" numeric(15,2) NOT NULL,
    "created_at" date NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT "PK_Account_id" PRIMARY KEY ("id"),
    CONSTRAINT fk_user FOREIGN KEY ("user_id") REFERENCES "users"("id")
);

ALTER TABLE "accounts" REPLICA IDENTITY FULL;

CREATE PUBLICATION bank_pub FOR TABLE users, accounts;

SELECT * FROM pg_create_logical_replication_slot('bank_slot', 'pgoutput');