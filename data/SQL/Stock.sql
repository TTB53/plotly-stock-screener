CREATE TABLE IF NOT EXISTS "stock" (
                  "id" INTEGER PRIMARY KEY,
                  "symbol" TEXT NOT NULL UNIQUE,
                  "company" TEXT NOT NULL,
                  "nasdaq_sector" TEXT,
                  "gics_sector" TEXT,
                  "gics_subsector" TEXT,
                  "headquarters" TEXT,
                  "date_added" TEXT ,
                  "CIK INTEGER",
                  "founded" INTEGER
                  );