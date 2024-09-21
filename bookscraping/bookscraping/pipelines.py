# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapingPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        #strip all white space from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value =adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        
        ## category and product type switch to lower case
        lowecase_key = ['category', 'product_type']
        for lowecase_key in lowecase_key:
            value = adapter.get(lowecase_key)
        adapter[lowecase_key] = value.lower()


        ##price-- convet to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax','tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## availability extract number of books in    stock

        availablity_string = adapter.get('availablity')
        split_string_array = availablity_string.split('(')
        if len(split_string_array) <2:
            adapter['availablity'] = 0
        else:
            availablity_array = split_string_array[1].split(' ')
            adapter['availablity'] = int(availablity_array[0])
        
        ## review convert string to number
        num_review_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_review_string)


        ##stars convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value =="one":
            adapter['stars'] = 1
        elif stars_text_value =="two":
            adapter['stars'] = 2
        elif stars_text_value =="three":
            adapter['stars'] = 3
        elif stars_text_value =="four":
            adapter['stars'] = 4
        
        elif stars_text_value =="five":
            adapter['stars'] = 5
        

        return item
