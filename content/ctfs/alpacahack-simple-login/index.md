+++
date = '2025-12-01T20:30:23+02:00'
draft = false
title = 'Alpacahack Simple Login'
+++
# Alpacahack Simple Logic
### category : web
### difficulty : beginners
### url to ctf :https://alpacahack.com/challenges/simple-login

We are provided with the source code `app.py`. The application takes a username and password, checks them against a database, and logs the user in if the credentials match.

## Reconnaissance

### Source Code Analysis

The core logic lies in the `/login` route. Here are the interesting parts of `app.py`:

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    # ... checks ...
    if "'" in username or "'" in password:
        return "Do not try SQL injection 🤗", 400

    # ... connection ...
    cursor.execute(
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )

```

we try to do a basic check for sqli
and get that annoying emoji message.. 
what do we do? we need to find a way to bypass the blacklist of "'"
we can use the Backslash Escaping technique. In MySQL, a backslash (\) escapes the character immediately following it.

If we send \ as the username, it escapes the developer's closing quote
which means we have the ' without even typing it.

we go and see that we succesfuly bypassed the login logic and got in as admins
however we still did not get no flag
we see inside the source code that the sql database , theres the flag is, we cant see it since its from a remote server but using the new vulnerability we just might be able to get it

we try enumerating the DB using the union method
UNION SELECT 1,2 # 
yea this one works

now we do UNION SELECT 1,* FROM flag#
we got it 
thank you for reading hope you enjoyed this ctf.
