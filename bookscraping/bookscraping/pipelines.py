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



from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask('__name__')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = b'_5#y2L"F4Q8zksldkjfksd/'
db = SQLAlchemy(app)






# Create an in-memory SQLite database engine
#engine = create_engine('sqlite:///:memory:')

# Define Table Classes
#Base = declarative_base()
class Books(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(80), unique=True, nullable=False)
    title = db.Column(db.String(120), unique=True, nullable=False)
    product_type = db.Column(db.String(120), unique=True, nullable=False)
    price_excl_tax = db.Column(db.Integer(), unique=False, nullable=True)
    price_incl_tax = db.Column(db.Integer(), unique=False, nullable=False)
    tax = db.Column(db.Integer(), unique=False, nullable=False)
    num_reviews = db.Column(db.Integer(), unique=False, nullable=False)
    stars = db.Column(db.Integer(), unique=False, nullable=False)
    description = db.Column(db.String(900), unique=False, nullable=False)
    price = db.Column(db.Integer(), unique=False, nullable=False)

        
    with app.app_context():
            db.create_all()
    def __repr__(self):
                #db.create_all()
                #db.commit()
        return '<Booking %r>' % self.url, self.title, self.product_type, self.price_excl_tax, self.price_incl_tax,self.tax , self.num_reviews ,self.stars, self.description, self.price
                #db.create_all()
                #db.commit()
        
class save_to_sqlite():
   # __tablename__ = 'Books'


    #custom_id = Column(Integer, primary_key=True)
    #url = Column(String, unique=True)
    #title = Column(String, unique=True)
    #product_type = Column(String, unique=False)
    #price_excl_tax = Column(Integer, unique=False)
    #price_incl_tax = Column(Integer, unique=False)
    #tax = Column( Integer , unique=False)
    #availablity = Column(Integer, unique=False)
    #num_reviews = Column(Integer, unique=False)
    #stars = Column(Integer, unique=False)
   # description = Column(String, unique=True)
   # price = Column(Integer, unique=False)
    
   
    #Base.metadata.create_all(engine)


    def process_items(self, item, spider):
      

    # todb = Books(url=url,title=title,product_type=product_type,price_excl_tax=price_excl_tax,price_incl_tax=price_incl_tax,tax=tax, availablity=availablity, num_review=num_review,stars=stars,description=description,price=price)
        #with engine.connect() as conn:
         #   result = self.curl.conn.execute(
          #  add(Books),
           # [
            #url : item['url'],
            #title = item['title'],
            #product_type = item['product_type'],
            #price_excl_tax = item['price_excl_tax'],
            #price_incl_tax = item['price_incl_tax'],
            #tax = item['tax'],
            #availablity = item['availablity'],
            #num_review = item['num_review'],
            #stars = item['stars'],
            #description = item['description'],
            #price = item['price'],
            #]
            #)
        #self.conn.commit()
        #return item 
        url = item['url'],
        title = item['title'],
        product_type = item['product_type'],
        price_excl_tax = item['price_excl_tax'],
        price_incl_tax = item['price_incl_tax'],
        tax = item['tax'],
        availablity = item['availablity'],
        num_review = item['num_review'],
        stars = item['stars'],
        description = item['description'],
        price = item['price'],
            
        upload =  Books(url=url,title=title,product_type=product_type,price_excl_tax=price_excl_tax,price_incl_tax=price_incl_tax,tax=tax, availablity=availablity, num_review=num_review,stars=stars,description=description,price=price)
		#upload = Books( name = name, email=email, phone_num=phone_num, case = case ,message = message)
        db.session.add(upload)
        db.session.commit()
		#flash('You booked successfully ')
        return item



    def close_spider(self, spider):
        self.close()
        