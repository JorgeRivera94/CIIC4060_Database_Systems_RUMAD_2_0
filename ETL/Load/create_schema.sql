CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS room (
    rid SERIAL PRIMARY KEY,
    building VARCHAR(50),
    room_number VARCHAR(10),
    capacity INT
);

CREATE TABLE IF NOT EXISTS meeting (
    mid SERIAL PRIMARY KEY,
    ccode VARCHAR(10),
    starttime TIMESTAMP,
    endtime TIMESTAMP,
    cdays VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS class (
    cid SERIAL PRIMARY KEY,
    cname VARCHAR(50),
    ccode VARCHAR(10),
    cdesc VARCHAR(100),
    term VARCHAR(100),
    years VARCHAR(50),
    cred INT,
    csyllabus VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS requisite (
    classid INT REFERENCES class (cid),
    reqid INT REFERENCES class (cid),
    prereq BOOLEAN,
    PRIMARY KEY (classid, reqid)
);

CREATE TABLE IF NOT EXISTS docs (
    did SERIAL PRIMARY KEY,
    docname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS syllabus (
    chunkid SERIAL PRIMARY KEY,
    courseid INT REFERENCES class (cid),
    did INT REFERENCES docs (did),
    embedding_text VECTOR(768),
    chunk VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS section (
    sid SERIAL PRIMARY KEY,
    roomid INT REFERENCES room (rid),
    cid INT REFERENCES class (cid),
    mid INT REFERENCES meeting (mid),
    semester VARCHAR(50),
    years VARCHAR(50),
    capacity INT
);

CREATE TABLE IF NOT EXISTS users (
    uid SERIAL PRIMARY KEY,
    username VARCHAR(50),
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS passwords (
    pid SERIAL PRIMARY KEY,
    password VARCHAR(50),
    uid INT REFERENCES users (uid)
);