-- Comments, anonymous profiles and the admin tools. Run ONCE in the Supabase SQL editor (after the votes SQL in README.md).
-- Running it again is safe: it also upgrades an earlier version of this file and keeps the data.
--
-- How it works
--  * A visitor picks a name and one of 50 abstract avatars. The server creates a profile and returns a secret
--    recovery code (shown once). The browser remembers it; with the code the profile can be restored in any browser.
--    Only a hash of the code is stored.
--  * All tables are locked (row level security, no policies). The site talks to them only through the functions below.
--  * Comments are public right away. Staff can hide any comment and reply officially from /admin/.
--  * Admin access is a long secret that only you know. Its hash is kept in app_settings (see the last block).

create extension if not exists pgcrypto with schema extensions;

create table if not exists profiles (
  id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 2 and 30),
  avatar int not null check (avatar between 0 and 49),
  code_hash text not null unique,
  created_at timestamptz not null default now(),
  last_seen timestamptz not null default now()
);

create table if not exists comments (
  id bigint generated always as identity primary key,
  idea int not null check (idea between 1 and 100),
  parent_id bigint references comments (id) on delete cascade,
  profile_id uuid references profiles (id) on delete set null,
  is_staff boolean not null default false,
  body text not null check (char_length(body) between 1 and 1000),
  hidden boolean not null default false,
  created_at timestamptz not null default now()
);
-- reply_to: the exact comment a team reply answers (threads are one level deep, so parent_id is always the top one)
alter table comments add column if not exists reply_to bigint references comments (id) on delete set null;
-- deleted: removed by its author; the row stays (rate limits count it) and nobody can show it again
alter table comments add column if not exists deleted boolean not null default false;
create index if not exists comments_idea_idx on comments (idea, created_at);
create index if not exists comments_parent_idx on comments (parent_id);
create index if not exists comments_profile_idx on comments (profile_id);

create table if not exists app_settings (key text primary key, value text not null);

-- one vote of a profile on a comment: 1 (plus) or -1 (minus); taking a vote back removes the row
create table if not exists comment_votes (
  comment_id bigint not null references comments (id) on delete cascade,
  profile_id uuid not null references profiles (id) on delete cascade,
  value smallint not null check (value in (-1, 1)),
  primary key (comment_id, profile_id)
);

alter table comment_votes enable row level security;
revoke all on table comment_votes from anon, authenticated;
alter table profiles enable row level security;
alter table comments enable row level security;
alter table app_settings enable row level security;
-- no policies on purpose: the anon key cannot read or write these tables directly
revoke all on table profiles, comments, app_settings from anon, authenticated;

-- ---------------------------------------------------------------- helpers
create or replace function _hash(p_code text) returns text
language sql immutable set search_path = public, extensions as $$
  select encode(digest(upper(regexp_replace(coalesce(p_code, ''), '[^0-9A-Za-z]', '', 'g')), 'sha256'), 'hex');
$$;

create or replace function _profile(p_code text) returns profiles
language sql stable security definer set search_path = public, extensions as $$
  select * from profiles where code_hash = _hash(p_code);
$$;

create or replace function _is_admin(p_key text) returns boolean
language sql stable security definer set search_path = public, extensions as $$
  select exists (
    select 1 from app_settings
    where key = 'admin_key_hash' and value = encode(digest(coalesce(p_key, ''), 'sha256'), 'hex')
  );
$$;

-- ---------------------------------------------------------------- profiles
create or replace function register_profile(p_name text, p_avatar int)
returns table (id uuid, code text, name text, avatar int)
language plpgsql security definer set search_path = public, extensions as $$
declare
  v_code text; v_row profiles; v_name text := btrim(regexp_replace(coalesce(p_name, ''), '\s+', ' ', 'g'));
begin
  if char_length(v_name) < 2 or char_length(v_name) > 30 then raise exception 'bad_name'; end if;
  if p_avatar is null or p_avatar < 0 or p_avatar > 49 then raise exception 'bad_avatar'; end if;
  perform pg_advisory_xact_lock(hashtext('dsrb.register'));
  if (select count(*) from profiles where created_at > now() - interval '1 minute') > 30 then raise exception 'busy'; end if;
  v_code := upper(encode(gen_random_bytes(8), 'hex'));
  insert into profiles (name, avatar, code_hash) values (v_name, p_avatar, _hash(v_code)) returning * into v_row;
  return query select v_row.id, substr(v_code, 1, 4) || '-' || substr(v_code, 5, 4) || '-' || substr(v_code, 9, 4) || '-' || substr(v_code, 13, 4),
                      v_row.name, v_row.avatar;
end $$;

