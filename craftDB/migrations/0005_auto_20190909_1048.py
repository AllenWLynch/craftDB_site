# Generated by Django 2.2.4 on 2019-09-09 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('craftDB', '0004_auto_20190906_2336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mod',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='mod',
            name='overwriting_mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='craftDB.Mod', verbose_name='Overwritten By'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='dependencies',
            field=models.ManyToManyField(blank=True, related_name='dependent_recipes', to='craftDB.Mod'),
        ),
        migrations.AlterField(
            model_name='oredict',
            name='leading_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead', to='craftDB.Item', verbose_name='Representative Item'),
        ),
    ]
