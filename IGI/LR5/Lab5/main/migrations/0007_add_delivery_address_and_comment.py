from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_date_delivery_order_delivery_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(default='', max_length=255, verbose_name='Адрес доставки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий к заказу'),
        ),
    ] 