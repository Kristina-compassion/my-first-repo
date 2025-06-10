from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_order_discount_amount_order_promocode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_delivery',
            new_name='delivery_date',
        ),
    ] 