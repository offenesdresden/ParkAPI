from yoyo import step

step("""
CREATE TABLE "public"."parkapi" (
   "id" SERIAL,
   "timestamp_updated" TIMESTAMP NOT NULL,
   "timestamp_downloaded" TIMESTAMP NOT NULL,
   "city" TEXT NOT NULL,"data" JSON NOT NULL,
PRIMARY KEY ("id"))
TABLESPACE "pg_default";
""",
 "create index latest_scrape_index on parkapi (city, timestamp_downloaded DESC);"
)
