from app.db.database import SessionLocal
from app.db.models import Product

db = SessionLocal()

product1 = Product(title="Ноутбук", price=50000.0, count = 10)
product2 = Product(title="Наушники", price = 3500.0, count = 17)

db.add_all([product1, product2])

db.commit()

print("В таблицу были добавлены 2 записи")

products = db.query(Product).all()

for p in products:
    print(f"ID: {p.id}, Название: {p.title}, Цена: {p.price}, Количество: {p.count}")
    
db.close()