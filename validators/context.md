# Artist Remix Studio — Project Context

## Overview
A music/audio web application with AI-powered features: stem separation, AI song generation, lyrics assistance, and audio-reactive video generation. Has a subscription/payments model via Stripe.

---

## Architecture

### Frontend — Next.js (Static Export)
- **Root**: `/Users/ervindavid/Workspace/vocal_remix_studio/` (project root *is* the Next.js app)
- **Next.js version**: `16.2.6` (non-standard — read `node_modules/next/dist/docs/` before writing Next.js code)
- **React version**: `19.2.4`
- **Output mode**: `output: "export"` (static HTML in `out/`) — no SSR/API routes
- **Build**: `bun run build` → outputs to `out/`
- **Package manager**: `bun` (uses `bun.lock`)
- **TypeScript** errors are ignored at build time (`ignoreBuildErrors: true`)
- **Images**: `unoptimized: true`
- **Deploy dist**: `out/` directory

### Backend — FastAPI (Python)
- **Root**: `backend/`
- **Entry**: `backend/app/main.py` → `app.main:app`
- **Runner**: `uvicorn`
- **Package manager**: `uv` (uses `uv.lock`, `pyproject.toml`)
- **Python**: `>=3.11`
- **CORS**: allows `localhost:3000`, `localhost:3001`, `127.0.0.1:3000`
- **API prefix**: `/api/v1`

---

## Key Dependencies

### Frontend
- `tailwindcss ^4` + `@tailwindcss/postcss ^4`
- `framer-motion` — animations
- `zustand ^5` — global state management
- `lucide-react ^1.16` — icons
- `@radix-ui/react-slot` — Radix UI primitives
- `class-variance-authority` + `clsx` + `tailwind-merge` — styling utilities (shadcn/ui pattern)
- `axios` — HTTP client
- `@stripe/stripe-js` + `stripe` — payments

### Backend
- `fastapi` + `uvicorn` — web framework
- `pydantic-settings` — config via env vars
- `replicate` — AI model inference (Demucs stem sep, MusicGen, Llama 2, Stable Diffusion video)
- `stripe` — subscription billing
- `sqlalchemy` + `psycopg2-binary` — ORM + Postgres
- `python-multipart` — file upload support

---

## Backend Structure
```
backend/
  app/
    main.py          # FastAPI app setup, CORS, router mounting
    core/
      config.py      # pydantic-settings Settings class (env-based config)
    api/
      endpoints.py   # Root router; mounts audio + subscriptions sub-routers
      audio.py       # /audio/* endpoints: process-audio, generate-video, generate-song, assist-lyrics
      subscriptions.py # /subscriptions/* endpoints: create-checkout-session, webhook
    models/
      user.py        # (empty — not yet implemented)
    services/
      replicate.py   # Replicate API wrappers (separate_stems, generate_video, generate_song_from_text, assist_lyrics)
      stripe.py      # (empty)
```

---

## Configuration / Secrets
- Backend config via `pydantic-settings` reading `.env`:
  - `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET`
  - `REPLICATE_API_TOKEN`
  - `DATABASE_URL` (defaults to SQLite: `sqlite:///./vocal_remix.db`)
- Workshop connectors available:
  - Neon Postgres (prefix `DBC5E2657D_`) — `DBC5E2657D_DATABASE_URL`, `DBC5E2657D_DIRECT_URL`
  - OpenAI (prefix `OPENAI_`) — `OPENAI_WORKSHOP_API_KEY`, `OPENAI_WORKSHOP_BASE_URL`

---

## Frontend Pages (routes)
- `/` — Home/landing
- `/dashboard` — User dashboard
- `/pricing` — Pricing page (connects to Stripe checkout)

---

## Important Conventions
- **All services mock gracefully** when API tokens are missing — Replicate calls return mock URLs, Stripe returns mock checkout URL
- **No app source files checked in** — the frontend source (`.tsx`/`.ts` files, `app/` dir) appears to have been built and only the `out/` static build is committed; source may exist locally but is not visible in the directory tree. Before adding new frontend pages, check if source files exist somewhere.
- **Babel-related artifacts at root** (`index.d.ts`, `index.js`, `traverse/`, `builders/`, etc.) are from a Babel package that ended up at project root — not application code.
- The `validators/` directory at root is similarly a stray package artifact.
- **Deploy config** in `.workshop/deploy.json`: backend = `uvicorn app.main:app` from `backend/`, frontend = static export from `out/`

---

## Development Notes
- Frontend dev: `bun run dev` (from project root, port 3000)
- Backend dev: `cd backend && uv run uvicorn app.main:app --reload`
- Before adding Python deps: `uv add <package>` inside `backend/`
- The `user.py` model and `stripe.py` service are empty stubs — database models not yet implemented
- Replicate models used: Demucs (audio stem separation), MusicGen (song gen), Llama 2 70B (lyrics), Stable Diffusion video
