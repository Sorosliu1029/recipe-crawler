import scrapy
from xiachufang.items import Recipe


class RecipesSpider(scrapy.Spider):
    name = "recipes"

    start_urls = [
        "https://www.xiachufang.com/category/"
    ]

    allowed_domains = ["xiachufang.com"]

    def parse(self, response):
        for category in response.css('div.cates-list-all'):
            for li in category.xpath('.//li[contains(@id, "cat")]/a'):
                href = li.xpath('@href').extract_first()
                text = li.xpath('text()').extract_first()
                yield response.follow("{}/time/".format(href), callback=self.parse_category)

    def parse_category(self, response):
        try:
            next_page = response.css('a.next')[0]
            if int(next_page.xpath('@href').re_first(r'page=(\d+)$')) <= self.settings.getint('CATEGORY_PAGE_LIMIT'):
                yield response.follow(next_page, callback=self.parse_category)
        except IndexError:
            pass
        for recipe in response.css('div.normal-recipe-list li'):
            if recipe.css('span.green-font'):
                recipe_link = recipe.xpath('.//a/@href')
                yield response.follow(recipe_link.extract_first(), callback=self.parse_recipe)

    def parse_recipe(self, response):
        name = response.css('h1.page-title::text').extract_first().strip()
        rating = response.css('.score')[0]
        rating_value = float(rating.css('.number::text').extract_first())
        best_rating = None
        rating_count = None
        for meta in rating.xpath('.//meta'):
            if meta.xpath('@itemprop').extract_first() == 'bestRating':
                best_rating = float(meta.xpath('@content').extract_first())
            elif meta.xpath('@itemprop').extract_first() == 'ratingCount':
                rating_count = int(meta.xpath('@content').extract_first())
        cooked_number = int(response.css('.cooked').css('.number::text').extract_first())
        favorite_number = int(response.css('.pv').re_first(r'(\d+)'))
        categories = response.css('.recipe-cats').css('a::text').extract()
        recipe_list = list(map(lambda s: s.strip(), response.css('.recipe-menu-name::text').extract()))
        ingredients = list(map(extract_ingredient, response.css('.ings').css('tr')))
        instructions = response.css('.steps').css('ol li p::text').extract()
        tips = response.css('.tip::text').extract_first()
        yield Recipe({
            "name": name,
            "rating_value": rating_value,
            "best_rating": best_rating,
            "rating_count": rating_count,
            "cooked_number": cooked_number,
            "favorited_number": favorite_number,
            "categories": categories,
            "recipe_list": recipe_list,
            "ingredients": ingredients,
            "instructions": instructions,
            "tips": tips.strip() if tips else tips 
        })


def extract_ingredient(tr_selector):
    unit = tr_selector.css('.unit::text').extract_first()
    name = tr_selector.css('a::text').extract_first()
    if name is None:
        name = tr_selector.css('.name::text').extract_first()
    return "{} {}".format(unit.strip(), name.strip()).strip()