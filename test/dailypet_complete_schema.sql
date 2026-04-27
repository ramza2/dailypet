--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: dog_chat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dog_chat (
    id integer NOT NULL,
    message text,
    response text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    dog_id integer,
    message_embedding text,
    llm_provider text DEFAULT 'ollama'::text NOT NULL,
    prompt_template_text text,
    uid character varying(50) NOT NULL
);


--
-- Name: dog_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dog_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dog_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dog_chat_id_seq OWNED BY public.dog_chat.id;


--
-- Name: dog_doc; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.dog_doc (
    id integer NOT NULL,
    content text NOT NULL,
    embedding text NOT NULL,
    source text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    loader_type text
);


--
-- Name: dog_doc_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.dog_doc_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dog_doc_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.dog_doc_id_seq OWNED BY public.dog_doc.id;


--
-- Name: prompt_template; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.prompt_template (
    id integer NOT NULL,
    name text NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone
);


--
-- Name: prompt_template_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.prompt_template_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: prompt_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.prompt_template_id_seq OWNED BY public.prompt_template.id;


--
-- Name: t_basic_feed; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_basic_feed (
    idt_basic_feed integer NOT NULL,
    idt_pet integer NOT NULL,
    cups double precision NOT NULL,
    feed_count integer NOT NULL
);


--
-- Name: t_basic_feed_idt_basic_feed_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_basic_feed_idt_basic_feed_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_basic_feed_idt_basic_feed_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_basic_feed_idt_basic_feed_seq OWNED BY public.t_basic_feed.idt_basic_feed;


