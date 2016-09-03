# iTunes App Store Feedback Scraper

Import it as a module, run it with

```
iTunesScraper.get_reviews(app_id, country=None)
```

where `app_id` is the ID of the app you wish to scrape and country is which country to scrape the feedback from.
Not providing a country will default to returning a `dict` of all countries and their feedback.

Inspired by:

http://blogs.oreilly.com/iphone/2008/08/scraping-appstore-reviews.html
