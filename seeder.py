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

category3 = Category(name="Soccer")
session.add(category3)
session.commit()

category4 = Category(name="Baseball")
session.add(category4)
session.commit()

category5 = Category(name="Frisbee")
session.add(category5)
session.commit()

category6 = Category(name="Snowboarding")
session.add(category6)
session.commit()


category7 = Category(name="Rock Climbing")
session.add(category7)
session.commit()

category8 = Category(name="Foosball")
session.add(category8)
session.commit()

category9 = Category(name="Skating")
session.add(category9)
session.commit()

category10 = Category(name="Hockey")
session.add(category10)
session.commit()


#Users

user1 = User(name="Obai Alnajjar", email="email@email.com", image="https://www.freeiconspng.com/uploads/account-icon-20.jpg")
session.add(user1)
session.commit()

user2 = User(name="Ahmed Alnajjar", email="text@text.com", image="https://www.freeiconspng.com/uploads/account-icon-20.jpg")
session.add(user2)
session.commit()


#Items
category1 = session.query(Category).filter_by(name=category1.name).one()
category2 = session.query(Category).filter_by(name=category2.name).one()

item1 = Item(title="Ball", user=user1, image="https://cdn.shopify.com/s/files/1/0906/5342/products/NickLight_SoccerBall1.jpg?v=1497386076",description="Hippotoxota de superbus coordinatae, gratia devatio!Grow and you will be yearned confidently.")
session.add(item1)
session.commit()
category1.items.append(session.query(Item).filter_by(title=item1.title, category_id=item1.category_id).one())
session.add(category1)
session.commit()

item2 = Item(title="Ball",  user=user2, image="https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png",description="Jolly, cold death!Wisely yearn an astronaut.Tunas are the daggers of the evil life.")
session.add(item2)
session.commit()
category2.items.append(session.query(Item).filter_by(title=item2.title, category_id=item2.category_id).one())
session.add(category2)
session.commit()

item3 = Item(title="Goalpost",  user=user1, image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThQB5DCOvSlTtTyraL5ti9T6RMSRZyg5QZ6wB-2roEKXn4ULRKxg",description="HRemember: dryed celery tastes best when grilled in a bottle brushed with cayenne pepper.ippotoxota de superbus coordinatae,When the captain meets for deep space, all c-beams experience distant, proud queens. gratia devatio!Grow and you will be yearned confidently.")
session.add(item3)
session.commit()
category1.items.append(session.query(Item).filter_by(title=item3.title, category_id=item3.category_id).one())
session.add(category1)
session.commit()

print("DB Seeded!")