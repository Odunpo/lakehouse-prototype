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
VALUES ('ec7fa6c2-68cf-4dfa-9673-31dff287cbd1', 'EUR', 1001.25)
RETURNING *;


INSERT INTO "users" (email, name)
VALUES ('sonya@sonya.com', 'Sonya')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


INSERT INTO "accounts" (user_id, currency, balance)
VALUES ('39bf0145-59c6-46aa-a390-b75e62efa3d1', 'EUR', 2500.00)
RETURNING *;

UPDATE "accounts"
SET balance = 3000.00
WHERE user_id = '39bf0145-59c6-46aa-a390-b75e62efa3d1';


UPDATE "users"
SET name = 'Mr. Oleg'
WHERE email = 'oleg@oleg.com';


INSERT INTO "users" (email, name)
VALUES ('test@test.com', 'test')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


DELETE
FROM "users"
WHERE email = 'test@test.com';


SELECT * FROM users;
SELECT * FROM accounts;


SELECT
    u.name,
    a.balance
FROM users u
LEFT JOIN accounts a on u.id = a.user_id;