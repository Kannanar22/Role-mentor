# NovaTech Role Mentor AI

A chat-based project mentor for students in the **CAT-II Problem-Driven
Industry AI Engineer Program**. Built with Streamlit and the Google Gemini
API. Students pick their current phase and role, then ask what to do next —
the mentor replies with objectives, tasks, tools, deliverables, and a
submission checklist.

The app uses **one shared API key** (the instructor's), stored securely as a
Streamlit secret. Students never see or enter a key.

## Files

```
novatech/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── .gitignore                      # Keeps secrets.toml out of git
└── .streamlit/
    └── secrets.toml.example        # Template — copy to secrets.toml locally
```

## 1. Local setup

**Requirements:** Python 3.9+

```bash
# 1. Clone or download this folder, then cd into it
cd novatech

# 2. (Recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Gemini API key
#    Copy the example file and fill in your real key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
#    Then edit .streamlit/secrets.toml:
#    GEMINI_API_KEY = "AIza-your-real-key-here"

# 5. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

> ⚠️ **Never commit `.streamlit/secrets.toml`** — it holds your real key.
> The included `.gitignore` already excludes it.

## 2. Deploy to Streamlit Community Cloud

1. **Push to GitHub** — include `app.py`, `requirements.txt`, and
   `.gitignore`. Do *not* push `secrets.toml`.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with
   GitHub, click **New app**, and select your repo, branch, and `app.py` as
   the main file.
3. In the app's dashboard, open **Settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "AIza-your-real-key-here"
   ```
   This is stored securely by Streamlit and injected at runtime — it never
   appears in the repo or the deployed UI.
4. Click **Deploy**. Once it builds, open the public URL and confirm the
   sidebar shows "Mentor AI is ready to use."
5. Share the URL with students. That's the only thing they need — no key,
   no setup.

## 3. How the app works

- **Phase & Role selectors** (sidebar) — sets session context so the mentor
  tailors answers to the student's assignment.
- **Quick-prompt buttons** — one-click common questions ("What should I do
  today?", "What are my deliverables?", "Who do I coordinate with?").
- **Chat** — free-text questions get answered using a structured mentor
  system prompt (objective, tasks, tools, deliverables, checklist, common
  mistakes).
- **Clear Conversation** — resets the chat history for the current session
  only (each student's session is separate; nothing is shared or persisted
  across users).

## 4. Notes on the shared key

Every student's request draws from the same Gemini quota and billing.

- Watch usage in [Google AI Studio](https://aistudio.google.com) if you
  expect many concurrent students.
- If you hit free-tier rate limits, consider upgrading to a paid Gemini
  tier for the duration of the program.
- If you ever need to rotate the key (e.g. it leaks), just update the
  `GEMINI_API_KEY` value in Streamlit Cloud's Secrets panel — no code
  change or redeploy needed.

## 5. Troubleshooting

| Symptom | Likely cause |
|---|---|
| Sidebar shows "Mentor AI isn't configured yet" | `GEMINI_API_KEY` missing from secrets (local or Cloud) |
| `ModuleNotFoundError: google` | Run `pip install -r requirements.txt` |
| "API error: ..." in chat | Check the key is valid and has quota remaining in Google AI Studio |
