-- Run once in the Supabase SQL editor. Visitors can only ADD rows; nobody but the project owner can read them
-- (read them in the dashboard: Table editor -> suggestions).
create table if not exists suggestions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  idea int check (idea between 1 and 100),
  message text not null check (char_length(message) between 10 and 1500),
  contact text check (char_length(contact) <= 200),
  lang text check (lang in ('sr', 'en'))
);
alter table suggestions enable row level security;
create policy "anyone can add a suggestion" on suggestions for insert to anon with check (true);
grant insert on suggestions to anon;
