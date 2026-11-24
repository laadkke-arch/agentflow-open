-- AF-RES-231 controls: documented predictions only, not run here.
-- PostgreSQL 16.0 (server_version_num=160000) first; any other exact version separately.
-- psql -X -v ON_ERROR_STOP=1 -f docs/workstreams/research/AF-RES-231/controls.sql
\pset null '(NULL)'
SHOW server_version;
SHOW server_version_num;
BEGIN;
CREATE TEMP TABLE af231(g text NOT NULL,id integer PRIMARY KEY,ts timestamp,payload text);
INSERT INTO af231 VALUES
 ('A',1,'2024-02-01','zeta'),('A',2,'2024-02-01','beta'),
 ('A',3,'2024-01-01','aardvark'),('A',4,NULL,'missing'),
 ('B',5,NULL,'x'),('B',6,NULL,'y');
SELECT * FROM af231 ORDER BY g,id;
\echo 'D0: A4; B5 or B6'
SELECT DISTINCT ON(g) * FROM af231 ORDER BY g,ts DESC;
\echo 'D1: A1 or A2; B5 or B6'
SELECT DISTINCT ON(g) * FROM af231 ORDER BY g,ts DESC NULLS LAST;
\echo 'D2: A1 B5'
SELECT DISTINCT ON(g) * FROM af231 ORDER BY g,ts DESC NULLS LAST,id ASC;
\echo 'D3: A2 B6'
SELECT DISTINCT ON(g) * FROM af231 ORDER BY g,ts DESC NULLS LAST,id DESC;
\echo 'RN0: A1 or A2; B5 or B6'
SELECT g,id,ts,payload FROM (SELECT *,row_number() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST) r FROM af231) x WHERE r=1 ORDER BY g,id;
\echo 'RN1: A1 B5'
SELECT g,id,ts,payload FROM (SELECT *,row_number() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST,id) r FROM af231) x WHERE r=1 ORDER BY g,id;
\echo 'R0: A1 A2 B5 B6'
SELECT g,id,ts,payload FROM (SELECT *,rank() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST) r FROM af231) x WHERE r=1 ORDER BY g,id;
\echo 'R1: A4 B5 B6'
SELECT g,id,ts,payload FROM (SELECT *,rank() OVER(PARTITION BY g ORDER BY ts DESC) r FROM af231) x WHERE r=1 ORDER BY g,id;
\echo 'R2: A1 B5'
SELECT g,id,ts,payload FROM (SELECT *,rank() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST,id) r FROM af231) x WHERE r=1 ORDER BY g,id;
\echo 'R3: A1 A2; B absent'
SELECT g,id,ts,payload FROM (SELECT *,rank() OVER(PARTITION BY g ORDER BY ts DESC NULLS LAST) r FROM af231 WHERE ts IS NOT NULL) x WHERE r=1 ORDER BY g,id;
\echo 'M0: A1 A2; B absent'
SELECT a.* FROM af231 a JOIN (SELECT g,max(ts) m FROM af231 GROUP BY g) b ON a.g=b.g AND a.ts=b.m ORDER BY a.g,a.id;
\echo 'M1: A1 A2 B5 B6'
SELECT a.* FROM af231 a JOIN (SELECT g,max(ts) m FROM af231 GROUP BY g) b ON a.g=b.g AND a.ts IS NOT DISTINCT FROM b.m ORDER BY a.g,a.id;
\echo 'M2: A max 2024-02-01 with aardvark; nonexistent pair'
SELECT g,max(ts),min(payload COLLATE "C") FROM af231 GROUP BY g ORDER BY g;
ROLLBACK;