create or replace function restore_profile(p_code text)
returns table (id uuid, name text, avatar int)
language plpgsql security definer set search_path = public, extensions as $$
declare v_row profiles;
begin
  v_row := _profile(p_code);
  if v_row.id is null then raise exception 'unknown_code'; end if;
  update profiles set last_seen = now() where profiles.id = v_row.id;
  return query select v_row.id, v_row.name, v_row.avatar;
end $$;

create or replace function update_profile(p_code text, p_name text, p_avatar int)
returns table (id uuid, name text, avatar int)
language plpgsql security definer set search_path = public, extensions as $$
declare v_row profiles; v_name text := btrim(regexp_replace(coalesce(p_name, ''), '\s+', ' ', 'g'));
begin
  v_row := _profile(p_code);
  if v_row.id is null then raise exception 'unknown_code'; end if;
  if char_length(v_name) < 2 or char_length(v_name) > 30 then raise exception 'bad_name'; end if;
  if p_avatar is null or p_avatar < 0 or p_avatar > 49 then raise exception 'bad_avatar'; end if;
  update profiles set name = v_name, avatar = p_avatar, last_seen = now() where profiles.id = v_row.id;
  return query select v_row.id, v_name, p_avatar;
end $$;

-- ---------------------------------------------------------------- reading (public)
create or replace function get_comment_counts()
returns table (idea int, n bigint)
language sql stable security definer set search_path = public as $$
  select c.idea, count(*) from comments c left join comments t on t.id = c.parent_id
  where not c.hidden and t.hidden is not true group by c.idea;
$$;

create or replace function get_comments(p_idea int)
returns table (id bigint, parent_id bigint, body text, created_at timestamptz, is_staff boolean,
               name text, avatar int, profile_id uuid)
language sql stable security definer set search_path = public as $$
  select c.id, c.parent_id, c.body, c.created_at, c.is_staff, p.name, p.avatar, c.profile_id
  from comments c left join profiles p on p.id = c.profile_id
  -- the 300 newest threads, each with its replies
  where c.idea = p_idea and not c.hidden and coalesce(c.parent_id, c.id) in (
    select t.id from comments t where t.idea = p_idea and t.parent_id is null and not t.hidden
    order by t.created_at desc, t.id desc limit 300)
  order by c.created_at asc, c.id asc;
$$;

-- ---------------------------------------------------------------- writing (with the profile code)
create or replace function post_comment(p_code text, p_idea int, p_body text, p_parent bigint default null)
returns table (id bigint, parent_id bigint, body text, created_at timestamptz, is_staff boolean,
               name text, avatar int, profile_id uuid)
language plpgsql security definer set search_path = public, extensions as $$
declare
  v_profile profiles; v_body text := btrim(coalesce(p_body, ''), E' \t\r\n'); v_parent comments; v_new comments;
begin
  v_profile := _profile(p_code);
  if v_profile.id is null then raise exception 'unknown_code'; end if;
  if p_idea is null or p_idea < 1 or p_idea > 100 then raise exception 'bad_idea'; end if;
  if char_length(v_body) < 1 or char_length(v_body) > 1000 then raise exception 'bad_body'; end if;
  -- one post at a time per profile, so that parallel requests cannot pass the limits together
  perform 1 from profiles pr where pr.id = v_profile.id for update;
  if exists (select 1 from comments c where c.profile_id = v_profile.id and c.created_at > clock_timestamp() - interval '15 seconds') then
    raise exception 'slow_down';
  end if;
  if (select count(*) from comments c where c.profile_id = v_profile.id and c.created_at > now() - interval '1 day') >= 40 then
    raise exception 'daily_limit';
  end if;
  if p_parent is not null then
    select * into v_parent from comments c where c.id = p_parent and not c.hidden;
    if v_parent.id is null or v_parent.idea <> p_idea or v_parent.parent_id is not null then raise exception 'bad_parent'; end if;
  end if;
  insert into comments (idea, parent_id, profile_id, body, created_at)
    values (p_idea, p_parent, v_profile.id, v_body, clock_timestamp()) returning * into v_new;
  update profiles set last_seen = now() where profiles.id = v_profile.id;
  return query select v_new.id, v_new.parent_id, v_new.body, v_new.created_at, v_new.is_staff, v_profile.name, v_profile.avatar, v_profile.id;
end $$;

create or replace function delete_my_comment(p_code text, p_id bigint)
returns boolean
language plpgsql security definer set search_path = public, extensions as $$
declare v_profile profiles;
begin
  v_profile := _profile(p_code);
  if v_profile.id is null then raise exception 'unknown_code'; end if;
  update comments c set hidden = true, deleted = true where c.id = p_id and c.profile_id = v_profile.id;
  return found;
end $$;

-- replies (from other visitors or from staff) to the visitor's own comments
create or replace function get_my_replies(p_code text)
returns table (id bigint, idea int, body text, created_at timestamptz, is_staff boolean,
               name text, avatar int, parent_body text)
