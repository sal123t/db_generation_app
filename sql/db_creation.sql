-- Database: school_diary

--DROP DATABASE IF EXISTS school_diary;

CREATE DATABASE school_diary
	WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE school_diary
    IS 'Administrative school database';