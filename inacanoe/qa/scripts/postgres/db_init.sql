-- in the 'public' schema
-- initializes tables in postgres
--
DROP TABLE IF EXISTS public.blog_post;
DROP TABLE IF EXISTS public.user;
--
-- holds blog data
--- date_modified auto-updates when the row is changed
CREATE TABLE public.blog_post (
	id SERIAL NOT NULL,
	CONSTRAINT blog_post_pk PRIMARY KEY (id),
	date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	date_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	title varchar NULL,
	author_id int NOT NULL,
	-- CONSTRAINT blog_post_author_fk FOREIGN KEY (author_id) REFERENCES public.user (id),
	markdown varchar NULL,
	private bool NOT NULL,
	malone bool NULL
);
ALTER SEQUENCE accounts_user_id_seq RESTART WITH 1;

-- holds user data
--- date_modified auto-updates when the row is changed
CREATE TABLE public.user (
	id SERIAL NOT NULL,
	CONSTRAINT user_pk PRIMARY KEY (id),
	date_created TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	date_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	username varchar NOT NULL UNIQUE,
	realname varchar NOT NULL,
	description varchar NULL,
	email varchar NULL,
	private bool NOT NULL
);

-- blog_post.author_id is a foreign key of user.id
ALTER TABLE public.blog_post
	ADD CONSTRAINT blog_post_author_fk FOREIGN KEY (author_id) REFERENCES public.user (id);

-- auto-update date_dreated column of blog_post and user tables, on row modification
-- https://x-team.com/blog/automatic-timestamps-with-postgresql/
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
	NEW.date_modified = NOW();
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;
--
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.user
FOR EACH row
EXECUTE PROCEDURE trigger_set_timestamp();
--
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON public.blog_post
FOR EACH row
EXECUTE PROCEDURE trigger_set_timestamp();

-- pre-fill data into user table
INSERT INTO public.user (username, realname, description, email, private)
	VALUES ('InACanoe', 'Jacob C', 'cool guy', 'nope', FALSE);
INSERT INTO public.user (username, realname, description, email, private)
	VALUES ('test_user', 'tTest User', 'another cool guy', 'nope', FALSE);