language plpgsql stable security definer set search_path = public, extensions as $$
declare v_profile profiles;
begin
  v_profile := _profile(p_code);
  if v_profile.id is null then raise exception 'unknown_code'; end if;
  return query
    select r.id, r.idea, r.body, r.created_at, r.is_staff, p.name, p.avatar, m.body
    from comments r
    join comments t on t.id = r.parent_id and not t.hidden
    -- my comment that this reply is about: the one the team answered, otherwise the top of the thread
    join lateral (
      select c.body from comments c
      where c.id in (r.reply_to, r.parent_id) and c.profile_id = v_profile.id and not c.hidden
      order by c.id desc limit 1
    ) m on true
    left join profiles p on p.id = r.profile_id
    where not r.hidden and r.profile_id is distinct from v_profile.id
    order by r.created_at desc, r.id desc
    limit 50;
end $$;

-- the visitor's own comments, newest first (without deleted ones and ones that are hidden from everybody)
create or replace function get_my_comments(p_code text)
returns table (id bigint, idea int, parent_id bigint, body text, created_at timestamptz)
language plpgsql stable security definer set search_path = public, extensions as $$
declare v_profile profiles;
begin
  v_profile := _profile(p_code);
  if v_profile.id is null then raise exception 'unknown_code'; end if;
  return query
    select c.id, c.idea, c.parent_id, c.body, c.created_at
    from comments c left join comments t on t.id = c.parent_id
    where c.profile_id = v_profile.id and not c.hidden and t.hidden is not true
    order by c.created_at desc, c.id desc
    limit 500;
end $$;

-- ---------------------------------------------------------------- votes on comments (a profile is needed)
-- totals for the comments of one idea; "mine" is the vote of the profile with this code (0 without one)
create or replace function get_comment_votes(p_idea int, p_code text default null)
returns table (id bigint, up bigint, down bigint, mine int)
language sql stable security definer set search_path = public, extensions as $$
  select v.comment_id, count(*) filter (where v.value = 1), count(*) filter (where v.value = -1),
         coalesce(max(v.value) filter (where v.profile_id = (select p.id from profiles p where p.code_hash = _hash(p_code))), 0)::int
  from comment_votes v
  join comments c on c.id = v.comment_id
  left join comments t on t.id = c.parent_id
  where c.idea = p_idea and not c.hidden and t.hidden is not true
  group by v.comment_id;
$$;

-- p_value: 1 plus, -1 minus, 0 takes the vote back. Sending the same value again changes nothing.
create or replace function vote_comment(p_code text, p_id bigint, p_value int)
returns table (up bigint, down bigint, mine int)
language plpgsql security definer set search_path = public, extensions as $$
declare v_profile profiles; v_comment comments;
begin
  v_profile := _profile(p_code);
  if v_profile.id is null then raise exception 'unknown_code'; end if;
  if p_value is null or p_value not in (-1, 0, 1) then raise exception 'bad_vote'; end if;
  select c.* into v_comment from comments c left join comments t on t.id = c.parent_id
    where c.id = p_id and not c.hidden and t.hidden is not true;
  if v_comment.id is null then raise exception 'not_found'; end if;
  if v_comment.profile_id = v_profile.id then raise exception 'own_comment'; end if;
  if p_value = 0 then
    delete from comment_votes v where v.comment_id = p_id and v.profile_id = v_profile.id;
  else
    insert into comment_votes as v (comment_id, profile_id, value) values (p_id, v_profile.id, p_value)
      on conflict (comment_id, profile_id) do update set value = excluded.value;
  end if;
  update profiles set last_seen = now() where profiles.id = v_profile.id;
  return query select count(*) filter (where v.value = 1), count(*) filter (where v.value = -1), p_value
    from comment_votes v where v.comment_id = p_id;
end $$;

-- ---------------------------------------------------------------- admin (needs the admin key)
drop function if exists admin_comments(text, int);
create or replace function admin_comments(p_key text, p_limit int default 300)
returns table (id bigint, idea int, parent_id bigint, body text, created_at timestamptz, hidden boolean,
               is_staff boolean, profile_id uuid, name text, avatar int, deleted boolean)
language plpgsql stable security definer set search_path = public, extensions as $$
begin
  if not _is_admin(p_key) then raise exception 'forbidden'; end if;
  return query
    select c.id, c.idea, c.parent_id, c.body, c.created_at, c.hidden, c.is_staff, c.profile_id, p.name, p.avatar, c.deleted
    from comments c left join profiles p on p.id = c.profile_id
    order by c.created_at desc limit least(greatest(p_limit, 1), 2000);
end $$;

