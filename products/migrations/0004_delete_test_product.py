from django.db import migrations

def delete_test_product(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    # 尋找並自動刪除名稱為「測試商品」的品項
    Product.objects.filter(name='測試商品').delete()

class Migration(migrations.Migration):

    dependencies = [
        # 依賴於您上一個建立的 migration 檔案
        ('products', '0003_seed_products'),
    ]

    operations = [
        migrations.RunPython(delete_test_product),
    ]