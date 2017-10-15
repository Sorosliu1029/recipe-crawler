# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Recipe(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    rating_value = scrapy.Field()
    best_rating = scrapy.Field()
    rating_count = scrapy.Field()
    cooked_number = scrapy.Field()
    favorited_number = scrapy.Field()
    categories = scrapy.Field()
    recipe_list = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    tips = scrapy.Field()