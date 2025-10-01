# Ai_Agent_Telegram_Bot
📅 Telegram Bot + Google Calendar Integration
🔎 Overview

This project is a Telegram bot that lets users manage their Google Calendar directly through chat — in Uzbek or Russian.
The bot provides a mini-app (WebApp) for one-time Google login, then continues to work entirely inside Telegram. Users can add events like meetings, classes, or reminders by simply typing natural sentences.

⚙️ How It Works

User starts the bot → Gets a button “Sign in with Google”.

Mini-app (WebApp) opens → User logs into their Google account.

OAuth2 flow completes → Bot saves the user’s access_token + refresh_token in the database.

User chats in Uzbek or Russian → Example:

“Ertaga soat 3 da dars bor”

“Добавь встречу завтра в 14:00”

Bot parses the message → Detects date/time/summary.

Bot calls Google Calendar API → Adds the event instantly.

Confirmation reply → User gets a success message in the same language.

🛠️ Tech Stack

Telegram Bot API (aiogram) → Handles messages & commands

FastAPI → OAuth2 backend for Google login

Google Calendar API (google-api-python-client) → Creates events

SQLite DB → Stores user credentials (tokens)

OAuth 2.0 → Secure Google authentication via mini-app

🔄 Flow Diagram
[Telegram User] 
     ↓
 [Telegram Bot] -- (Sign in button) --> [WebApp + FastAPI]
     ↓                                         ↓
   Messages -------------------------------> Google OAuth
     ↓                                         ↓
 [Bot Backend] <----(tokens stored in DB)----> [Google API]
     ↓
 Google Calendar Event Created ✅

✨ Features

Supports multiple users (tokens stored per Telegram ID).

Works in Uzbek and Russian with rule-based parsing.

Mini-app only used for sign-in; all other interactions happen in chat.

Automatic event creation in Google Calendar.

Easily extendable (add event editing, reminders, or even Keep/Tasks later).