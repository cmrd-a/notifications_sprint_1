CREATE TYPE status AS ENUM ('created', 'processed', 'error');
CREATE TYPE category AS ENUM ('service', 'content_updates', 'recommendations');
CREATE TYPE notification_channel AS ENUM ('email', 'push', 'sms');

CREATE TABLE IF NOT EXISTS public.notifications (
    task_id TEXT ,
    users_ids INTEGER[],
    message TEXT,
    status status,
    channel notification_channel,
    category category,
    send_time timestamp with time zone,

    PRIMARY KEY(task_id)
);