--
-- Name: t_board; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_board (
    idt_board integer NOT NULL,
    type_code character varying(4) NOT NULL,
    uid character varying(255) NOT NULL,
    title character varying(250) NOT NULL,
    content character varying(4000) NOT NULL,
    view_count integer DEFAULT 0,
    del_yn character varying(1) DEFAULT 'N'::character varying,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_board_file; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_board_file (
    idt_file integer NOT NULL,
    idt_board integer NOT NULL,
    file_path character varying(500) NOT NULL,
    file_name character varying(500) NOT NULL,
    file_size integer NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_board_file_idt_file_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_board_file_idt_file_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_board_file_idt_file_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_board_file_idt_file_seq OWNED BY public.t_board_file.idt_file;


--
-- Name: t_board_idt_board_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_board_idt_board_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_board_idt_board_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_board_idt_board_seq OWNED BY public.t_board.idt_board;


--
-- Name: t_board_reply; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_board_reply (
    idt_reply integer NOT NULL,
    idt_board integer NOT NULL,
    uid character varying(255) NOT NULL,
    idt_org_reply integer NOT NULL,
    group_ord integer DEFAULT 0,
    group_layer integer DEFAULT 0,
    reply character varying(4000) NOT NULL,
    del_yn character varying(1) DEFAULT 'N'::character varying,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_board_reply_idt_reply_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_board_reply_idt_reply_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_board_reply_idt_reply_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_board_reply_idt_reply_seq OWNED BY public.t_board_reply.idt_reply;


--
-- Name: t_board_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_board_type (
    type_code character varying(4) NOT NULL,
    type_desc character varying(45) NOT NULL
);


--
-- Name: t_breed_info; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_breed_info (
    idt_breed_info integer NOT NULL,
    breed_kor character varying(45),
    breed_eng character varying(128),
    fci character varying(4),
    body_shape character varying(1),
    weight_min integer,
    weitgt_max integer,
    life_min integer,
    life_max integer,
    height_min integer,
    height_max integer,
    brachycephalic character varying(1),
    long_haired character varying(1),
    temperament1 text,
    temperament2 text,
    temperament3 text,
    temperament4 text,
    temperament5 text,
    temperament6 text,
    temperament7 text,
    adaptability character varying(1),
    apartment_friendly character varying(1),
    bark character varying(1),
    cat_friendly character varying(1),
    kids_friendly character varying(1),
    other_dog_friendly character varying(1),
    need_exercise character varying(1),
    grooming_degree character varying(1),
    hypoallergenic character varying(1),
    health_issue_degree character varying(1),
    intelligence character varying(1),
    playfulness character varying(1),
    hair_loss character varying(1),
    stranger_friendly character varying(1),
    trainability character varying(1),
    surveillance character varying(1),
    health_issue text,
    exercise text,
    grooming text,
    feature text
);


--
-- Name: t_breed_info_idt_breed_info_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_breed_info_idt_breed_info_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_breed_info_idt_breed_info_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_breed_info_idt_breed_info_seq OWNED BY public.t_breed_info.idt_breed_info;


--
-- Name: t_event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_event (
    idevent integer NOT NULL,
    subject character varying(500) NOT NULL,
    content text NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_event_idevent_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_event_idevent_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_event_idevent_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_event_idevent_seq OWNED BY public.t_event.idevent;


--
-- Name: t_family; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_family (
    idt_family integer NOT NULL,
    uid character varying(255) NOT NULL,
    name character varying(128),
    member_limit integer DEFAULT 10 NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_family_idt_family_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_family_idt_family_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_family_idt_family_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_family_idt_family_seq OWNED BY public.t_family.idt_family;


--
-- Name: t_family_member; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_family_member (
    idt_family integer NOT NULL,
    uid character varying(255) NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_feed; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_feed (
    idt_feed integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    cups double precision,
    feed_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_feed_idt_feed_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_feed_idt_feed_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_feed_idt_feed_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_feed_idt_feed_seq OWNED BY public.t_feed.idt_feed;


--
-- Name: t_invite; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_invite (
    idt_invite integer NOT NULL,
    idt_family integer NOT NULL,
    uid character varying(255) NOT NULL,
    phone character varying(45) NOT NULL,
    accept_yn character varying(1),
    invite_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_invite_idt_invite_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_invite_idt_invite_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_invite_idt_invite_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_invite_idt_invite_seq OWNED BY public.t_invite.idt_invite;


--
-- Name: t_measure_pulse; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_measure_pulse (
    idt_measure_pulse integer NOT NULL,
    idt_pet integer NOT NULL,
    file_path character varying(1000),
    heart_rate integer NOT NULL,
    ar_per double precision,
    keti_heart_rate integer,
    keti_ar_per double precision,
    avg_s1_amp integer,
    max_s1_amp integer,
    min_s1_amp integer,
    avg_s1_period integer,
    max_s1_period integer,
    min_s1_period integer,
    s1_count integer,
    avg_s2_amp integer,
    max_s2_amp integer,
    min_s2_amp integer,
    avg_s2_period integer,
    max_s2_period integer,
    min_s2_period integer,
    s2_count integer,
    measure_time integer,
    correct_rate double precision,
    valid_yn character varying(1),
    raw_temp text,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_measure_pulse_idt_measure_pulse_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_measure_pulse_idt_measure_pulse_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_measure_pulse_idt_measure_pulse_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_measure_pulse_idt_measure_pulse_seq OWNED BY public.t_measure_pulse.idt_measure_pulse;


--
-- Name: t_measure_respiration; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_measure_respiration (
    idt_measure_respiration integer NOT NULL,
    idt_pet integer NOT NULL,
    file_path character varying(1000),
    duration double precision,
    phase integer,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_measure_respiration_idt_measure_respiration_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_measure_respiration_idt_measure_respiration_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_measure_respiration_idt_measure_respiration_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_measure_respiration_idt_measure_respiration_seq OWNED BY public.t_measure_respiration.idt_measure_respiration;


--
-- Name: t_notice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_notice (
    idnotice integer NOT NULL,
    subject character varying(500) NOT NULL,
    content text NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_notice_idnotice_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_notice_idnotice_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_notice_idnotice_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_notice_idnotice_seq OWNED BY public.t_notice.idnotice;


--
-- Name: t_pet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_pet (
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    name character varying(45) NOT NULL,
    thumb_type character varying(1) DEFAULT 'N'::character varying,
    thumb_content character varying(255),
    gender character varying(1) NOT NULL,
    neutering_yn character varying(1) NOT NULL,
    birthday date NOT NULL,
    adoption_date date NOT NULL,
    breed character varying(45) NOT NULL,
    weight double precision DEFAULT 0 NOT NULL,
    classification character varying(1) NOT NULL,
    regist_number character varying(128),
    deleted boolean DEFAULT false NOT NULL,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    bcs_type character varying(20),
    bcs_score integer,
    health_status character varying(20),
    health_issues character varying(255),
    last_checkup_date date
);


--
-- Name: t_pet_idt_pet_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_pet_idt_pet_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_pet_idt_pet_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_pet_idt_pet_seq OWNED BY public.t_pet.idt_pet;


--
-- Name: t_pulse; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_pulse (
    idt_pulse integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    idt_measure_pulse integer,
    pulse integer NOT NULL,
    pulse_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_pulse_idt_pulse_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_pulse_idt_pulse_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_pulse_idt_pulse_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_pulse_idt_pulse_seq OWNED BY public.t_pulse.idt_pulse;


--
-- Name: t_respiration; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_respiration (
    idt_respiration integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    idt_measure_respiration integer,
    respiration integer NOT NULL,
    respiration_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_respiration_idt_respiration_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_respiration_idt_respiration_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_respiration_idt_respiration_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_respiration_idt_respiration_seq OWNED BY public.t_respiration.idt_respiration;


--
-- Name: t_snack; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_snack (
    idt_snack integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    snack_name character varying(45) NOT NULL,
    count integer,
    snack_date date DEFAULT CURRENT_DATE
);


--
-- Name: t_snack_idt_snack_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_snack_idt_snack_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_snack_idt_snack_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_snack_idt_snack_seq OWNED BY public.t_snack.idt_snack;


--
-- Name: t_snack_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_snack_type (
    idt_pet integer NOT NULL,
    name character varying(45) NOT NULL
);


--
-- Name: t_stress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_stress (
    idt_stress integer NOT NULL,
    idt_pet integer NOT NULL,
    idt_measure_pulse integer,
    stress integer NOT NULL,
    stress_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_stress_idt_stress_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_stress_idt_stress_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_stress_idt_stress_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_stress_idt_stress_seq OWNED BY public.t_stress.idt_stress;


--
-- Name: t_talk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_talk (
    idt_talk integer NOT NULL,
    uid character varying(255) NOT NULL,
    idt_family integer NOT NULL,
    type character varying(2) DEFAULT 'TT'::character varying NOT NULL,
    talk text,
    talk_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_talk_has_t_pet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_talk_has_t_pet (
    idt_talk integer NOT NULL,
    idt_pet integer NOT NULL
);


--
-- Name: t_talk_idt_talk_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_talk_idt_talk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_talk_idt_talk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_talk_idt_talk_seq OWNED BY public.t_talk.idt_talk;


--
-- Name: t_temperature; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_temperature (
    idt_body_heat integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    idt_measure_pulse integer,
    temp double precision NOT NULL,
    temp_a double precision,
    temp_h double precision,
    temp_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_temperature_idt_body_heat_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_temperature_idt_body_heat_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_temperature_idt_body_heat_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_temperature_idt_body_heat_seq OWNED BY public.t_temperature.idt_body_heat;


--
-- Name: t_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_user (
    uid character varying(255) NOT NULL,
    push_key character varying(500),
    id character varying(45) NOT NULL,
    phone character varying(45) NOT NULL,
    thumb_type character varying(1) DEFAULT 'N'::character varying NOT NULL,
    thumb_content character varying(255),
    name character varying(45),
    address character varying(255),
    deleted boolean DEFAULT false NOT NULL,
    name_changed_dt timestamp without time zone,
    create_dt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: t_walk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.t_walk (
    idt_walk integer NOT NULL,
    idt_pet integer NOT NULL,
    uid character varying(255) NOT NULL,
    walk_minute integer,
    walk_distance double precision,
    walk_dt character varying(10) NOT NULL
);


--
-- Name: t_walk_idt_walk_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.t_walk_idt_walk_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: t_walk_idt_walk_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.t_walk_idt_walk_seq OWNED BY public.t_walk.idt_walk;


--
-- Name: dog_chat id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_chat ALTER COLUMN id SET DEFAULT nextval('public.dog_chat_id_seq'::regclass);


--
-- Name: dog_doc id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_doc ALTER COLUMN id SET DEFAULT nextval('public.dog_doc_id_seq'::regclass);


--
-- Name: prompt_template id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_template ALTER COLUMN id SET DEFAULT nextval('public.prompt_template_id_seq'::regclass);


--
-- Name: t_basic_feed idt_basic_feed; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_basic_feed ALTER COLUMN idt_basic_feed SET DEFAULT nextval('public.t_basic_feed_idt_basic_feed_seq'::regclass);


--
-- Name: t_board idt_board; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board ALTER COLUMN idt_board SET DEFAULT nextval('public.t_board_idt_board_seq'::regclass);


--
-- Name: t_board_file idt_file; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_file ALTER COLUMN idt_file SET DEFAULT nextval('public.t_board_file_idt_file_seq'::regclass);


--
-- Name: t_board_reply idt_reply; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_reply ALTER COLUMN idt_reply SET DEFAULT nextval('public.t_board_reply_idt_reply_seq'::regclass);


--
-- Name: t_breed_info idt_breed_info; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_breed_info ALTER COLUMN idt_breed_info SET DEFAULT nextval('public.t_breed_info_idt_breed_info_seq'::regclass);


--
-- Name: t_event idevent; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_event ALTER COLUMN idevent SET DEFAULT nextval('public.t_event_idevent_seq'::regclass);


--
-- Name: t_family idt_family; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family ALTER COLUMN idt_family SET DEFAULT nextval('public.t_family_idt_family_seq'::regclass);


--
-- Name: t_feed idt_feed; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_feed ALTER COLUMN idt_feed SET DEFAULT nextval('public.t_feed_idt_feed_seq'::regclass);


--
-- Name: t_invite idt_invite; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_invite ALTER COLUMN idt_invite SET DEFAULT nextval('public.t_invite_idt_invite_seq'::regclass);


--
-- Name: t_measure_pulse idt_measure_pulse; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_pulse ALTER COLUMN idt_measure_pulse SET DEFAULT nextval('public.t_measure_pulse_idt_measure_pulse_seq'::regclass);


--
-- Name: t_measure_respiration idt_measure_respiration; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_respiration ALTER COLUMN idt_measure_respiration SET DEFAULT nextval('public.t_measure_respiration_idt_measure_respiration_seq'::regclass);


--
-- Name: t_notice idnotice; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_notice ALTER COLUMN idnotice SET DEFAULT nextval('public.t_notice_idnotice_seq'::regclass);


--
-- Name: t_pet idt_pet; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pet ALTER COLUMN idt_pet SET DEFAULT nextval('public.t_pet_idt_pet_seq'::regclass);


--
-- Name: t_pulse idt_pulse; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pulse ALTER COLUMN idt_pulse SET DEFAULT nextval('public.t_pulse_idt_pulse_seq'::regclass);


--
-- Name: t_respiration idt_respiration; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_respiration ALTER COLUMN idt_respiration SET DEFAULT nextval('public.t_respiration_idt_respiration_seq'::regclass);


--
-- Name: t_snack idt_snack; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack ALTER COLUMN idt_snack SET DEFAULT nextval('public.t_snack_idt_snack_seq'::regclass);


--
-- Name: t_stress idt_stress; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_stress ALTER COLUMN idt_stress SET DEFAULT nextval('public.t_stress_idt_stress_seq'::regclass);


--
-- Name: t_talk idt_talk; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk ALTER COLUMN idt_talk SET DEFAULT nextval('public.t_talk_idt_talk_seq'::regclass);


--
-- Name: t_temperature idt_body_heat; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_temperature ALTER COLUMN idt_body_heat SET DEFAULT nextval('public.t_temperature_idt_body_heat_seq'::regclass);


--
-- Name: t_walk idt_walk; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_walk ALTER COLUMN idt_walk SET DEFAULT nextval('public.t_walk_idt_walk_seq'::regclass);


--
-- Name: dog_chat dog_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_chat
    ADD CONSTRAINT dog_chat_pkey PRIMARY KEY (id);


--
-- Name: dog_doc dog_doc_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_doc
    ADD CONSTRAINT dog_doc_pkey PRIMARY KEY (id);


--
-- Name: prompt_template prompt_template_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.prompt_template
    ADD CONSTRAINT prompt_template_pkey PRIMARY KEY (id);


--
-- Name: t_basic_feed t_basic_feed_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_basic_feed
    ADD CONSTRAINT t_basic_feed_pkey PRIMARY KEY (idt_basic_feed);


--
-- Name: t_board_file t_board_file_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_file
    ADD CONSTRAINT t_board_file_pkey PRIMARY KEY (idt_file);


--
-- Name: t_board t_board_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board
    ADD CONSTRAINT t_board_pkey PRIMARY KEY (idt_board);


--
-- Name: t_board_reply t_board_reply_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_reply
    ADD CONSTRAINT t_board_reply_pkey PRIMARY KEY (idt_reply);


--
-- Name: t_board_type t_board_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_type
    ADD CONSTRAINT t_board_type_pkey PRIMARY KEY (type_code);


--
-- Name: t_breed_info t_breed_info_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_breed_info
    ADD CONSTRAINT t_breed_info_pkey PRIMARY KEY (idt_breed_info);


--
-- Name: t_event t_event_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_event
    ADD CONSTRAINT t_event_pkey PRIMARY KEY (idevent);


--
-- Name: t_family_member t_family_member_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family_member
    ADD CONSTRAINT t_family_member_pkey PRIMARY KEY (idt_family, uid);


--
-- Name: t_family t_family_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family
    ADD CONSTRAINT t_family_pkey PRIMARY KEY (idt_family);


--
-- Name: t_feed t_feed_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_feed
    ADD CONSTRAINT t_feed_pkey PRIMARY KEY (idt_feed);


--
-- Name: t_invite t_invite_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_invite
    ADD CONSTRAINT t_invite_pkey PRIMARY KEY (idt_invite);


--
-- Name: t_measure_pulse t_measure_pulse_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_pulse
    ADD CONSTRAINT t_measure_pulse_pkey PRIMARY KEY (idt_measure_pulse);


--
-- Name: t_measure_respiration t_measure_respiration_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_respiration
    ADD CONSTRAINT t_measure_respiration_pkey PRIMARY KEY (idt_measure_respiration);


--
-- Name: t_notice t_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_notice
    ADD CONSTRAINT t_notice_pkey PRIMARY KEY (idnotice);


--
-- Name: t_pet t_pet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pet
    ADD CONSTRAINT t_pet_pkey PRIMARY KEY (idt_pet);


--
-- Name: t_pulse t_pulse_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pulse
    ADD CONSTRAINT t_pulse_pkey PRIMARY KEY (idt_pulse);


--
-- Name: t_respiration t_respiration_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_respiration
    ADD CONSTRAINT t_respiration_pkey PRIMARY KEY (idt_respiration);


--
-- Name: t_snack t_snack_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack
    ADD CONSTRAINT t_snack_pkey PRIMARY KEY (idt_snack);


--
-- Name: t_snack_type t_snack_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack_type
    ADD CONSTRAINT t_snack_type_pkey PRIMARY KEY (idt_pet, name);


--
-- Name: t_stress t_stress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_stress
    ADD CONSTRAINT t_stress_pkey PRIMARY KEY (idt_stress);


--
-- Name: t_talk_has_t_pet t_talk_has_t_pet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk_has_t_pet
    ADD CONSTRAINT t_talk_has_t_pet_pkey PRIMARY KEY (idt_talk, idt_pet);


--
-- Name: t_talk t_talk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk
    ADD CONSTRAINT t_talk_pkey PRIMARY KEY (idt_talk);


--
-- Name: t_temperature t_temperature_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_temperature
    ADD CONSTRAINT t_temperature_pkey PRIMARY KEY (idt_body_heat);


--
-- Name: t_user t_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_user
    ADD CONSTRAINT t_user_pkey PRIMARY KEY (uid);


--
-- Name: t_walk t_walk_idt_pet_walk_dt_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_walk
    ADD CONSTRAINT t_walk_idt_pet_walk_dt_key UNIQUE (idt_pet, walk_dt);


--
-- Name: t_walk t_walk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_walk
    ADD CONSTRAINT t_walk_pkey PRIMARY KEY (idt_walk);


--
-- Name: dog_chat dog_chat_dog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_chat
    ADD CONSTRAINT dog_chat_dog_id_fkey FOREIGN KEY (dog_id) REFERENCES public.t_pet(idt_pet);


--
-- Name: dog_chat fk_dog_chat_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.dog_chat
    ADD CONSTRAINT fk_dog_chat_user FOREIGN KEY (uid) REFERENCES public.t_user(uid);


--
-- Name: t_basic_feed t_basic_feed_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_basic_feed
    ADD CONSTRAINT t_basic_feed_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_board_file t_board_file_idt_board_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_file
    ADD CONSTRAINT t_board_file_idt_board_fkey FOREIGN KEY (idt_board) REFERENCES public.t_board(idt_board) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_board_reply t_board_reply_idt_board_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_reply
    ADD CONSTRAINT t_board_reply_idt_board_fkey FOREIGN KEY (idt_board) REFERENCES public.t_board(idt_board) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_board_reply t_board_reply_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board_reply
    ADD CONSTRAINT t_board_reply_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_board t_board_type_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board
    ADD CONSTRAINT t_board_type_code_fkey FOREIGN KEY (type_code) REFERENCES public.t_board_type(type_code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_board t_board_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_board
    ADD CONSTRAINT t_board_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_family_member t_family_member_idt_family_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family_member
    ADD CONSTRAINT t_family_member_idt_family_fkey FOREIGN KEY (idt_family) REFERENCES public.t_family(idt_family) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_family_member t_family_member_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family_member
    ADD CONSTRAINT t_family_member_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_family t_family_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_family
    ADD CONSTRAINT t_family_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_feed t_feed_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_feed
    ADD CONSTRAINT t_feed_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_feed t_feed_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_feed
    ADD CONSTRAINT t_feed_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_invite t_invite_idt_family_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_invite
    ADD CONSTRAINT t_invite_idt_family_fkey FOREIGN KEY (idt_family) REFERENCES public.t_family(idt_family) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_invite t_invite_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_invite
    ADD CONSTRAINT t_invite_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_measure_pulse t_measure_pulse_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_pulse
    ADD CONSTRAINT t_measure_pulse_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_measure_respiration t_measure_respiration_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_measure_respiration
    ADD CONSTRAINT t_measure_respiration_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_pet t_pet_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pet
    ADD CONSTRAINT t_pet_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_pulse t_pulse_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pulse
    ADD CONSTRAINT t_pulse_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_pulse t_pulse_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_pulse
    ADD CONSTRAINT t_pulse_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_respiration t_respiration_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_respiration
    ADD CONSTRAINT t_respiration_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_respiration t_respiration_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_respiration
    ADD CONSTRAINT t_respiration_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_snack t_snack_idt_pet_snack_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack
    ADD CONSTRAINT t_snack_idt_pet_snack_name_fkey FOREIGN KEY (idt_pet, snack_name) REFERENCES public.t_snack_type(idt_pet, name) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_snack_type t_snack_type_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack_type
    ADD CONSTRAINT t_snack_type_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_snack t_snack_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_snack
    ADD CONSTRAINT t_snack_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_stress t_stress_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_stress
    ADD CONSTRAINT t_stress_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_talk_has_t_pet t_talk_has_t_pet_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk_has_t_pet
    ADD CONSTRAINT t_talk_has_t_pet_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_talk_has_t_pet t_talk_has_t_pet_idt_talk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk_has_t_pet
    ADD CONSTRAINT t_talk_has_t_pet_idt_talk_fkey FOREIGN KEY (idt_talk) REFERENCES public.t_talk(idt_talk) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_talk t_talk_idt_family_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk
    ADD CONSTRAINT t_talk_idt_family_fkey FOREIGN KEY (idt_family) REFERENCES public.t_family(idt_family) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_talk t_talk_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_talk
    ADD CONSTRAINT t_talk_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_temperature t_temperature_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_temperature
    ADD CONSTRAINT t_temperature_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_temperature t_temperature_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_temperature
    ADD CONSTRAINT t_temperature_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_walk t_walk_idt_pet_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_walk
    ADD CONSTRAINT t_walk_idt_pet_fkey FOREIGN KEY (idt_pet) REFERENCES public.t_pet(idt_pet) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: t_walk t_walk_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.t_walk
    ADD CONSTRAINT t_walk_uid_fkey FOREIGN KEY (uid) REFERENCES public.t_user(uid) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

