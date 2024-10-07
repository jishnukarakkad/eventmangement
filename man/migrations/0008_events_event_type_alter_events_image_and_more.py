# Generated by Django 5.0.2 on 2024-10-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('man', '0007_events_image_alter_events_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='event_type',
            field=models.CharField(choices=[('wedding', 'Wedding'), ('birthday', 'Birthday Party'), ('reception', 'Reception'), ('conference', 'Conference'), ('other', 'Other Event')], default='other', max_length=20),
        ),
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
        migrations.AlterField(
            model_name='events',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
