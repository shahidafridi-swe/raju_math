# Generated by Django 5.0.7 on 2024-08-12 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_payment_is_paid_alter_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
