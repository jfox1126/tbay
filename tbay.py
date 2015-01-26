from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

engine = create_engine('postgresql://action:action@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
  __tablename__ = "item"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String)
  start_time = Column(DateTime, default=datetime.utcnow)
  owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  bids = relationship("Bid", backref="item")
  
class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  username = Column(String, nullable=False)
  password = Column(String, nullable=False)
  auctions = relationship("Item", backref="owner")
  bids = relationship("Bid", backref="bidder")
  
class Bid(Base):
  __tablename__ = "bid"
  id = Column(Integer, primary_key=True) 
  price = Column(Integer, nullable=False)
  bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  item_id = Column(Integer, ForeignKey('item.id'), nullable=False)

#Create tables/classes
Base.metadata.create_all(engine)

#Users
jared = User(username="jrod", password="dogs")
anne = User(username="adog", password="cats")
riley = User(username="rman", password="fish")

#Items
baseball = Item(name="baseball", description="white & round w/stiches", owner=jared)
basketball = Item(name="basketball", description="big & orange", owner=riley)

#Bids
b1 = Bid(price=10, bidder=riley, item=baseball)
b2 = Bid(price=15, bidder=anne, item=baseball)
b3 = Bid(price=20, bidder=riley, item=baseball)
b4 = Bid(price=18, bidder=jared, item=basketball)


def add_elements():
  """Add users, items, and bids from abov"""
  session.add_all([jared, anne, riley, baseball, basketball, b1, b2, b3, b4])
  session.commit()
#add_elements()

def find_highest(item):
  print item + " has the following bids:"
  highest_bid = 0
  leader = 0
  for i, b, u in session.query(Item, Bid, User).\
      filter(Item.name == str(item)).\
      filter(Bid.item_id == Item.id).\
      filter(User.id == Bid.bidder_id).\
      all():
    print "$" + str(b.price) + " by " + u.username
    if b.price > highest_bid:
      highest_bid = b.price
      leader = u.username
  print leader + " has the highest bid at $" + str(highest_bid)
  
def seller_dashboard(user):
  for item in user.auctions:
    print user.username + " is selling " + item.name
    find_highest(item.name)