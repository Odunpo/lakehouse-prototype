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
