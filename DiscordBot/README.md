# JSONWisdom DiscordBot v0.1

**Home:** `COMPUTERWISDOM/DiscordBot/`  
**Authority:** false  
**Mode:** explicit slash commands only

The bot answers `/ask` through the OpenAI Responses API. It does not post autonomously, merge pull requests, write to GitHub or Drive, promote facts, or claim authority.

## Required environment

Copy `.env.example` to an untracked `.env` and provide:

- `DISCORD_TOKEN`
- `DISCORD_APPLICATION_ID`
- `DISCORD_GUILD_ID`
- `OPENAI_API_KEY`
- optional `OPENAI_MODEL` (defaults to `gpt-5.6`)

## Run

```bash
npm install
npm test
npm start
```

The Discord application must be invited to the target server with the `applications.commands` and `bot` scopes. The bot needs no privileged gateway intents.

## Boundary

- Business / Jay Money → `COMPUTERWISDOM`
- Locality / state work → `AL`
- `JOY` and `COMPUTERWISDOM` are substrates
- `HEIDEE` remains the child JoySpace
- Responses end with `authority=false`

No secret belongs in git.
