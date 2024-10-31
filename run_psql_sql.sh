#!/bin/bash

# Connect to Postgres container and execute multiple SQL commands
docker exec -i postgres psql -U postgres <<EOF
\c bank;

INSERT INTO "users" (id, email, name)
VALUES ('1b214475-9054-4f45-91f4-d111422a7b16', 'bruce@wayne.com', 'Bruce W')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


INSERT INTO "accounts" (user_id, currency, balance)
VALUES ('1b214475-9054-4f45-91f4-d111422a7b16', 'EUR', 1001.25)
RETURNING *;


INSERT INTO "users" (id, email, name)
VALUES ('dbddcfe3-a590-4358-958f-e8ed882df158', 'clark@kent.com', 'Clark Kent')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


INSERT INTO "accounts" (user_id, currency, balance)
VALUES ('dbddcfe3-a590-4358-958f-e8ed882df158', 'EUR', 2500.00)
RETURNING *;

UPDATE "accounts"
SET balance = 3000.00
WHERE user_id = 'dbddcfe3-a590-4358-958f-e8ed882df158';


UPDATE "users"
SET name = 'Bruce Wayne'
WHERE email = 'bruce@wayne.com';


INSERT INTO "users" (email, name)
VALUES ('test@test.com', 'test')
ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
RETURNING *;


DELETE
FROM "users"
WHERE email = 'test@test.com';

EOF