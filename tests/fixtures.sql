--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: computer; Type: TABLE; Schema: public; Owner: pymm
--

CREATE TABLE computer (
    computer_id bigint NOT NULL,
    name text NOT NULL,
    ip inet NOT NULL,
    public boolean NOT NULL,
    additional_infos jsonb
);


ALTER TABLE computer OWNER TO pymm;

--
-- Name: computer_computer_id_seq; Type: SEQUENCE; Schema: public; Owner: pymm
--

CREATE SEQUENCE computer_computer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE computer_computer_id_seq OWNER TO pymm;

--
-- Name: computer_computer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pymm
--

ALTER SEQUENCE computer_computer_id_seq OWNED BY computer.computer_id;


--
-- Name: manager; Type: TABLE; Schema: public; Owner: pymm
--

CREATE TABLE manager (
    user_id bigint NOT NULL,
    username text,
    first_name text,
    last_name text,
    birth timestamp with time zone,
    is_admin boolean
);


ALTER TABLE manager OWNER TO pymm;

--
-- Name: manager_user_id_seq; Type: SEQUENCE; Schema: public; Owner: pymm
--

CREATE SEQUENCE manager_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE manager_user_id_seq OWNER TO pymm;

--
-- Name: manager_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pymm
--

ALTER SEQUENCE manager_user_id_seq OWNED BY manager.user_id;


--
-- Name: computer_id; Type: DEFAULT; Schema: public; Owner: pymm
--

ALTER TABLE ONLY computer ALTER COLUMN computer_id SET DEFAULT nextval('computer_computer_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: pymm
--

ALTER TABLE ONLY manager ALTER COLUMN user_id SET DEFAULT nextval('manager_user_id_seq'::regclass);


--
-- Data for Name: computer; Type: TABLE DATA; Schema: public; Owner: pymm
--

COPY computer (computer_id, name, ip, public, additional_infos) FROM stdin;
1	desktop	192.168.0.1	f	\N
2	laptop	192.168.0.2	f	{"brand": "thinkpad"}
4	front1	10.28.123.19	t	\N
6	back1	10.28.123.10	f	\N
5	front2	10.28.123.9	t	{"mode": "degraded"}
3	ci	192.168.0.8	t	\N
7	back2	192.168.0.6	f	\N
\.


--
-- Name: computer_computer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pymm
--

SELECT pg_catalog.setval('computer_computer_id_seq', 7, true);


--
-- Data for Name: manager; Type: TABLE DATA; Schema: public; Owner: pymm
--

COPY manager (user_id, username, first_name, last_name, birth, is_admin) FROM stdin;
1	tadmin	thibaut	claquetin	2012-12-24 13:22:22+01	t
2	simpleplan	simple	plan	1989-12-12 13:22:22+01	f
\.


--
-- Name: manager_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pymm
--

SELECT pg_catalog.setval('manager_user_id_seq', 2, true);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

