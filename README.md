# Telegram spammer
## The software for spamming megagroups with your messages

**Requirements**
1.  Telethon v.1.9.0.
2. python-telegram-bot v.11.1.0.
3. PostgreSQL Database.
4. psycopg2 v.2.8.3.		



**Configuration**
 1. In file `manager_bot.py` change the token variable value to your Telegram Bot token, given by https://t.me/botfather.
 2.  Register your Telegram Application on https://core.telegram.org/api/obtaining_api_id.
 3. In file `sender_test.py` change variable **api_id** to api id given by Telegram, then change variable **api_hash** to   api hash, given by Telegram.
 4. In file `config_app.py` add owners ids in owner_list, in class **Config**: set default interval between launching a spamming script and default interval between sending messages into the megagroups. In class **DbConfig**: edit default database table configuration or leave as it is.
 5.  Set environment variable DATABASE_URL to your postgresql database url. Example(UNIX):
  ```export DATABASE_URL=postgresql://user:password@host/database_name```


**Launching**

The main application is `manager_bot.py`, so the launching looks like this:
```python manager_bot.py```
first usage of spam script(`sender_test.py`) requires authorization, so login with your spamming account where the megagrops to send messages in are stored. Then, it will use the authorization session file.

**Managing**

You can manage spamming through the keyboard your bot sends to you after */start* command. Available options: set spam session interval, start spamming, stop spamming, set spam message text.
 

