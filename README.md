# iTunes App Store Feedback Scraper

Install with pip:

```
pip install git+git://github.com/allawi/itunes-feedback-scraper.git@v1.0.0
```

Import it as a module

```
from iscraper import iTunesScraper
```

run it with

```
iTunesScraper.get_reviews(app_id, [country])
```

where `app_id` is the ID of the app you wish to scrape and country is which country to scrape the feedback from.
Not providing a country will default to returning a `dict` of all countries and their feedback.

The return value is

```
{
  'date': 'Sep 04, 2011',
  'stars': '5',
  'text': 'This app is really fantastic for plenty of reasons.',
  'title': 'A fantastic app!',
  'username': 'AyyLmao123',
  'version': '2.2'
}
```

Inspired by:

http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
