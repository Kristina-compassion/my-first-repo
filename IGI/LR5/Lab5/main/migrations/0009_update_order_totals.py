from django.db import migrations

def update_order_totals(apps, schema_editor):
    Order = apps.get_model('main', 'Order')
    for order in Order.objects.all():
        total = sum(item.total_price for item in order.order_items.all())
        order.total_sum = total
        order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_order_options_remove_order_discount_amount_and_more'),
    ]

    operations = [
        migrations.RunPython(update_order_totals, reverse_code=migrations.RunPython.noop),
    ] 