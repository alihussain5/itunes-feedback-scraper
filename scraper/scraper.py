import requests
import xml.etree.ElementTree as ET

from config import Config


class iTunesScraper(object):
    @classmethod
    def _request_itunes(cls, app_id, store_id, page):
        headers = {'X-Apple-Store-Front': Config.STORE_FRONT.format(store_id=store_id), 'User-Agent': Config.USER_AGENT}

        r = requests.get(Config.URL.format(app_id=app_id, page=page), headers=headers)

        if r.status_code != 200:
            raise RuntimeError('Failed to get data for {}: {}'.format(store_id, r.status_code))

        return r.content

    @classmethod
    def _parse_itunes_xml(cls, data):
        reviews = []

        try:
            root = ET.fromstring(data)
        except:
            return reviews

        for node in root.findall(Config.REVIEW_NODE, Config.NAMESPACE):
            review = {}

            star_data = node.find(Config.STAR_CHILD, Config.NAMESPACE)
            text_data = node.find(Config.TEXT_CHILD, Config.NAMESPACE)
            review_metadata = node.findall(Config.METADATA_CHILD, Config.NAMESPACE)

            review['title'] = review_metadata[0][0].text
            review['stars'] = star_data.get('alt').strip(' stars')
            review['text'] = text_data.text
            review['username'] = review_metadata[1][0][0].text.strip()

            version_date_data = review_metadata[1][0].tail

            version = Config.VERSION_RE.search(version_date_data)

            if version:
                review['version'] = version.group()
            else:
                review['version'] = None

            date = Config.DATE_RE.search(version_date_data)

            if date:
                review['date'] = date.group()
            else:
                review['date'] = None

            reviews.append(review)

        return reviews

    @classmethod
    def _get_all_pages(cls, app_id, store_id):
        reviews = []
        page = 0

        while 1:
            reviews_xml = cls._request_itunes(app_id, store_id, page)
            reviews_parsed = cls._parse_itunes_xml(reviews_xml)

            if not reviews_parsed:
                break

            reviews += reviews_parsed
            page += 1

        return reviews

    @classmethod
    def _get_all_countries(cls, app_id):
        reviews = {}

        for country, store_id in Config.COUNTRIES.iteritems():
            reviews[country] = cls._get_all_pages(app_id, store_id)

        return reviews

    @classmethod
    def _get_reviews_country(cls, app_id, country='US'):
        if len(country) != 2 and len(country) != 6:
            raise ValueError('Either use a country code or a store id')

        if len(country) == 2:
            if country not in Config.COUNTRIES:
                raise ValueError('{} is not a valid country'.format(country))

            country = Config.COUNTRIES[country]

        if len(country) == 6:
            if country not in Config.COUNTRIES.values():
                raise ValueError('{} is not a valid store id'.format(country))

        reviews = cls._get_all_pages(app_id, country)

        return reviews

    @classmethod
    def get_reviews(cls, app_id, country=None):
        if country is None:
            return cls._get_all_countries(app_id)

        return cls._get_reviews_country(app_id, country)
