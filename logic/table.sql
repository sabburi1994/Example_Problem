CREATE TABLE public."inputBot_unfollowlog"
(
    id integer NOT NULL DEFAULT nextval('"inputBot_unfollowlog_id_seq"'::regclass),
    following_name text COLLATE pg_catalog."default",
    unfollowed boolean NOT NULL,
    unfollowed_time timestamp with time zone,
    follow_time timestamp with time zone,
    insta_data_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "inputBot_unfollowlog_pkey" PRIMARY KEY (id),
    CONSTRAINT "inputB_insta_data_id_af6a234e_fk_dashboard_instadata_insta_name" FOREIGN KEY (insta_data_id)
        REFERENCES public.dashboard_instadata (insta_name) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        DEFERRABLE INITIALLY DEFERRED
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."inputBot_unfollowlog"
    OWNER to "instabroUser";

-- Index: inputBot_unfollowlog_4736104c

-- DROP INDEX public."inputBot_unfollowlog_4736104c";

CREATE INDEX "inputBot_unfollowlog_4736104c"
    ON public."inputBot_unfollowlog" USING btree
    (insta_data_id COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Index: inputBot_unfollowlog_insta_data_id_af6a234e_like

-- DROP INDEX public."inputBot_unfollowlog_insta_data_id_af6a234e_like";

CREATE INDEX "inputBot_unfollowlog_insta_data_id_af6a234e_like"
    ON public."inputBot_unfollowlog" USING btree
    (insta_data_id COLLATE pg_catalog."default" varchar_pattern_ops)
    TABLESPACE pg_default;
