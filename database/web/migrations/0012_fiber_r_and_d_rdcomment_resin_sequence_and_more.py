# Generated by Django 4.2.11 on 2024-05-27 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_remove_project_partsnumber_project_quantityofpart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fiber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, max_length=255, null=True, verbose_name='Material')),
                ('manufacturer', models.CharField(blank=True, max_length=255, null=True, verbose_name='Manufacturer')),
                ('distributor', models.CharField(max_length=255, verbose_name='Distributor')),
                ('grade', models.CharField(blank=True, max_length=255, null=True, verbose_name='Grade')),
                ('singleFilamentDiameter', models.CharField(blank=True, max_length=255, null=True, verbose_name='Single filament diameter (mm)')),
                ('tow', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tow')),
                ('towInThousands', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tow (in thousands)')),
                ('tex', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tex (g/km)')),
                ('density', models.CharField(blank=True, max_length=255, null=True, verbose_name='Density (g/cm3)')),
                ('theoreticalDrySection', models.CharField(blank=True, max_length=255, null=True, verbose_name='Theoretical dry section (mm2)')),
                ('tensileStrength', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tensile strength (MPa)')),
                ('tensileModulus', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tensile modulus (GPa)')),
            ],
        ),
        migrations.CreateModel(
            name='R_and_D',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(blank=True, max_length=255, null=True, verbose_name='Program :')),
                ('projectNr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Project Nr. :')),
                ('ERMDS', models.CharField(max_length=255, unique=True, verbose_name='ERMDS Nr. :')),
                ('lastUpdate', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last update :')),
                ('verifiedBy', models.CharField(blank=True, max_length=255, null=True, verbose_name='Verified by:')),
                ('approvedBy', models.CharField(blank=True, max_length=255, null=True, verbose_name='Approved by :')),
                ('numberOfBobbins', models.IntegerField(blank=True, null=True, verbose_name='Number of bobbins')),
                ('endEffector', models.CharField(blank=True, max_length=255, null=True, verbose_name='End-effector N°')),
                ('impregnationBath', models.CharField(blank=True, max_length=255, null=True, verbose_name='Impregnation bath')),
                ('entryNozzleDiam', models.CharField(blank=True, max_length=255, null=True, verbose_name='Entry nozzle diameter (mm)')),
                ('exitNozzleDiam', models.CharField(blank=True, max_length=255, null=True, verbose_name='Exit nozzle diameter (mm)')),
                ('roomTemperature', models.CharField(blank=True, max_length=255, null=True, verbose_name='Room temperature (°C)')),
                ('roomhumidity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Room humidity (%)')),
                ('brakeForcebobin', models.CharField(blank=True, max_length=255, null=True, verbose_name='Brake force/bobbin (N) (kg) (bar)')),
                ('windingSpeedRange', models.CharField(blank=True, max_length=255, null=True, verbose_name='Windng speed range (mm/s)')),
                ('FVR', models.CharField(blank=True, max_length=255, null=True, verbose_name='FVR (%)')),
                ('compositeDensity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Composite density ρ (g/cm3)')),
                ('porosity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Porosity (%)')),
                ('theoreticalSampleSection', models.CharField(blank=True, max_length=255, null=True, verbose_name='Theoretical sample section (mm²)')),
                ('experimentalSampleSection', models.CharField(blank=True, max_length=255, null=True, verbose_name='Experimental sample section (mm²)')),
                ('aged', models.CharField(blank=True, max_length=255, null=True, verbose_name='Aged / Non-aged')),
                ('temperatureOfTests', models.CharField(blank=True, max_length=255, null=True, verbose_name='Temperature of the tests')),
                ('numberOfSamples', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of samples')),
                ('configurarion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Configuration')),
                ('sampleLength', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sample length')),
                ('numberOfCycles', models.CharField(blank=True, max_length=255, null=True, verbose_name='Number of cycles')),
                ('sleeve', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sleeve diameter / height (mm)')),
                ('thermalExpansionCoefficient', models.CharField(blank=True, max_length=255, null=True, verbose_name='Thermal expansion coefficient A (/K)')),
                ('thermalConductivity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Thermal conductivity K (W/(m.K))')),
                ('tensileYoungModulus', models.FloatField(blank=True, null=True, verbose_name="Tensile Young's modulus - Average (MPa)")),
                ('tensileUltimateStress', models.FloatField(blank=True, null=True, verbose_name='Tensile Ultimate Stress - Average (MPa)')),
                ('tensileUltimateStressMA', models.FloatField(blank=True, null=True, verbose_name='Tensile Ultimate Stress - Min A (MPa)')),
                ('tensileUltimateStressMB', models.FloatField(blank=True, null=True, verbose_name='Tensile Ultimate Stress - Min B (MPa)')),
                ('tensileUltimateLoad', models.FloatField(blank=True, null=True, verbose_name='Tensile Ultimate Load - Average (kN)')),
                ('tensileYieldStress', models.FloatField(blank=True, null=True, verbose_name='Tensile Yield Stress - Average (MPa)')),
                ('tensileYieldStressMA', models.FloatField(blank=True, null=True, verbose_name='Tensile Yield Stress - Min A (MPa)')),
                ('tensileYieldStressMB', models.FloatField(blank=True, null=True, verbose_name='Tensile Yield Stress - Min B (MPa)')),
                ('tensileYieldLoad', models.FloatField(blank=True, null=True, verbose_name='Tensile Yield Load - Average (kN)')),
                ('compressionYoungModulus', models.FloatField(blank=True, null=True, verbose_name="Compression Young's modulus - Average (MPa)")),
                ('compressionUltimateStress', models.FloatField(blank=True, null=True, verbose_name='Compression Ultimate Stress - Average (MPa)')),
                ('compressionUltimateStressMA', models.FloatField(blank=True, null=True, verbose_name='Compression Ultimate Stress - Min A (MPa)')),
                ('compressionUltimateStressMB', models.FloatField(blank=True, null=True, verbose_name='Compression Ultimate Stress - Min B (MPa)')),
                ('compressionUltimateLoad', models.FloatField(blank=True, null=True, verbose_name='Compression Ultimate Load - Average (kN)')),
                ('compressionYieldStress', models.FloatField(blank=True, null=True, verbose_name='Compression Yield Stress- Average (MPa)')),
                ('compressionYieldStressMA', models.FloatField(blank=True, null=True, verbose_name='Compression Yield Stress - Min A (MPa)')),
                ('compressionYieldStressMB', models.FloatField(blank=True, null=True, verbose_name='Compression Yield Stress - Min B (MPa)')),
                ('compressionYieldLoad', models.FloatField(blank=True, null=True, verbose_name='Compression Yield Load - Average (kN)')),
                ('poissonRatio', models.FloatField(blank=True, null=True, verbose_name="Poisson's ratio ν (-)")),
                ('flexuralModulusILSS', models.FloatField(blank=True, null=True, verbose_name='Flexural modulus - Average (MPa)')),
                ('ultimateShearForce', models.FloatField(blank=True, null=True, verbose_name='Ultimate Shear Force - Average (kN)')),
                ('ultimateShearStress', models.FloatField(blank=True, null=True, verbose_name='Ultimate Shear Stress - Average (MPa)')),
                ('ultimateShearStressMA', models.FloatField(blank=True, null=True, verbose_name='Ultimate Shear Stress - Min A (MPa)')),
                ('ultimateShearStressMB', models.FloatField(blank=True, null=True, verbose_name='Ultimate Shear Stress - Min B (MPa)')),
                ('flexuralModulusF', models.FloatField(blank=True, null=True, verbose_name='Flexural modulus - Average (MPa)')),
                ('flexuralUltimateStrength', models.FloatField(blank=True, null=True, verbose_name='Flexural Ultimate strength - Average (MPa)')),
                ('flexuralUltimateStrengthMA', models.FloatField(blank=True, null=True, verbose_name='Flexural Ultimate strength - Min A (MPa)')),
                ('flexuralUltimateStrengthMB', models.FloatField(blank=True, null=True, verbose_name='Flexural Ultimate strength - Min B (MPa)')),
                ('strainUltimateStrength', models.FloatField(blank=True, null=True, verbose_name='Strain at ultimate strength (%)')),
                ('flexuralUltimateForce', models.FloatField(blank=True, null=True, verbose_name=' Flexural Ultimate Force (N)')),
                ('yieldTorque', models.FloatField(blank=True, null=True, verbose_name='Yield Torque (Nm)')),
                ('maxiTorque', models.FloatField(blank=True, null=True, verbose_name='Maxi Torque (Nm)')),
                ('yieldAngle', models.FloatField(blank=True, null=True, verbose_name='Yield angle (°)')),
                ('maxiTwistedAngle', models.FloatField(blank=True, null=True, verbose_name='Maxi Twisted Angle (°)')),
                ('fiber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.fiber', verbose_name='Fiber')),
            ],
        ),
        migrations.CreateModel(
            name='RDComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiber', models.CharField(blank=True, max_length=255, null=True)),
                ('numberOfBobbins', models.CharField(blank=True, max_length=255, null=True)),
                ('resin', models.CharField(blank=True, max_length=255, null=True)),
                ('handener', models.CharField(blank=True, max_length=255, null=True)),
                ('curingCycle', models.CharField(blank=True, max_length=255, null=True)),
                ('fiberTow', models.CharField(blank=True, max_length=255, null=True)),
                ('fiberTex', models.CharField(blank=True, max_length=255, null=True)),
                ('fiberDensity', models.CharField(blank=True, max_length=255, null=True)),
                ('matrixDensity', models.CharField(blank=True, max_length=255, null=True)),
                ('endEffector', models.CharField(blank=True, max_length=255, null=True)),
                ('impregnationBath', models.CharField(blank=True, max_length=255, null=True)),
                ('entryNozzleDiam', models.CharField(blank=True, max_length=255, null=True)),
                ('exitNozzleDiam', models.CharField(blank=True, max_length=255, null=True)),
                ('roomTemperature', models.CharField(blank=True, max_length=255, null=True)),
                ('roomhumidity', models.CharField(blank=True, max_length=255, null=True)),
                ('brakeForcebobin', models.CharField(blank=True, max_length=255, null=True)),
                ('windingSpeedRange', models.CharField(blank=True, max_length=255, null=True)),
                ('FVR', models.CharField(blank=True, max_length=255, null=True)),
                ('compositeDensity', models.CharField(blank=True, max_length=255, null=True)),
                ('porosity', models.CharField(blank=True, max_length=255, null=True)),
                ('theoreticalSampleSection', models.CharField(blank=True, max_length=255, null=True)),
                ('experimentalSampleSection', models.CharField(blank=True, max_length=255, null=True)),
                ('aged', models.CharField(blank=True, max_length=255, null=True)),
                ('temperatureOfTests', models.CharField(blank=True, max_length=255, null=True)),
                ('numberOfSamples', models.CharField(blank=True, max_length=255, null=True)),
                ('configurarion', models.CharField(blank=True, max_length=255, null=True)),
                ('sampleLength', models.CharField(blank=True, max_length=255, null=True)),
                ('numberOfCycles', models.CharField(blank=True, max_length=255, null=True)),
                ('sleeve', models.CharField(blank=True, max_length=255, null=True)),
                ('thermalExpansionCoefficient', models.CharField(blank=True, max_length=255, null=True)),
                ('thermalConductivity', models.CharField(blank=True, max_length=255, null=True)),
                ('tensileYoungModulus', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileUltimateStress', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileUltimateStressMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileUltimateStressMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileUltimateLoad', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileYieldStress', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileYieldStressMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileYieldStressMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('tensileYieldLoad', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionYoungModulus', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionUltimateStress', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionUltimateStressMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionUltimateStressMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionUltimateLoad', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionYieldStress', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionYieldStressMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionYieldStressMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('compressionYieldLoad', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('poissonRatio', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralModulusILSS', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('ultimateShearForce', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('ultimateShearStress', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('ultimateShearStressMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('ultimateShearStressMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralModulusF', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralUltimateStrength', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralUltimateStrengthMA', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralUltimateStrengthMB', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('strainUltimateStrength', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('flexuralUltimateForce', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('yieldTorque', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('maxiTorque', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('yieldAngle', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('maxiTwistedAngle', models.CharField(blank=True, default='Samples number: ', max_length=255, null=True)),
                ('ERMDS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.r_and_d', verbose_name='ERMDS')),
            ],
        ),
        migrations.CreateModel(
            name='Resin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=255, verbose_name='Manufacturer')),
                ('resin', models.CharField(max_length=255, verbose_name='Resin system - Resin')),
                ('hardener', models.CharField(max_length=255, unique=True, verbose_name='Resin system - Hardener')),
                ('accelerator', models.CharField(blank=True, max_length=255, null=True, verbose_name='Resin system - Accelerator')),
                ('ratioWR', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(weight) R')),
                ('ratioWH', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(weight) H')),
                ('ratioWA', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(weight) A')),
                ('ratioVR', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(volume) R')),
                ('ratioVH', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(volume) H')),
                ('ratioVA', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ratio(volume) A')),
                ('potLife', models.CharField(blank=True, max_length=255, null=True, verbose_name='Pot life (Process T°;h)')),
                ('processT', models.CharField(blank=True, max_length=255, null=True, verbose_name='Process T (°C)')),
                ('curingCycle', models.CharField(blank=True, max_length=255, null=True, verbose_name='Curing cycle')),
                ('tg', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tg (°C)')),
                ('priceResin', models.CharField(blank=True, max_length=255, null=True, verbose_name='Price resin')),
                ('priceHardener', models.CharField(blank=True, max_length=255, null=True, verbose_name='Price hardener')),
                ('densityR', models.CharField(blank=True, max_length=255, null=True, verbose_name='Density (g/cm³)')),
                ('flexuralStrength', models.CharField(blank=True, max_length=255, null=True, verbose_name='Flexural strength (MPa)')),
                ('flexuralmodulus', models.CharField(blank=True, max_length=255, null=True, verbose_name='Flexural modulus (GPa)')),
                ('modulusElasticity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Modulus of elasticity (GPa) (tensile)')),
                ('tensileStrength', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tensile strength (MPa)')),
                ('elongationBreak', models.CharField(blank=True, max_length=255, null=True, verbose_name='Elongation at break (%)')),
                ('compressionUltStrength', models.CharField(blank=True, max_length=255, null=True, verbose_name='Compression ult. strength (MPa)')),
                ('compressionModulus', models.CharField(blank=True, max_length=255, null=True, verbose_name='Compression modulus (GPa)')),
                ('thermalExpansionCoefficient', models.CharField(blank=True, max_length=255, null=True, verbose_name='Thermal expansion coefficient (ppm/K)')),
                ('charpyimpact', models.CharField(blank=True, max_length=255, null=True, verbose_name='Charpy impact at RT (mJ/mm²)')),
                ('fractureToughness', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fracture toughness K1C (Mpa.m1/2)')),
                ('fractureEnergy', models.CharField(blank=True, max_length=255, null=True, verbose_name='Fracture energy G1C (J/m²)')),
                ('totalShrinkage', models.CharField(blank=True, max_length=255, null=True, verbose_name='Total shrinkage at RT (Vol%)')),
                ('Hardness', models.CharField(blank=True, max_length=255, null=True, verbose_name='Hardness at RT')),
                ('waterAbsorption', models.CharField(blank=True, max_length=255, null=True, verbose_name='Water absorption (7d at 23°C)')),
            ],
        ),
        migrations.CreateModel(
            name='Sequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequenceName', models.CharField(max_length=255, verbose_name='Sequence Name')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
        ),
        migrations.RemoveField(
            model_name='part',
            name='compressionYoungModulus',
        ),
        migrations.RemoveField(
            model_name='part',
            name='defaultCycleNumber',
        ),
        migrations.RemoveField(
            model_name='part',
            name='fiberDensity',
        ),
        migrations.RemoveField(
            model_name='part',
            name='fiberName',
        ),
        migrations.RemoveField(
            model_name='part',
            name='fiberSectionAcc',
        ),
        migrations.RemoveField(
            model_name='part',
            name='fiberSectionCalc',
        ),
        migrations.RemoveField(
            model_name='part',
            name='fiberVolumeRatio',
        ),
        migrations.RemoveField(
            model_name='part',
            name='flexuralModulus',
        ),
        migrations.RemoveField(
            model_name='part',
            name='resinDensity',
        ),
        migrations.RemoveField(
            model_name='part',
            name='resinName',
        ),
        migrations.RemoveField(
            model_name='part',
            name='tensileUtimateStress',
        ),
        migrations.RemoveField(
            model_name='part',
            name='tensileYieldStress',
        ),
        migrations.RemoveField(
            model_name='part',
            name='tensileYoungModulus',
        ),
        migrations.RemoveField(
            model_name='part',
            name='totalTowNumber',
        ),
        migrations.RemoveField(
            model_name='part',
            name='windingDensity',
        ),
        migrations.RemoveField(
            model_name='winding',
            name='windingType',
        ),
        migrations.DeleteModel(
            name='WindingType',
        ),
        migrations.AddField(
            model_name='r_and_d',
            name='resin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.resin', verbose_name='Resin'),
        ),
        migrations.AddField(
            model_name='winding',
            name='sequence',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.sequence', verbose_name='WindingType Description'),
            preserve_default=False,
        ),
    ]
