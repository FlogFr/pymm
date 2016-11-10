-- This is selecting all information about the schema
-- pymm needs to work with.
-- 
-- This is largely possible to improve it from the definition
-- of the views in the information_schema schema, like 'columns'.
-- For instance improve all the data about the data type from pg_type
SELECT
	a.attname as column_name,
	c.relname AS table_name,
	nc.nspname AS table_schema,
	COALESCE(idx.indisprimary, 'f') as column_pk,
	a.attnum AS ordinal_position,
	NOT a.attnotnull AS is_nullable,
	-- data_type,
	pg_catalog.col_description(c.oid, a.attnum) AS description
FROM
	-- pg_class catalogs tables and most everything that has columns or is
	-- similar to a table
	pg_catalog.pg_class c
	-- pg_attribute stores information about table columns
	JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid
	JOIN pg_catalog.pg_namespace nc ON nc.oid = c.relnamespace
	LEFT JOIN pg_catalog.pg_index idx ON idx.indrelid = a.attrelid
										AND a.attnum = ANY(idx.indkey)
WHERE
	-- only 'r' ordinary table, 't' TOAST table, and 'm' materialized views
	c.relkind = ANY (ARRAY['r'::"char", 't'::"char", 'm'::"char"])
	AND a.attnum > 0
	-- not any columns that are dropped but physically present in PG
	AND NOT a.attisdropped
