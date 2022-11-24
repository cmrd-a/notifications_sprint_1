CREATE TYPE status AS ENUM ('created', 'processed', 'error');
CREATE TYPE category AS ENUM ('service', 'content_updates', 'recommendations');
CREATE TYPE notification_channel AS ENUM ('email', 'push', 'sms');

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;

CREATE TABLE IF NOT EXISTS public.notifications (
    task_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    users_ids INTEGER[]  NOT NULL,
    template_name VARCHAR,
    variables json,
    status status NOT NULL,
    channel notification_channel NOT NULL,
    category category NOT NULL,
    send_time timestamp with time zone NOT NULL,

    PRIMARY KEY(task_id)
);
