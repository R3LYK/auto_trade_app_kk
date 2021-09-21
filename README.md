**I tried my best to explain everything and add links where applicable. I also tried to format neatly. Hopefully it all copies over to discord well. I would be shocked if I didn't forget something though.**

**INSTRUCTIONS & REQUIREMENTS FOR GETTING UP-TO SPEED**

**Python & SQL versions**

I'm working in ```Python 3.9.4```, so far I haven't had any issues with it. Some packages are still catching up to the latest version so it could cause issues down the road. Cross that bridge then.
I'm working with ```SQL 12.x```, same thing as far as functionality.

**PULLING THE REPO**
Install ```GIT & GitHub desktop```. I recommend using GIT, command line is easier than learning new GUI's for me. But you may as well download so you can start learning.

Follow one of the GIT/GitHub links in #helpful-links
**NOTE:**The SSL part is tricky, I ended up having to google for quite a while. If you get stuck just @ me and i'll hop on if I can.

DO NOT clone the repo. If you clone the repo, I don't think it will allow you to push or merge. (again, i'm still learning GIT/GitHub. But it makes sense it wouldn't)

You need to ```CLONE``` from the repo. Make sure you choose the correct branch ``` "Postgres-light-change" ``` it whould should that it was updated today (9/16).
then follow the instructions in the link below.
https://github.blog/2019-01-07-create-pull-requests-in-vscode/							
						

**INSTALLING REQUIRED PACKAGES**

I suggest using ```vscode```. It allows screen sharring, but mostly it's what I know best. We will have to use ```Jupyter Notebook``` ```(JupyterLab)``` later but let's worry about one thing at a time for now.

In the terminal, make sure you're in the working directory. ```your/filepath/here/auto_trade_app_kk```

in the terminal run this command ```bash pip install -r requirements.txt```

I forgot to add a couple to the requirements so you need to run these in the terminal too
```pip install pandas``` 
```pip install psycopg2-binary``` 
```pip install uvicorn```

You should be good to go on requirements now!


**THIS WILL GET YOU UP AND RUNNING FOR THE DB**

This should give you access the the db. I don't have any financials attached to the account yet so we all have admin access. That needs to be one of the next things I figure out. It's ```TimescaleDB```.

ADD THE SCRIPT BELOW TO THE CONFIG. Right now there isn't a config in the repo. You will have to create a new file in VSCode after you pull. name it ```config.py```)

```python connection = ("postgres://tsdbadmin:kypej0e0psu4w90m@fwzbhedd6y.u59ev93pfx.tsdb.forge.timescale.com:34020/tsdb?sslmode=require")```

In the files that point towards a DB REPLACE ```python connection = ("blah, blah, blah")``` 

WITH THIS ```python connection = psycopg2.connect(config.connection)```

Just make sure you don't accidentally run drop_tables.py please, I've been populating the price_table for hours and it's still just now on AMZN stock. It goes in alphabetical order.

**NOTE:**I would prefer right now if you guys only played around with ```call_db.py``` 
You can query the database all you want. Just don't try to write to it. I don't have error handles coded in a lot of places yet, so it could mess things up.
If yo want to play with the API's follow the instructions below labeled 

**PLAYING WITH THE API**

First you need to sign-up for the ```Alpaca-Markets-API```

When you sign-up, you will be given an ```API KEY``` and a ```SECRET KEY```. 
Save those somewhere safe. Then copy them from that safe spot into ```config.py```

```python
API_KEY = ("paste_your_key_here")
API_URL = ("https://paper-api.alpaca.markets")
API_SECRET = ("paste_your_secret_key_here")
```
**NOTE:** if you haven't touched Python since the 2.x days, they changed some syntax. 
You used to be able define things like ```python this = "that"``` now you have to do ```python this = ("that")``` There are other minor changes, nothing too crazy though.

Once you have your API keys saved in ```config.py``` you should be able to work with the data. You can test this with ```api_check.py``` in the repo.
Right now the code is iterating through the barsets because that was the last bit of data I was playing with. ```api_check.py``` is just a file I use to hold the api connection. 
You can do whatever you want with it. I need to add quite a few files to ```.gitignore``` but I wanted everybody to have all the little scripts i've been working with before I do.

I think this is basically everything. I just need to walk you guys through what I have so far and then we can all discuss what direction we want to take it. 
There is potentially one more person coming on tomorrow who (looks like) might be ahead of us knowledge wise. She said she had worked with AWS before, so that will be cool.

If you're caught up to this point and don't know what to do you could check out the SQL in ```create_tables.py``` 
I'm not sure the ```SQL PRIMARY KEY``` ```SQL CONSTAINT``` ```SQL FOREIGN KEY``` ```SQL REFERENCES``` are correct. The most I've worked with SQL up to now was when I was doing bug bounties. So mainly just fuzzing SQL injections.

