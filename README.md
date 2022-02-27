# longneaux-bot
Tweepy bot to respond to my friend tweets with random funny pictures.

If you want to use it you have to replace the os.environ.get('VARIABLE') with your twitter authentication keys and target account or place those in a .env file.

UPDATE 27-02-2022: There is now a longneaux_analysis.py file that allowed me to get the following informations:
- The number of occurences for each word used by my friend
- The average time between 2 of his tweets
- The average number of words in his tweets
- Get charts of those informations
- Keep a trace of those in some csv files

The code is absolutely not optimized but i'm planning to do it later

If you're passing by because you have problem with twitter authentication while trying to use tweepy, be sure that you activated the OAuth 1.0 and OAuth 2.0 on the twitter developper portal, I had trouble with it before finding the source of the problem.
