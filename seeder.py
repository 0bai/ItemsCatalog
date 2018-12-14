from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itemsCatalogDB_setup import Base, User, Item, Category

engine = create_engine('sqlite:///itemsCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Categories

category1 = Category(name="Football")
session.add(category1)
session.commit()

category2 = Category(name="BasketBall")
session.add(category2)
session.commit()

category3 = Category(name="TVs")
session.add(category3)
session.commit()

#Users

user1 = User(full_name="Obai Alnajjar", email="email@email.com", image="https://www.freeiconspng.com/uploads/account-icon-20.jpg")
user1.hash_password("pass")
session.add(user1)
session.commit()

user2 = User(full_name="Ahmed Alnajjar", email="text@text.com", image="https://www.freeiconspng.com/uploads/account-icon-20.jpg")
user2.hash_password("somePass")
session.add(user2)
session.commit()


#Items

item1 = Item(title="Ball", category=category1, user=user1, image="https://cdn.shopify.com/s/files/1/0906/5342/products/NickLight_SoccerBall1.jpg?v=1497386076",description="Hippotoxota de superbus coordinatae, gratia devatio!Grow and you will be yearned confidently.")
session.add(item1)
session.commit()

item2 = Item(title="Ball", category=category2, user=user2, image="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png",description="Jolly, cold death!Wisely yearn an astronaut.Tunas are the daggers of the evil life.")
session.add(item2)
session.commit()

item3 = Item(title="Goalpost", category=category1, user=user1, image="https://www.itsagoal.net/wp-content/uploads/2013/11/foldaway-goal.jpg",description="HRemember: dryed celery tastes best when grilled in a bottle brushed with cayenne pepper.ippotoxota de superbus coordinatae,When the captain meets for deep space, all c-beams experience distant, proud queens. gratia devatio!Grow and you will be yearned confidently.")
session.add(item3)
session.commit()

print("DB Seeded!")