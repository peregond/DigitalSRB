# Digitalna Srbija · Digital Serbia

61 ideas against bureaucracy and corruption, for citizens and foreigners. A one-page static site in Serbian and English with a language switch and a + / − vote under every idea.

## Publishing on GitHub Pages

Repository **Settings → Pages → Build and deployment → Deploy from a branch**, pick the branch and `/ (root)`. No build step runs on GitHub: `index.html` is already built and committed.

Design and content rules (screen proportions, AI labels, bilingual pages): see [docs/GUIDELINES.md](docs/GUIDELINES.md).

## Editing

| What | Where |
| --- | --- |
| Idea texts, visuals, sources (both languages) | `source/print.html` (the A4 print document) |
| Hero, navigation, page shell | `tools/template.html` |
| Topics (which idea belongs to which category) | `tools/categories.py` |
| Tier names and UI labels | top of `tools/build.py` |
| Detail pages of the 8 main ideas (texts, infographics) | `tools/pages_data.py`, layout in `tools/build_pages.py` and `tools/page_template.html`, look in `assets/page.css` |
| Colours of each detail page | `THEMES` in `tools/pages_data.py` |
| Card illustrations | `tools/gen_featured_art.py` (writes `assets/featured/*.svg`) |
| Look | `assets/styles.css` |
| Behaviour (language, filter, votes) | `assets/app.js` |

After changing the first three, rebuild:

```bash
python3 tools/build.py
```

It needs Python 3 with `beautifulsoup4`.

## Votes

Out of the box each visitor's + / − is stored only in their own browser (`localStorage`), so nobody sees totals. GitHub Pages has no server, so shared totals need an external database. The site supports a free [Supabase](https://supabase.com) project:

1. Create a project and run this in its SQL editor:

```sql
create table idea_votes (
  idea int primary key check (idea between 1 and 100),
  up int not null default 0,
  down int not null default 0
);
alter table idea_votes enable row level security;
create policy "read totals" on idea_votes for select using (true);

create function cast_vote(p_idea int, p_up int, p_down int)
returns idea_votes language sql security definer set search_path = public as $$
  insert into idea_votes (idea, up, down)
  values (p_idea, greatest(least(p_up, 1), 0), greatest(least(p_down, 1), 0))
  on conflict (idea) do update set
    up = greatest(idea_votes.up + greatest(least(p_up, 1), -1), 0),
    down = greatest(idea_votes.down + greatest(least(p_down, 1), -1), 0)
  returning *;
$$;
grant execute on function cast_vote to anon;
```

2. Put the project URL and the public `anon` key into `assets/config.js`.

The counts then appear next to + and −. This is an honest-visitor counter, not a secure poll: one person can vote again from another browser.

## Comments, profiles and the admin page

Under every idea on the home page there is a **Comments** button. A visitor writes a comment; the first time they pick a name and one of four random abstract pictures, or press the button for a random one (no email, no password; there are 50 pictures in all). The server returns a secret **recovery code** that is shown once. The browser remembers the profile, and the code restores it in any other browser. Each comment has plus and minus buttons: they need a profile, each profile has one vote per comment (pressing again takes it back) and nobody can vote on their own comment. The avatar in the top bar opens a menu: all of the visitor’s own comments, replies to them (from other visitors or from the team), name and picture, the recovery code and sign out.

1. Run `docs/supabase-comments.sql` once in the Supabase SQL editor. It creates the tables (locked: the site can only use the functions in that file), rate limits and the admin functions. Running the file again is safe and upgrades an earlier version without losing data; do that whenever the file changes.
2. Choose an admin key: a long random secret (24+ characters). Run the commented `insert into app_settings ...` statement at the end of the SQL file with your secret in place. Only its hash is stored.
3. Open `/admin/` on the site and type the key. It stays in that browser tab only. The globe menu switches the page between Serbian (Latin or Cyrillic), English and Russian (the default); the choice is remembered separately from the public site. There you see statistics (profiles, comments per day and per idea, votes next to comments, ideas nobody has commented on), all comments (hide / show, official replies marked "Tim") and the suggestions from the form.

Until the SQL is run the Comments buttons show "not available right now". The admin page is `noindex` and excluded in `robots.txt`; the real protection is the key.

## Suggestions form

The "Predloži ideju / Suggest an idea" form on the home page stores messages in your Supabase project. Run `docs/supabase-suggestions.sql` once in the SQL editor. Visitors can only add rows; you read the messages in the dashboard (Table editor, `suggestions`). Until the table exists the form shows a "try again later" message.

## Other settings

- **Link previews / SEO:** `python3 tools/og.py` renders `assets/og/*.jpg`; `tools/build.py` writes `sitemap.xml`, `robots.txt` and `404.html` (the site address comes from `CNAME`).
- **Language:** chosen automatically from the browser language (Serbian-family languages give Serbian, everything else English; the menu choice is remembered and wins). **Language menu:** one globe button with Srpski (latinica), Српски (ћирилица) and English. Cyrillic is made by `assets/translit.js`, which converts the Serbian text in the browser; names that must stay Latin are listed in `KEEP`.
- **Showcase images:** `python3 tools/shots.py`. **Review of the drafted text:** `docs/REVIEW.md`.
