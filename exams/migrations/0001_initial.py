import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. Mid-Term Exam, End of Year Exam', max_length=150)),
                ('term', models.CharField(choices=[('first', 'First Term'), ('second', 'Second Term'), ('third', 'Third Term')], max_length=10)),
                ('academic_year', models.CharField(help_text='e.g. 2025/2026', max_length=20)),
                ('date', models.DateField(blank=True, help_text='Start date of the exam (optional).', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('classes', models.ManyToManyField(blank=True, related_name='exams', to='academics.schoolclass')),
            ],
            options={
                'ordering': ['-academic_year', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
                ('max_score', models.DecimalField(decimal_places=2, default=100, max_digits=5)),
                ('remarks', models.CharField(blank=True, max_length=100)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='exams.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='students.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='academics.subject')),
            ],
            options={
                'ordering': ['student__roll_number', 'student__full_name'],
                'unique_together': {('exam', 'student', 'subject')},
            },
        ),
    ]