create or replace function admin_set_hidden(p_key text, p_id bigint, p_hidden boolean)
returns boolean
language plpgsql security definer set search_path = public, extensions as $$
begin
  if not _is_admin(p_key) then raise exception 'forbidden'; end if;
  update comments c set hidden = p_hidden where c.id = p_id and (p_hidden or not c.deleted);
  return found;
end $$;

create or replace function admin_reply(p_key text, p_parent bigint, p_body text)
returns bigint
language plpgsql security definer set search_path = public, extensions as $$
declare v_parent comments; v_id bigint; v_body text := btrim(coalesce(p_body, ''), E' \t\r\n');
begin
  if not _is_admin(p_key) then raise exception 'forbidden'; end if;
  select * into v_parent from comments c where c.id = p_parent;
  if v_parent.id is null then raise exception 'bad_parent'; end if;
  if char_length(v_body) < 1 or char_length(v_body) > 1000 then raise exception 'bad_body'; end if;
  insert into comments (idea, parent_id, reply_to, profile_id, is_staff, body)
    values (v_parent.idea, coalesce(v_parent.parent_id, v_parent.id), v_parent.id, null, true, v_body) returning id into v_id;
  return v_id;
end $$;

create or replace function admin_stats(p_key text)
returns jsonb
language plpgsql stable security definer set search_path = public, extensions as $$
declare v jsonb; v_sugg bigint := 0;
begin
  if not _is_admin(p_key) then raise exception 'forbidden'; end if;
  -- the suggestions table comes from docs/supabase-suggestions.sql; the overview works without it
  if to_regclass('public.suggestions') is not null then select count(*) into v_sugg from suggestions; end if;
  select jsonb_build_object(
    'profiles_total', (select count(*) from profiles),
    'profiles_7d', (select count(*) from profiles where created_at > now() - interval '7 days'),
    'active_7d', (select count(*) from profiles where last_seen > now() - interval '7 days'),
    'comments_total', (select count(*) from comments where not is_staff),
    'comments_7d', (select count(*) from comments where not is_staff and created_at > now() - interval '7 days'),
    'hidden', (select count(*) from comments where hidden),
    'staff_replies', (select count(*) from comments where is_staff),
    'by_idea', coalesce((select jsonb_agg(jsonb_build_object('idea', x.idea, 'comments', x.n, 'authors', x.a) order by x.idea)
                         from (select c.idea, count(*) n, count(distinct c.profile_id) a
                               from comments c left join comments t on t.id = c.parent_id
                               where not c.is_staff and not c.hidden and t.hidden is not true group by c.idea) x), '[]'::jsonb),
    'by_day', coalesce((select jsonb_agg(jsonb_build_object('day', d.day, 'n', d.n) order by d.day)
                        from (select (created_at at time zone 'UTC')::date as day, count(*) n from comments
                              where not is_staff and created_at > now() - interval '30 days' group by 1) d), '[]'::jsonb),
    'votes', coalesce((select jsonb_agg(jsonb_build_object('idea', idea, 'up', up, 'down', down) order by idea) from idea_votes), '[]'::jsonb),
    'suggestions', v_sugg
  ) into v;
  return v;
end $$;

create or replace function admin_suggestions(p_key text, p_limit int default 200)
returns table (id bigint, created_at timestamptz, idea int, message text, contact text, lang text)
language plpgsql stable security definer set search_path = public, extensions as $$
begin
  if not _is_admin(p_key) then raise exception 'forbidden'; end if;
  if to_regclass('public.suggestions') is null then return; end if;
  return query select s.id, s.created_at, s.idea, s.message, s.contact, s.lang from suggestions s
    order by s.created_at desc limit least(greatest(p_limit, 1), 1000);
end $$;

-- the helpers must not be callable from the site; the public functions are
revoke all on function _hash(text), _profile(text), _is_admin(text) from public, anon, authenticated;
grant execute on function register_profile(text, int), restore_profile(text), update_profile(text, text, int),
  get_comment_counts(), get_comments(int), post_comment(text, int, text, bigint), delete_my_comment(text, bigint),
  get_my_replies(text), get_my_comments(text), get_comment_votes(int, text), vote_comment(text, bigint, int),
  admin_comments(text, int), admin_set_hidden(text, bigint, boolean), admin_reply(text, bigint, text),
  admin_stats(text), admin_suggestions(text, int)
  to anon;

-- ---------------------------------------------------------------- admin key (do this yourself, once)
-- Invent a long random secret (at least 24 characters), put it below instead of PUT-A-LONG-SECRET-HERE and run only this
-- statement. Then open /admin/ on the site and type the same secret. Do not share it and do not commit it anywhere.
--
-- insert into app_settings (key, value) values ('admin_key_hash', encode(extensions.digest('PUT-A-LONG-SECRET-HERE', 'sha256'), 'hex'))
--   on conflict (key) do update set value = excluded.value;
