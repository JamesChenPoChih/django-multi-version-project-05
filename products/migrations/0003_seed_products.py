from django.db import migrations

def seed_products(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    
    products_to_add = [
        {"name": "外套", "price": 199, "image": ""},
        {"name": "帽子", "price": 35, "image": ""},
        {"name": "杯子", "price": 15, "image": ""},
        {"name": "T-shirt", "price": 15, "image": ""},
        {"name": "褲子", "price": 20, "image": ""},
        {"name": "保溫杯", "price": 25, "image": ""},
    ]

    for item in products_to_add:
        Product.objects.get_or_create(
            name=item["name"],
            defaults={
                "price": item["price"],
                "image": item["image"],
                "quantity": 1000
            }
        )

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_quantity'),
    ]

    operations = [
        migrations.RunPython(seed_products),
    ]