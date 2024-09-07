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


ALTER TABLE "users"
   REPLICA IDENTITY FULL;


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

ALTER TABLE "accounts"
   REPLICA IDENTITY FULL;


INSERT INTO "users" (email, name)
VALUES ('oleg@oleg.com', 'Oleg')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


INSERT INTO "accounts" (user_id, currency, balance)
VALUES ('65ee8afb-2de2-4ef4-b25f-508f2e8e54c1', 'EUR', 1001.25)
RETURNING *;


INSERT INTO "users" (email, name)
VALUES ('sonya@sonya.com', 'sonya')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


UPDATE "users"
SET name = 'Mr. Oleg'
WHERE email = 'oleg@oleg.com';


DELETE
FROM "users"
WHERE email = 'sonya@sonya.com';


SELECT * FROM users;