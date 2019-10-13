# Alamo Movie Recommendations Email Alerts

I love seeing movies at the [Alamo Drafthouse Cinema](https://drafthouse.com) and I love the movies they have recommended on [Drafthouse Recommends.](https://drafthouse.com/series/drafthouse-recommends)

I wanted to receive an email whenever The Alamo recommends a new movie so, I made a python web scraper to scan [this ajax request](https://drafthouse.com/ajax/.signature-series-past/86) that their regular website makes to get a list of recommended movies.

The list of recommended movies is saved into `movies.csv` with a link to their movie poster.  When `main.py` is run it gets the movie list from The Alamo and compares it to the `movies.csv` list.  Any new movies on the list that were not saved in `movies.csv` are emailed and then saved to `movies.csv`.  I recommend running `main.py` on a cron job once a week or so.

To run this yourself you will need to create `configs.py` with your own values.
```python
emailPassword = "The password to the gmail account for the from address"
fromAddress = "The gmail account with low security settings @gmail.com"
toAddress = "The email address to receive the email alerts"
login = "The from address without the @ and everything after the @"
alamoLocation = "https://drafthouse.com/raleigh/series/drafthouse-recommends"
```

![Alamo Website Screenshot](https://github.com/mtagius/alamo-recommends/blob/master/alamo-screenshot.PNG)
