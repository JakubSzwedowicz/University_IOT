--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Ubuntu 14.6-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.6 (Ubuntu 14.6-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: access_level; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.access_level (
    id integer NOT NULL,
    level character varying(255)
);


ALTER TABLE public.access_level OWNER TO postgres;

--
-- Name: access_level_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.access_level_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.access_level_id_seq OWNER TO postgres;

--
-- Name: access_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.access_level_id_seq OWNED BY public.access_level.id;


--
-- Name: authorization_message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorization_message (
    id integer NOT NULL,
    date timestamp without time zone,
    cardid integer NOT NULL,
    deviceid integer NOT NULL,
    authorization_message_statusid integer NOT NULL
);


ALTER TABLE public.authorization_message OWNER TO postgres;

--
-- Name: authorization_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.authorization_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authorization_message_id_seq OWNER TO postgres;

--
-- Name: authorization_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.authorization_message_id_seq OWNED BY public.authorization_message.id;


--
-- Name: authorization_message_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authorization_message_status (
    id integer NOT NULL,
    status character varying(255)
);


ALTER TABLE public.authorization_message_status OWNER TO postgres;

--
-- Name: authorization_message_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.authorization_message_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.authorization_message_status_id_seq OWNER TO postgres;

--
-- Name: authorization_message_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.authorization_message_status_id_seq OWNED BY public.authorization_message_status.id;


--
-- Name: card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.card (
    id integer NOT NULL,
    rfid_tag integer,
    employeeid integer NOT NULL,
    card_statusid integer NOT NULL
);


ALTER TABLE public.card OWNER TO postgres;

--
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.card_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.card_id_seq OWNER TO postgres;

--
-- Name: card_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.card_id_seq OWNED BY public.card.id;


--
-- Name: card_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.card_status (
    id integer NOT NULL,
    status character varying(255)
);


ALTER TABLE public.card_status OWNER TO postgres;

--
-- Name: card_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.card_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.card_status_id_seq OWNER TO postgres;

--
-- Name: card_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.card_status_id_seq OWNED BY public.card_status.id;


--
-- Name: device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.device (
    id integer NOT NULL,
    mac_address character varying(255)
);


ALTER TABLE public.device OWNER TO postgres;

--
-- Name: device_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.device_id_seq OWNER TO postgres;

--
-- Name: device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.device_id_seq OWNED BY public.device.id;


--
-- Name: door; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.door (
    id integer NOT NULL,
    description character varying(255),
    deviceid integer NOT NULL,
    access_levelid integer NOT NULL
);


ALTER TABLE public.door OWNER TO postgres;

--
-- Name: door_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.door_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.door_id_seq OWNER TO postgres;

--
-- Name: door_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.door_id_seq OWNED BY public.door.id;


--
-- Name: employee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employee (
    id integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    access_levelid integer NOT NULL
);


ALTER TABLE public.employee OWNER TO postgres;

--
-- Name: employee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.employee_id_seq OWNER TO postgres;

--
-- Name: employee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employee_id_seq OWNED BY public.employee.id;


--
-- Name: access_level id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_level ALTER COLUMN id SET DEFAULT nextval('public.access_level_id_seq'::regclass);


--
-- Name: authorization_message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message ALTER COLUMN id SET DEFAULT nextval('public.authorization_message_id_seq'::regclass);


--
-- Name: authorization_message_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message_status ALTER COLUMN id SET DEFAULT nextval('public.authorization_message_status_id_seq'::regclass);


--
-- Name: card id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card ALTER COLUMN id SET DEFAULT nextval('public.card_id_seq'::regclass);


--
-- Name: card_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card_status ALTER COLUMN id SET DEFAULT nextval('public.card_status_id_seq'::regclass);


--
-- Name: device id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device ALTER COLUMN id SET DEFAULT nextval('public.device_id_seq'::regclass);


--
-- Name: door id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.door ALTER COLUMN id SET DEFAULT nextval('public.door_id_seq'::regclass);


--
-- Name: employee id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee ALTER COLUMN id SET DEFAULT nextval('public.employee_id_seq'::regclass);


--
-- Data for Name: access_level; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.access_level (id, level) FROM stdin;
1	L1
2	L2
3	L3
\.


--
-- Data for Name: authorization_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authorization_message (id, date, cardid, deviceid, authorization_message_statusid) FROM stdin;
1	1992-10-20 18:54:43	38	1	3
2	1998-05-10 22:05:11	3	4	1
3	2009-07-14 04:35:02	9	2	3
4	1982-06-26 19:01:55	4	6	3
5	2006-10-06 07:55:38	15	3	1
6	2013-11-03 04:22:44	39	3	2
7	1981-03-19 01:46:01	32	3	3
8	2008-12-12 10:58:55	38	6	3
9	1995-09-25 01:28:59	40	3	2
10	2003-10-07 14:11:34	26	3	1
11	1970-02-28 20:09:31	6	4	3
12	1979-01-17 17:51:27	44	1	2
13	1988-12-23 17:23:00	27	4	1
14	2016-08-06 17:28:44	32	5	1
15	2000-01-07 02:27:27	12	5	3
16	1976-01-31 04:57:22	34	1	3
17	2018-06-26 12:56:53	11	2	3
18	1981-10-21 20:31:03	13	1	1
19	2011-05-03 09:25:01	18	3	2
20	1995-05-21 13:21:45	11	1	3
21	1990-04-22 05:11:53	17	2	3
22	1995-09-27 05:26:28	3	2	1
23	1998-11-17 11:49:15	6	2	3
24	1989-04-16 01:01:36	2	1	3
25	2008-09-06 05:52:30	13	6	3
26	2013-06-28 14:54:00	9	6	1
27	2009-06-18 21:12:39	5	6	1
28	1978-06-28 13:15:54	42	6	2
29	1988-07-05 07:55:34	19	3	2
30	2013-07-29 15:47:25	12	6	1
31	1988-02-25 15:13:18	23	2	2
32	1975-11-15 13:04:55	32	1	1
33	1995-04-27 10:42:45	6	6	2
34	2008-05-23 02:44:30	29	6	2
35	2013-06-12 18:05:50	30	4	3
36	1999-08-03 16:40:07	37	6	2
37	2013-07-26 20:58:50	2	1	1
38	1975-03-30 04:12:02	6	6	3
39	1980-09-12 01:13:16	16	3	3
40	1981-12-23 10:06:17	43	6	3
41	1984-05-04 10:34:49	8	4	3
42	2009-10-20 06:53:57	22	5	1
43	2021-07-30 16:31:45	15	1	1
44	1981-11-21 11:38:21	15	6	3
45	1991-02-22 09:34:43	35	4	3
46	2021-11-11 05:16:15	25	2	3
47	2009-04-12 02:59:49	21	6	3
48	1985-05-22 06:56:29	33	4	2
49	2016-03-06 23:56:10	22	3	3
50	1979-04-04 02:54:59	20	6	2
51	2001-01-29 00:46:54	39	2	3
52	1980-12-24 01:26:18	37	4	2
53	1983-01-10 13:22:13	12	3	3
54	2005-12-19 02:48:57	12	1	1
55	2005-11-30 20:32:19	41	2	2
56	1977-03-14 23:43:35	23	4	3
57	2002-01-31 12:43:36	14	6	1
58	2016-09-03 16:38:21	39	6	1
59	2013-12-07 00:14:34	39	3	1
60	1974-08-02 02:46:14	23	3	1
61	1999-12-27 05:20:06	33	5	3
62	2012-03-17 08:43:47	11	3	2
63	2001-02-26 14:35:10	37	4	2
64	1981-02-17 21:27:42	42	1	2
65	2015-07-08 13:39:03	21	2	1
66	2021-04-07 05:12:18	19	1	2
67	1993-08-12 04:31:07	22	4	2
68	1980-08-28 11:58:10	19	1	2
69	1979-06-23 03:56:25	28	6	2
70	2006-07-13 10:19:05	18	1	3
71	1998-05-22 11:10:47	33	1	3
72	2001-02-25 18:37:12	31	6	1
73	1993-04-27 11:33:20	18	5	1
74	1979-04-07 08:26:32	42	1	2
75	2004-06-08 04:59:56	2	2	3
76	1990-11-16 05:12:55	25	1	1
77	2020-06-05 08:42:31	24	6	2
78	1978-03-05 02:36:37	14	5	3
79	1971-10-02 21:50:09	10	3	1
80	2020-07-20 23:38:49	38	3	2
81	2014-09-04 06:32:26	39	5	3
82	1972-01-05 16:26:40	4	6	1
83	2008-09-22 11:35:23	18	1	1
84	2022-12-13 00:37:28	21	6	1
85	2020-09-18 15:52:49	26	1	2
86	1993-08-28 12:06:00	31	5	1
87	2015-02-22 00:22:48	11	2	3
88	1972-03-06 15:46:16	8	6	3
89	2007-11-22 21:05:19	44	5	1
90	1998-02-18 22:43:28	20	3	1
91	1973-04-18 21:58:14	18	4	1
92	1971-07-23 05:04:58	33	5	3
93	2021-11-08 09:23:50	2	5	1
94	1988-12-30 11:25:43	16	1	3
95	1976-02-07 06:34:14	43	4	1
96	1994-09-25 08:38:33	20	1	3
97	2005-06-22 08:01:44	38	3	2
98	1989-03-15 16:14:09	33	6	3
99	1990-05-24 13:10:41	32	6	3
100	2006-01-23 02:00:52	4	2	1
\.


--
-- Data for Name: authorization_message_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authorization_message_status (id, status) FROM stdin;
1	request
2	accepted
3	declined
\.


--
-- Data for Name: card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.card (id, rfid_tag, employeeid, card_statusid) FROM stdin;
1	123	8	1
2	124	13	2
3	125	8	1
4	126	16	2
5	127	10	1
6	128	8	2
7	129	12	1
8	130	17	1
9	131	7	1
10	132	8	2
11	133	14	1
12	134	5	1
13	135	19	2
14	136	18	2
15	137	4	1
16	138	5	1
17	139	19	2
18	140	1	2
19	141	7	1
20	142	14	1
21	143	2	1
22	144	4	1
23	145	9	2
24	146	2	1
25	147	6	2
26	148	12	1
27	149	17	2
28	150	11	2
29	151	16	1
30	152	4	1
31	153	1	2
32	154	3	2
33	155	9	1
34	156	6	1
35	157	2	2
36	158	4	1
37	159	13	1
38	160	8	1
39	161	15	1
40	162	1	1
41	163	5	1
42	164	15	1
43	165	12	1
44	166	19	1
45	167	10	1
\.


--
-- Data for Name: card_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.card_status (id, status) FROM stdin;
1	active
2	inactive
\.


--
-- Data for Name: device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.device (id, mac_address) FROM stdin;
1	0D:40:0B:00:0C:01
2	FF:0F:CD:00:23:10
3	AF:B3:5A:11:2D:BB
4	0D:40:0B:00:0C:01
5	AC:40:BB:CD:0C:43
6	EF:BB:A3:FF:0C:D4
\.


--
-- Data for Name: door; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.door (id, description, deviceid, access_levelid) FROM stdin;
1	Main building entry	1	1
2	Floor 1 entry	2	1
3	Lab 1-1 entry	3	2
4	Lab 1-2 entry	4	2
5	Lab 1-3 entry	5	3
6	Floor 2 entry	6	1
\.


--
-- Data for Name: employee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employee (id, first_name, last_name, access_levelid) FROM stdin;
1	Sandra	Pham	3
2	Desiree	Smith	1
3	Andrea	Garcia	1
4	Brittany	Moore	3
5	Cindy	Cooley	2
6	Kyle	Rodriguez	1
7	Stephanie	Henderson	3
8	Angela	Smith	2
9	David	Thornton	2
10	Madeline	Landry	2
11	Michelle	Silva	3
12	Beth	Gross	2
13	Steven	Jacobson	2
14	Lisa	Mcfarland	2
15	Rebecca	Jordan	1
16	James	Price	1
17	Maurice	Miller	1
18	Jennifer	Perez	1
19	Brittany	Bryant	2
20	Walter	Garcia	1
\.


--
-- Name: access_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.access_level_id_seq', 3, true);


--
-- Name: authorization_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.authorization_message_id_seq', 100, true);


--
-- Name: authorization_message_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.authorization_message_status_id_seq', 3, true);


--
-- Name: card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.card_id_seq', 45, true);


--
-- Name: card_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.card_status_id_seq', 2, true);


--
-- Name: device_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.device_id_seq', 6, true);


--
-- Name: door_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.door_id_seq', 6, true);


--
-- Name: employee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employee_id_seq', 20, true);


--
-- Name: access_level access_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_level
    ADD CONSTRAINT access_level_pkey PRIMARY KEY (id);


--
-- Name: authorization_message authorization_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message
    ADD CONSTRAINT authorization_message_pkey PRIMARY KEY (id);


--
-- Name: authorization_message_status authorization_message_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message_status
    ADD CONSTRAINT authorization_message_status_pkey PRIMARY KEY (id);


--
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- Name: card_status card_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card_status
    ADD CONSTRAINT card_status_pkey PRIMARY KEY (id);


--
-- Name: device device_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.device
    ADD CONSTRAINT device_pkey PRIMARY KEY (id);


--
-- Name: door door_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.door
    ADD CONSTRAINT door_pkey PRIMARY KEY (id);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (id);


--
-- Name: authorization_message fkauthorizat676564; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message
    ADD CONSTRAINT fkauthorizat676564 FOREIGN KEY (cardid) REFERENCES public.card(id);


--
-- Name: authorization_message fkauthorizat680726; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message
    ADD CONSTRAINT fkauthorizat680726 FOREIGN KEY (authorization_message_statusid) REFERENCES public.authorization_message_status(id);


--
-- Name: authorization_message fkauthorizat82390; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authorization_message
    ADD CONSTRAINT fkauthorizat82390 FOREIGN KEY (deviceid) REFERENCES public.device(id);


--
-- Name: card fkcard235613; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT fkcard235613 FOREIGN KEY (card_statusid) REFERENCES public.card_status(id);


--
-- Name: card fkcard552886; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT fkcard552886 FOREIGN KEY (employeeid) REFERENCES public.employee(id);


--
-- Name: door fkdoor437543; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.door
    ADD CONSTRAINT fkdoor437543 FOREIGN KEY (access_levelid) REFERENCES public.access_level(id);


--
-- Name: door fkdoor874510; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.door
    ADD CONSTRAINT fkdoor874510 FOREIGN KEY (deviceid) REFERENCES public.device(id);


--
-- Name: employee fkemployee943934; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employee
    ADD CONSTRAINT fkemployee943934 FOREIGN KEY (access_levelid) REFERENCES public.access_level(id);


--
-- PostgreSQL database dump complete
--

