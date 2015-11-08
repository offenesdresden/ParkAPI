from yoyo import step

step("""
CREATE TABLE free_lots (
    lot_id text REFERENCES lots (id),
    free int NOT NULL,
    updated_at timestamp,
    downloaded_at timestamp NOT NULL,
    PRIMARY KEY (lot_id, downloaded_at))
     """,
     """DROP TABLE free_lots;""")

step("""
CREATE TABLE lots (
    id text PRIMARY KEY,
    total int,
    seen_total int NOT NULL DEFAULT 0)
     """,
     """DROP TABLE free_lots;""")

step("""
CREATE OR REPLACE FUNCTION partition_free_lots()
RETURNS TRIGGER AS $PROC$
DECLARE
    year text;
    tablename text;
    index text;
    start_date text;
    end_date text;
    create_table_sql text;
    create_index_sql text;
BEGIN
    year := to_char(NEW.created_at, "YYYY");
    tablename := TG_TABLE_SCHEMA || "." || TG_TABLE_NAME || "_" || year;

    EXECUTE "INSERT INTO " || quote_indent(tablename) || " SELECT ($1).*" USING NEW;
    RETURN NULL;
EXCEPTION
    WHEN undefined_table THEN
        start_date := to_char(NEW.created_at, "YYYY-01-01");
        end_date := to_char(NEW.created_at + interval '1 years', "YYYY-12-01");
        create_table_sql := "CREATE TABLE IF NOT EXISTS " || quote_indent(tablename) ||
             " (CHECK (created_at >= timestamp " || quote_literal(start_date) ||
             " AND created_at < timestamp "  || quote_literal(end_date)   ||
             " INHERITS (" || quote_indent(TG_TABLE_SCHEMA || "." || TG_TABLE_NAME) || ")";

        RAISE NOTICE 'CREATE NEW TABLE: %', create_table_sql;
        EXECUTE create_table_sql;

        EXECUTE "INSERT INTO " || tablename || " SELECT ($1).*" USING NEW;
        RETURN NULL;

END;
$PROC$ LANGUAGE plpgsql
     """,
     """DROP FUNCTION partition_free_lots;""")

step("""
CREATE TRIGGER partition_free_lots
     BEFORE INSERT ON free_lots
     FOR EACH ROW EXECUTE PROCEDURE partition_free_lots()
     """,
     """DROP TRIGGER partition_free_lots on free_lots""")

step("""
CREATE OR REPLACE FUNCTION update_total_lots()
RETURNS TRIGGER AS $PROC$
BEGIN
EXECUTE "INSERT INTO lots SELECT ($1).uuid where NOT EXISTS (SELECT uuid from lots where uuid = ($1).uuid)" USING NEW;
EXECUTE "UPDATE lots set seen_total = ($1).free where lot_id = ($1).lot_id and seen_total < ($1).free" USING NEW;
RETURN NULL;
END;
$PROC$ LANGUAGE plpgsql
     """,
     """DROP FUNCTION update_total_lots;""")

step("""
CREATE TRIGGER update_total_lots
     BEFORE INSERT ON free_lots
     FOR EACH ROW EXECUTE PROCEDURE update_total_lots()
     """,
     """DROP TRIGGER update_total_lots on free_lots""")
