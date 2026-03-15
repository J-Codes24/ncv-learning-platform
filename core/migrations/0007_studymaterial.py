from django.db import migrations, models
import django.db.models.deletion
import core.models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_studentprofile_paperprogress_videoprogress"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudyMaterial",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("level", models.CharField(choices=[("L2", "Level 2"), ("L3", "Level 3"), ("L4", "Level 4")], default="L2", max_length=2)),
                ("material_file", models.FileField(upload_to=core.models.study_material_upload_path)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("subject", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="study_materials", to="core.subject")),
            ],
        ),
    ]
