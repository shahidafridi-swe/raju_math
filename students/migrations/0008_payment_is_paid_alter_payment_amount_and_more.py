# Generated by Django 5.0.7 on 2024-08-12 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_subject_student_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='month',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='payment',
            name='year',
            field=models.IntegerField(),
        ),
    ]
