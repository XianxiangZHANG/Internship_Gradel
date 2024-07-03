from django.db import models
from django.db.models import Sum
import math

class Department(models.Model):
    """ DepartmentTable """
    title = models.CharField(verbose_name="Title", max_length=30)
    # number = models.IntegerField(verbose_name="Number of members", null=True, blank=True)

    def __str__(self):
        return self.title


class User(models.Model):
    """ UserTable """
    username = models.CharField(verbose_name="Username", max_length=30)
    password = models.CharField(verbose_name="Password", max_length=255, default="1a7928232fd865f75808759d0ab8d24f") #default password : 123
    depart = models.ForeignKey(verbose_name="Department", to=Department, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return self.username

class Log(models.Model):
    user = models.ForeignKey(verbose_name="Username:",to=User, on_delete=models.CASCADE, to_field='id')
    action = models.CharField(verbose_name="Action:",max_length=30)
    model = models.CharField(verbose_name="Table:",max_length=30)
    object_id = models.CharField(verbose_name="Object ID:",max_length=50)
    timestamp = models.DateTimeField(verbose_name="Timestamp: (From - To)",max_length=50)
    # timestamp = models.CharField(max_length=50)
    changes = models.TextField(verbose_name="Changes:",null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} {self.action} {self.model} {self.object_id} on {self.timestamp}"



class Resin(models.Model):
    """ Resin Table """
    manufacturer = models.CharField(verbose_name="Manufacturer", max_length=50, null=True, blank=True)    
    resin = models.CharField(verbose_name="Resin system - Resin", max_length=50, null=True, blank=True)
    hardener = models.CharField(verbose_name="Resin system - Hardener", max_length=50, null=True, blank=True)
    accelerator = models.CharField(verbose_name="Resin system - Accelerator", max_length=50, null=True, blank=True)
    
    ratioWR = models.CharField(verbose_name="Ratio(weight) R", max_length=30, null=True, blank=True)
    ratioWH = models.CharField(verbose_name="Ratio(weight) H", max_length=30, null=True, blank=True)
    ratioWA = models.CharField(verbose_name="Ratio(weight) A", max_length=30, null=True, blank=True)

    ratioVR = models.CharField(verbose_name="Ratio(volume) R", max_length=30, null=True, blank=True)
    ratioVH = models.CharField(verbose_name="Ratio(volume) H", max_length=30, null=True, blank=True)
    ratioVA = models.CharField(verbose_name="Ratio(volume) A", max_length=30, null=True, blank=True)

    potLife = models.CharField(verbose_name="Pot life (Process T°;h)", max_length=255, null=True, blank=True)
    processT = models.CharField(verbose_name="Process T (°C)", max_length=30, null=True, blank=True)
    curingCycle = models.CharField(verbose_name="Curing cycle", max_length=255, null=True, blank=True)
    tg = models.CharField(verbose_name="Tg (°C)", max_length=30, null=True, blank=True)

    priceResin = models.CharField(verbose_name="Price resin", max_length=30, null=True, blank=True)
    priceHardener = models.CharField(verbose_name="Price hardener", max_length=30, null=True, blank=True)

    densityR = models.FloatField(verbose_name="Density (g/cm³)", null=True, blank=True)
    flexuralStrength = models.CharField(verbose_name="Flexural strength (MPa)", max_length=30, null=True, blank=True)
    flexuralmodulus = models.CharField(verbose_name="Flexural modulus (GPa)", max_length=30, null=True, blank=True)
    modulusElasticity = models.CharField(verbose_name="Modulus of elasticity (GPa) (tensile)", max_length=30, null=True, blank=True)
    tensileStrength = models.CharField(verbose_name="Tensile strength (MPa)", max_length=30, null=True, blank=True)
    elongationBreak = models.CharField(verbose_name="Elongation at break (%)", max_length=30, null=True, blank=True)
    compressionUltStrength = models.CharField(verbose_name="Compression ult. strength (MPa)", max_length=30, null=True, blank=True)
    compressionModulus = models.CharField(verbose_name="Compression modulus (GPa)", max_length=30, null=True, blank=True)
    thermalExpansionCoefficient = models.CharField(verbose_name="Thermal expansion coefficient (ppm/K)", max_length=30, null=True, blank=True)
    charpyimpact = models.CharField(verbose_name="Charpy impact at RT (mJ/mm²)", max_length=30, null=True, blank=True)
    fractureToughness = models.CharField(verbose_name="Fracture toughness K1C (Mpa.m1/2)", max_length=30, null=True, blank=True)
    fractureEnergy = models.CharField(verbose_name="Fracture energy G1C (J/m²)", max_length=30, null=True, blank=True)
    totalShrinkage = models.CharField(verbose_name="Total shrinkage at RT (Vol%)", max_length=30, null=True, blank=True)
    hardness = models.CharField(verbose_name="Hardness at RT", max_length=30, null=True, blank=True)
    waterAbsorption = models.CharField(verbose_name="Water absorption (7d at 23°C)", max_length=30, null=True, blank=True)
    valid = models.BooleanField(verbose_name="Validation", default=False)
    
    def __str__(self):
        return f"{self.resin} / {self.hardener}"

class Fiber(models.Model):
    """ Fiber Table """
    material = models.CharField(verbose_name="Material", max_length=30)
    manufacturer = models.CharField(verbose_name="Manufacturer", max_length=30, null=True, blank=True)    
    distributor = models.CharField(verbose_name="Distributor", max_length=50, null=True, blank=True)
    grade = models.CharField(verbose_name="Grade", max_length=50, null=True, blank=True)
    singleFilamentDiameter = models.FloatField(verbose_name="Single filament diameter (mm)", null=True, blank=True)
    tow = models.CharField(verbose_name="Tow", max_length=255, null=True, blank=True)
    towInThousands = models.IntegerField(verbose_name="Tow (in thousands)", null=True, blank=True)
    tex = models.IntegerField(verbose_name="Tex (g/km)", null=True, blank=True)

    density = models.FloatField(verbose_name="Density (g/cm3)", null=True, blank=True)
    theoreticalDrySection = models.CharField(verbose_name="Theoretical dry section (mm2)", max_length=30, null=True, blank=True)
    tensileStrength = models.CharField(verbose_name="Tensile strength (MPa)", max_length=30, null=True, blank=True)
    tensileModulus = models.CharField(verbose_name="Tensile modulus (GPa)", max_length=30, null=True, blank=True)

    price21 = models.CharField(verbose_name="Price euros/kg (2021 to febrary 2022)", max_length=30, null=True, blank=True)
    price22 = models.CharField(verbose_name="Price euros/kg (after 02/2022)", max_length=30, null=True, blank=True)
    price23 = models.CharField(verbose_name="Price euros/kg (after 02/2023)", max_length=30, null=True, blank=True)
    price24 = models.CharField(verbose_name="Price euros/kg (after 01/2024)", max_length=30, null=True, blank=True)
    valid = models.BooleanField(verbose_name="Validation", default=False)

    
    def __str__(self):
        return self.grade

class R_and_D(models.Model):
    """ R&D Table """
    program = models.CharField(verbose_name="Program ", max_length=50)
    projectNr = models.CharField(verbose_name="Project Nr. ", max_length=50)

    ERMDS = models.CharField(verbose_name="ERMDS Nr. ", max_length=50)
    lastUpdate = models.CharField(verbose_name="Last update ", max_length=50, null=True, blank=True)
    verifiedBy = models.CharField(verbose_name="Verified by", max_length=50, null=True, blank=True)
    approvedBy = models.CharField(verbose_name="Approved by ", max_length=50, null=True, blank=True)

    fiber = models.ForeignKey(verbose_name="Fiber", to=Fiber, on_delete=models.CASCADE, to_field='id')
    numberOfBobbins = models.IntegerField(verbose_name="Number of bobbins", null=True, blank=True)
    resin = models.ForeignKey(verbose_name="Resin", to=Resin, on_delete=models.CASCADE, to_field='id')

    endEffector = models.CharField(verbose_name="End-effector N°", max_length=30, null=True, blank=True)
    impregnationBath = models.CharField(verbose_name="Impregnation bath", max_length=30, null=True, blank=True)
    entryNozzleDiam = models.CharField(verbose_name="Entry nozzle diameter (mm)", max_length=30, null=True, blank=True)
    exitNozzleDiam = models.CharField(verbose_name="Exit nozzle diameter (mm)", max_length=30, null=True, blank=True)

    roomTemperature = models.CharField(verbose_name="Room temperature (°C)", max_length=30, null=True, blank=True)
    roomhumidity = models.CharField(verbose_name="Room humidity (%)", max_length=30, null=True, blank=True)

    brakeForcebobin = models.CharField(verbose_name="Brake force/bobbin (N) (kg) (bar)", max_length=30, null=True, blank=True)
    windingSpeedRange = models.CharField(verbose_name="Windng speed range (mm/s)", max_length=30, null=True, blank=True)

    FVR = models.CharField(verbose_name="FVR (%)", max_length=30, null=True, blank=True)
    compositeDensity = models.CharField(verbose_name="Composite density ρ (g/cm3)", max_length=30, null=True, blank=True)
    porosity = models.CharField(verbose_name="Porosity (%)", max_length=30, null=True, blank=True)
    theoreticalSampleSection = models.CharField(verbose_name="Theoretical sample section (mm²)", max_length=30, null=True, blank=True)
    experimentalSampleSection = models.CharField(verbose_name="Experimental sample section (mm²)", max_length=30, null=True, blank=True)
    aged = models.CharField(verbose_name="Aged / Non-aged", max_length=30, null=True, blank=True)
    temperatureOfTests = models.CharField(verbose_name="Temperature of the tests", max_length=30, null=True, blank=True)

    numberOfSamples = models.CharField(verbose_name="Number of samples", max_length=30, null=True, blank=True)
    configurarion = models.CharField(verbose_name="Configuration", max_length=30, null=True, blank=True)
    sampleLength = models.CharField(verbose_name="Sample length", max_length=30, null=True, blank=True)
    numberOfCycles = models.CharField(verbose_name="Number of cycles", max_length=30, null=True, blank=True)
    sleeve = models.CharField(verbose_name="Sleeve diameter / height (mm)", max_length=30, null=True, blank=True)

    thermalExpansionCoefficient = models.CharField(verbose_name="Thermal expansion coefficient A (/K)", max_length=30, null=True, blank=True)
    thermalConductivity = models.CharField(verbose_name="Thermal conductivity K (W/(m.K))", max_length=30, null=True, blank=True)

    tensileYoungModulus = models.FloatField(verbose_name="Tensile Young's modulus - Average (MPa)", null=True, blank=True)
    tensileUltimateStress = models.FloatField(verbose_name="Tensile Ultimate Stress - Average (MPa)", null=True, blank=True)
    tensileUltimateStressMA = models.FloatField(verbose_name="Tensile Ultimate Stress - Min A (MPa)", null=True, blank=True)
    tensileUltimateStressMB = models.FloatField(verbose_name="Tensile Ultimate Stress - Min B (MPa)", null=True, blank=True)
    tensileUltimateLoad = models.FloatField(verbose_name="Tensile Ultimate Load - Average (kN)", null=True, blank=True)
    tensileYieldStress = models.FloatField(verbose_name="Tensile Yield Stress - Average (MPa)", null=True, blank=True)
    tensileYieldStressMA = models.FloatField(verbose_name="Tensile Yield Stress - Min A (MPa)", null=True, blank=True)
    tensileYieldStressMB = models.FloatField(verbose_name="Tensile Yield Stress - Min B (MPa)", null=True, blank=True)
    tensileYieldLoad = models.FloatField(verbose_name="Tensile Yield Load - Average (kN)", null=True, blank=True)

    compressionYoungModulus = models.FloatField(verbose_name="Compression Young's modulus - Average (MPa)", null=True, blank=True)
    compressionUltimateStress = models.FloatField(verbose_name="Compression Ultimate Stress - Average (MPa)", null=True, blank=True)
    compressionUltimateStressMA = models.FloatField(verbose_name="Compression Ultimate Stress - Min A (MPa)", null=True, blank=True)
    compressionUltimateStressMB = models.FloatField(verbose_name="Compression Ultimate Stress - Min B (MPa)", null=True, blank=True)
    compressionUltimateLoad = models.FloatField(verbose_name="Compression Ultimate Load - Average (kN)", null=True, blank=True)
    compressionYieldStress = models.FloatField(verbose_name="Compression Yield Stress- Average (MPa)", null=True, blank=True)
    compressionYieldStressMA = models.FloatField(verbose_name="Compression Yield Stress - Min A (MPa)", null=True, blank=True)
    compressionYieldStressMB = models.FloatField(verbose_name="Compression Yield Stress - Min B (MPa)", null=True, blank=True)
    compressionYieldLoad = models.FloatField(verbose_name="Compression Yield Load - Average (kN)", null=True, blank=True)
    poissonRatio = models.FloatField(verbose_name="Poisson's ratio ν (-)", null=True, blank=True)

    flexuralModulusILSS = models.FloatField(verbose_name="Flexural modulus - Average (MPa)", null=True, blank=True)
    ultimateShearForce = models.FloatField(verbose_name="Ultimate Shear Force - Average (kN)", null=True, blank=True)
    ultimateShearStress = models.FloatField(verbose_name="Ultimate Shear Stress - Average (MPa)", null=True, blank=True)
    ultimateShearStressMA = models.FloatField(verbose_name="Ultimate Shear Stress - Min A (MPa)", null=True, blank=True)
    ultimateShearStressMB = models.FloatField(verbose_name="Ultimate Shear Stress - Min B (MPa)", null=True, blank=True)

    flexuralModulusF = models.FloatField(verbose_name="Flexural modulus - Average (MPa)", null=True, blank=True)
    flexuralUltimateStrength = models.FloatField(verbose_name="Flexural Ultimate strength - Average (MPa)", null=True, blank=True)
    flexuralUltimateStrengthMA = models.FloatField(verbose_name="Flexural Ultimate strength - Min A (MPa)", null=True, blank=True)
    flexuralUltimateStrengthMB = models.FloatField(verbose_name="Flexural Ultimate strength - Min B (MPa)", null=True, blank=True)
    strainUltimateStrength = models.FloatField(verbose_name="Strain at ultimate strength (%)", null=True, blank=True)
    flexuralUltimateForce = models.FloatField(verbose_name=" Flexural Ultimate Force (N)", null=True, blank=True)

    yieldTorque = models.FloatField(verbose_name="Yield Torque (Nm)", null=True, blank=True)
    maxiTorque = models.FloatField(verbose_name="Maxi Torque (Nm)", null=True, blank=True)
    yieldAngle = models.FloatField(verbose_name="Yield angle (°)", null=True, blank=True)
    maxiTwistedAngle = models.FloatField(verbose_name="Maxi Twisted Angle (°)", null=True, blank=True)

  
    fiberC = models.TextField(null=True, blank=True)
    numberOfBobbinsC = models.TextField(null=True, blank=True)
    resinC = models.TextField(null=True, blank=True)
    hardenerC = models.TextField(null=True, blank=True)
    curingCycleC = models.TextField(null=True, blank=True)
   
    towC = models.TextField(null=True, blank=True)
    texC = models.TextField(null=True, blank=True)
    fiberDensityC = models.TextField(null=True, blank=True)
    resinDensityC = models.TextField(null=True, blank=True)
    
    endEffectorC = models.TextField(null=True, blank=True)
    impregnationBathC = models.TextField(null=True, blank=True)
    entryNozzleDiamC = models.TextField(null=True, blank=True)
    exitNozzleDiamC = models.TextField(null=True, blank=True)

    roomTemperatureC = models.TextField(null=True, blank=True)
    roomhumidityC = models.TextField(null=True, blank=True)

    brakeForcebobinC = models.TextField(null=True, blank=True)
    windingSpeedRangeC = models.TextField(null=True, blank=True)

    FVRC = models.TextField(null=True, blank=True)
    compositeDensityC = models.TextField(null=True, blank=True)
    porosityC = models.TextField(null=True, blank=True)
    theoreticalSampleSectionC = models.TextField(null=True, blank=True)
    experimentalSampleSectionC = models.TextField(null=True, blank=True)
    agedC = models.TextField(null=True, blank=True)
    temperatureOfTestsC = models.TextField(null=True, blank=True)

    numberOfSamplesC = models.TextField(null=True, blank=True)
    configurarionC = models.TextField(null=True, blank=True)
    sampleLengthC = models.TextField(null=True, blank=True)
    numberOfCyclesC = models.TextField(null=True, blank=True)
    sleeveC = models.TextField(null=True, blank=True)

    thermalExpansionCoefficientC = models.TextField(null=True, blank=True)
    thermalConductivityC = models.TextField(null=True, blank=True)

    tensileYoungModulusC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileUltimateStressC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileUltimateStressMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileUltimateStressMBC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileUltimateLoadC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileYieldStressC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileYieldStressMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileYieldStressMBC = models.TextField(default="Samples number: ", null=True, blank=True)
    tensileYieldLoadC = models.TextField(default="Samples number: ", null=True, blank=True)

    compressionYoungModulusC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionUltimateStressC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionUltimateStressMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionUltimateStressMBC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionUltimateLoadC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionYieldStressC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionYieldStressMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionYieldStressMBC = models.TextField(default="Samples number: ", null=True, blank=True)
    compressionYieldLoadC = models.TextField(default="Samples number: ", null=True, blank=True)
    poissonRatioC = models.TextField(default="Samples number: ", null=True, blank=True)

    flexuralModulusILSSC = models.TextField(default="Samples number: ", null=True, blank=True)
    ultimateShearForceC = models.TextField(default="Samples number: ", null=True, blank=True)
    ultimateShearStressC = models.TextField(default="Samples number: ", null=True, blank=True)
    ultimateShearStressMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    ultimateShearStressMBC = models.TextField(default="Samples number: ", null=True, blank=True)

    flexuralModulusFC = models.TextField(default="Samples number: ", null=True, blank=True)
    flexuralUltimateStrengthC = models.TextField(default="Samples number: ", null=True, blank=True)
    flexuralUltimateStrengthMAC = models.TextField(default="Samples number: ", null=True, blank=True)
    flexuralUltimateStrengthMBC = models.TextField(default="Samples number: ", null=True, blank=True)
    strainUltimateStrengthC = models.TextField(default="Samples number: ", null=True, blank=True)
    flexuralUltimateForceC = models.TextField(default="Samples number: ", null=True, blank=True)

    yieldTorqueC = models.TextField(default="Samples number: ", null=True, blank=True)
    maxiTorqueC = models.TextField(default="Samples number: ", null=True, blank=True)
    yieldAngleC = models.TextField(default="Samples number: ", null=True, blank=True)
    maxiTwistedAngleC = models.TextField(default="Samples number: ", null=True, blank=True)
    valid = models.BooleanField(verbose_name="Validation", default=False)
    # def __str__(self):
    #     return f"{self.program} / {self.projectNr} / {self.ERMDS}" 
    def __str__(self):
        return self.ERMDS 

    


class Project(models.Model):
    """ ProjectTable """
    projectName = models.CharField(verbose_name="Project Name", max_length=128, unique= True)
    program = models.CharField(verbose_name="Program", max_length=128, null=True, blank=True)
    equipment = models.CharField(verbose_name="Equipment", max_length=128, null=True, blank=True)
    customer = models.CharField(verbose_name="Customer", max_length=128, null=True, blank=True)
    projectNo = models.CharField(verbose_name="Project No", max_length=128, null=True, blank=True)
    # partsNumber = models.PositiveIntegerField(verbose_name="Number of Parts", default=0, null=True, blank=True)


    relativeDesign = models.CharField(verbose_name="Relative Design", max_length=50, null=True, blank=True)
    structureDrawingNb = models.CharField(verbose_name="Structure Drawing Nb", max_length=50, null=True, blank=True)
    documentNb = models.CharField(verbose_name="Document Nr", max_length=50, null=True, blank=True)
    revision = models.CharField(verbose_name="Revision", max_length=50, null=True, blank=True)
    lastUpdate = models.DateField(verbose_name="Last Update M/D/Y", null=True, blank=True)
    valid = models.BooleanField(verbose_name="Validation", default=False)

    def __str__(self):
        return self.projectName

class Part(models.Model):
    """ PartTable """
    ########   1   ########
    partName = models.CharField(verbose_name="Part Name", max_length=128)
    fiber = models.ForeignKey(verbose_name="Fiber Name", to=Fiber, on_delete=models.CASCADE, to_field='id')

    resin = models.ForeignKey(verbose_name="Resin Name", to=Resin, on_delete=models.CASCADE, to_field='id')
    # resinName = models.CharField(verbose_name="Resin Name", max_length=50, null=True, blank=True)
    # resinDensity = models.FloatField(verbose_name="", null=True, blank=True)
    # fiberName = models.CharField(verbose_name="FiberName", max_length=50, null=True, blank=True)
    totalTowNumber = models.IntegerField(verbose_name="Number of Spools", null=True, blank=True)
    # fiberDensity = models.FloatField(verbose_name="Fiber Density[kg/m^3]", null=True, blank=True)

    fiberVolumeRatio = models.FloatField(verbose_name="Fiber Volume Ratio[%]", null=True, blank=True)

    # windingDensity = models.FloatField(verbose_name="Winding Density[kg/m^3]", null=True, blank=True)
    fiberSectionCalc = models.FloatField(verbose_name="Fiber Section calc.[mm²]", null=True, blank=True)
    fiberSectionAcc = models.FloatField(verbose_name="Fiber Section acc.[mm²]", null=True, blank=True)

    defaultInterfaceHeight = models.IntegerField(verbose_name="Default Interface Height[mm]", null=True, blank=True)
    defaultInterfaceIntDiam = models.IntegerField(verbose_name="Default Interface Int. Diam.[mm]", null=True, blank=True)
    defaultLinkType = models.CharField(verbose_name="Default Link(Element) Type", max_length=30, null=True, blank=True)
    defaultLinkDefined = models.CharField(verbose_name="Default Link defined by", max_length=30, null=True, blank=True)


    ########   2   ########
    # numberLink = models.IntegerField(verbose_name="Number of Links", null=True, blank=True)
    # numberBushing = models.IntegerField(verbose_name="Number of Bushings", null=True, blank=True)

    # totalMassLink = models.FloatField(verbose_name="Total Mass of Links[g]", null=True, blank=True)
    # totalMassAccumulation = models.FloatField(verbose_name="Total Mass of Accumulation[g]", null=True, blank=True)
    # totalMassWinding = models.FloatField(verbose_name="Total Mass of Winding[g]", null=True, blank=True)
    # totalMassBushing = models.FloatField(verbose_name="Total Mass of Bushings[g]", null=True, blank=True)
    additionalMass = models.FloatField(verbose_name="Additional Masses[g]", null=True, blank=True)
    # totalMassStructure = models.FloatField(verbose_name="Total Mass of Structure[g]", null=True, blank=True)

    # totalFiberLength = models.FloatField(verbose_name="Total Fiber Length[m]", null=True, blank=True)
    # totalFiberMass = models.FloatField(verbose_name="Total Fiber Mass[kg]", null=True, blank=True)
    # totalResinMass = models.FloatField(verbose_name="Total Resin Mass[g]", null=True, blank=True)

    projectImage = models.ImageField(upload_to='images/', verbose_name="Project Image", null=True, blank=True)


    ########   3   ########
    part_gh = models.CharField(verbose_name="Document.gh", max_length=50, null=True, blank=True)
    part_mod = models.CharField(verbose_name="Document.mod", max_length=50, null=True, blank=True)
    part_csv = models.CharField(verbose_name="Document.csv", max_length=50, null=True, blank=True)
    part_rs = models.CharField(verbose_name="Document.rs", max_length=50, null=True, blank=True)
    part_log = models.CharField(verbose_name="Document.log", max_length=50, null=True, blank=True)
    part_mp4 = models.CharField(verbose_name="Document.mp4", max_length=50, null=True, blank=True)
    part_jpg = models.CharField(verbose_name="Document.jpg", max_length=50, null=True, blank=True)


    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    # project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE)
    valid = models.BooleanField(verbose_name="Validation", default=False)

    def __str__(self):
        return self.partName
    
    @property
    def fiberDensity(self):
        return self.calculate_fiberDensity()
    
    @property
    def resinDensity(self):
        return self.calculate_resinDensity()
    
    @property
    def windingDensity(self):
        return self.calculate_windingDensity()

    @property
    def numberLink(self):
        return self.calculate_numberLink()

    @property
    def numberBushing(self):
        return self.calculate_numberBushing()

    @property
    def totalMassLink(self):
        return self.calculate_totalMassLink()

    @property
    def totalMassAccumulation(self):
        return self.calculate_totalMassAccumulation()

    @property
    def totalMassWinding(self):
        return self.calculate_totalMassWinding()

    @property
    def totalMassBushing(self):
        return self.calculate_totalMassBushing()

    @property
    def totalMassStructure(self):
        return self.calculate_totalMassStructure()

    @property
    def totalFiberLength(self):
        return self.calculate_totalFiberLength()

    @property
    def totalFiberMass(self):
        return self.calculate_totalFiberMass()

    @property
    def totalResinMass(self):
        return self.calculate_totalResinMass()

    def calculate_fiberDensity(self):
        if self.fiber.density:
            return self.fiber.density  * 1000
        return 0.0
    
    def calculate_resinDensity(self):
        if self.resin.densityR :
            return self.resin.densityR * 1000
        return 0.0
    
    def calculate_windingDensity(self):
        if self.fiberDensity and self.fiberVolumeRatio and self.resinDensity and self.fiberVolumeRatio:
            return (self.fiberDensity * self.fiberVolumeRatio + self.resinDensity * (1 - self.fiberVolumeRatio))
        return 0.0

    def calculate_numberLink(self):
        return Link.objects.filter(part=self).count()

    def calculate_numberBushing(self):
        return Bushing.objects.filter(part=self).count()

    def calculate_totalMassLink(self):
        links = Link.objects.filter(part=self)
        total_mass = sum(link.mass for link in links)
        return round(total_mass, 2)
        # total_mass = 0
        # if Link.objects.filter(part=self):
        #     links = Link.objects.filter(part=self)
        #     for link in links:
        #         total_mass += link.mass
        # return round(total_mass,2)

    def calculate_totalMassAccumulation(self):
        interfaces = Interface.objects.filter(part=self)
        total_accumulation = sum(interface.accMass for interface in interfaces if interface.accMass is not None)
        return round(total_accumulation, 2)
        # total_accumulation = 0
        # if Interface.objects.filter(part=self):
        #     interfaces = Interface.objects.filter(part=self)
        #     # print(interfaces)
        #     for interface in interfaces:
        #         total_accumulation += interface.accMass
        #         # print(total_accumulation)
        # return round(total_accumulation,2)

    def calculate_totalMassWinding(self):
        if self.totalMassLink and self.totalMassAccumulation:
            return round(self.totalMassLink + self.totalMassAccumulation,2)
        return 0

    def calculate_totalMassBushing(self):
        bushings = Bushing.objects.filter(part=self)
        total_mass = sum(bushing.bushingMass for bushing in bushings if bushing.bushingMass is not None)
        return round(total_mass, 2)
        # total_mass = 0
        # if Bushing.objects.filter(part=self):
        #     bushings = Bushing.objects.filter(part=self)
        #     for bushing in bushings:
        #         if bushing.bushingMass:
        #             total_mass += bushing.bushingMass
        # return round(total_mass,2)

    def calculate_totalMassStructure(self):
        totalMassStructure = 0
        if self.totalMassWinding and self.totalMassBushing and self.additionalMass:
            totalMassStructure = self.totalMassWinding + self.totalMassBushing + self.additionalMass
        elif self.totalMassWinding and self.totalMassBushing:
            totalMassStructure = self.totalMassWinding + self.totalMassBushing
        return round(totalMassStructure,2)

    def calculate_totalFiberLength(self):
        total_length = 0
        if self.totalMassAccumulation and self.totalMassLink and self.windingDensity and self.fiberSectionAcc and self.fiberSectionCalc:
            mass = self.totalMassAccumulation + self.totalMassLink
            total_length = mass / (self.windingDensity * (self.fiberSectionAcc + self.fiberSectionCalc)/2)*1000
        return round(total_length,2)

    def calculate_totalFiberMass(self):
        fiber_mass = 0
        if self.totalMassAccumulation and self.totalMassLink and self.windingDensity and self.fiberVolumeRatio and self.fiberDensity:
            mass = self.totalMassAccumulation + self.totalMassLink
            fiber_mass = mass / self.windingDensity * self.fiberVolumeRatio * self.fiberDensity / 1000
        return round(fiber_mass,3)

    def calculate_totalResinMass(self):
        resin_mass = 0
        if self.totalMassAccumulation and self.totalMassLink and self.windingDensity and self.fiberVolumeRatio and self.resinDensity:
            mass = self.totalMassAccumulation + self.totalMassLink
            resin_mass = mass / self.windingDensity * (1 - self.fiberVolumeRatio) * self.resinDensity
        return round(resin_mass,2)

class Bushing(models.Model):
    """ BushingTable """
    ########   1   ########
    bushingName = models.CharField(verbose_name="Bushing Name", max_length=30)

    numberInterface = models.IntegerField(verbose_name="Number of Interface", null=True, blank=True)

    bushingDrawNb = models.CharField(verbose_name="Bushing Draw. Nb", max_length=30, null=True, blank=True)
    # AccOnBushing = models.FloatField(verbose_name="Acc. On Bushing[g]", null=True, blank=True)
    bushingMass = models.FloatField(verbose_name="Bushing Mass[g]", null=True, blank=True)
    # totalBushingMass = models.FloatField(verbose_name="Total Bushing Mass[g]", null=True, blank=True)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE,  to_field='id')
    # valid = models.BooleanField(verbose_name="Validation", default=False)

    def __str__(self):
        return self.bushingName
    
    @property
    def AccOnBushing(self):
        return self.calculate_AccOnBushing()

    @property
    def totalBushingMass(self):
        return self.calculate_totalBushingMass()

    def calculate_AccOnBushing(self):
        if(Interface.objects.filter(part=self.part, interfaceName__startswith=self.bushingName + '.')):
            interfaces = Interface.objects.filter(part=self.part, interfaceName__startswith=self.bushingName + '.')
            total_acc_mass = sum(interface.accMass for interface in interfaces if interface.accMass is not None)
            return round(total_acc_mass, 2)
        return 0.0
    
    def calculate_totalBushingMass(self):
        acc_on_bushing = self.AccOnBushing
        total_mass = acc_on_bushing + (self.bushingMass if self.bushingMass else 0)
        return round(total_mass, 2)


class Interface(models.Model):
    """ InterfaceTable """
    ########   2   ########
    interfaceName = models.CharField(verbose_name="Interface Name", max_length=30)

    height = models.IntegerField(verbose_name="Height[mm]", null=True, blank=True)
    intDiameter = models.IntegerField(verbose_name="Int. Diameter[mm]", null=True, blank=True)
    # totalLink = models.IntegerField(verbose_name="Total Link", null=True, blank=True)
    # totalArm = models.IntegerField(verbose_name="Total Arm", null=True, blank=True)

    # totalSection = models.FloatField(verbose_name="Total Section[mm²]", null=True, blank=True)
    # extDiameter = models.FloatField(verbose_name="Ext. Diameter[mm]", null=True, blank=True)
    # theoHeight = models.FloatField(verbose_name="Theo. Height[mm]", null=True, blank=True)
    # accMass = models.FloatField(verbose_name="Acc. Mass[g]", null=True, blank=True)
    finODiam = models.FloatField(verbose_name="Fin. O. Diam.[mm]", null=True, blank=True)
    finAccSection = models.FloatField(verbose_name="Fin. Acc. Section[mm²]", null=True, blank=True)

    # safetyFactor = models.IntegerField(verbose_name="Safety Factor[%]", null=True, blank=True)

    interfaceCenterX = models.FloatField(verbose_name="Interface Center X", null=True, blank=True)
    interfaceCenterY = models.FloatField(verbose_name="Interface Center Y", null=True, blank=True)
    interfaceCenterZ = models.FloatField(verbose_name="Interface Center Z", null=True, blank=True)
    directionVectorX = models.FloatField(verbose_name="Direction Vector X", null=True, blank=True)
    directionVectorY = models.FloatField(verbose_name="Direction Vector Y", null=True, blank=True)
    directionVectorZ = models.FloatField(verbose_name="Direction Vector Z", null=True, blank=True)

    ########   3   ########
    divisionStep = models.IntegerField(verbose_name="Division Step", null=True, blank=True)
    # valid = models.BooleanField(verbose_name="Validation", default=False)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE,  to_field='id')
    # bushing = models.ForeignKey(verbose_name="Bushing Name", to=Bushing, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return self.interfaceName
    
    @property
    def totalLink(self):
        return self.calculate_totalLink()

    @property
    def totalArm(self):
        return self.calculate_totalArm()
    
    @property
    def totalSection(self):
        return self.calculate_totalSection()

    @property
    def extDiameter(self):
        return self.calculate_extDiameter()

    @property
    def accMass(self):
        return self.calculate_accMass()
    
    @property
    def totalSectionShow(self):
        return round(self.totalSection,2)

    @property
    def extDiameterShow(self):
        if isinstance(self.extDiameter, (int, float)):
            return round(self.extDiameter, 2)
        return "--"
        

    @property
    def accMassShow(self):
        return round(self.accMass,2)
    
    @property
    def safetyFactor(self):
        return self.calculate_safetyFactor()


    def calculate_totalLink(self):
        return Link.objects.filter(models.Q(interface1=self) | models.Q(interface2=self)).count()

    
    def calculate_totalArm(self):
        tot_arm = 0
        links = Link.objects.filter(models.Q(interface1=self) | models.Q(interface2=self))
        for link in links:
            if link.sequence:
                if link.sequence == "A":
                    tot_arm = tot_arm + 1
                    
                elif link.sequence == "B":
                    tot_arm = tot_arm + 2
                        
                elif ("C0" in link.sequence) or ("C1" in link.sequence) or ("B" in link.sequence) or ("C1X" in link.sequence) or ("C0X" in link.sequence):
                    tot_arm = tot_arm + 2

        return tot_arm
    
    def calculate_totalSection(self):
        tot_sec_lnk = 0
        tot_sec_acc = 0
        total_sec = 0
        links = Link.objects.filter(models.Q(interface1=self) | models.Q(interface2=self))
        if self.part.fiberSectionAcc:
            for link in links:
                if link.cycle and link.ratio:
                    link_final_section = link.cycle * self.part.fiberSectionAcc

                    if link.sequence == "A":
                        tot_sec_lnk = tot_sec_lnk + link_final_section 
                        
                    elif link.sequence == "B":
                        tot_sec_lnk = tot_sec_lnk + link_final_section
                        tot_sec_acc = tot_sec_acc + link_final_section
                            
                    elif ("C0" in link.sequence) or ("C1" in link.sequence) or ("B" in link.sequence) or ("C1X" in link.sequence) or ("C0X" in link.sequence):
                        ratio = link.ratio
                        tot_sec_acc = tot_sec_acc + link_final_section * ratio 
                        tot_sec_lnk = tot_sec_lnk + link_final_section
        total_sec = tot_sec_acc + tot_sec_lnk
        return total_sec

    def calculate_extDiameter(self):
        if self.height and self.intDiameter and self.height != 0:
            if self.totalSection!=0:
                ext_diam = self.intDiameter + 2 * self.totalSection / self.height
                return ext_diam
        return "--"

    def calculate_accMass(self):
        total_sec_acc = 0
        links = Link.objects.filter(models.Q(interface1=self) | models.Q(interface2=self))
        if self.part.fiberSectionAcc:
            for link in links:
                if link.cycle and link.ratio:
                    link_final_section = link.cycle * self.part.fiberSectionAcc

                    if link.sequence == "B":
                        total_sec_acc = total_sec_acc + link_final_section
                            
                    elif ("C0" in link.sequence) or ("C1" in link.sequence) or ("B" in link.sequence) or ("C1X" in link.sequence) or ("C0X" in link.sequence):
                        ratio = link.ratio
                        total_sec_acc = total_sec_acc + link_final_section * ratio 

        if self.height and self.intDiameter and self.height != 0 and self.part.fiberSectionAcc and self.part.fiberSectionCalc:
            total_sec = self.totalSection
            
            if total_sec!=0 and self.part.windingDensity :
                diam_acc_max = self.intDiameter + 2 * total_sec / self.height
                diam_acc_min = self.intDiameter + 2 * total_sec_acc / self.height
                diam_acc_mass_max = self.intDiameter + 2 * (total_sec / self.part.fiberSectionAcc * ((self.part.fiberSectionAcc+self.part.fiberSectionCalc) / 2)) / self.height
                # print(diam_acc_mass_max)
                diam_acc_mass_min = self.intDiameter + 2 * (total_sec_acc / self.part.fiberSectionAcc * ((self.part.fiberSectionAcc+self.part.fiberSectionCalc) / 2 ))/ self.height 
                # print(diam_acc_mass_min)
                acc_mass = ((diam_acc_mass_max ** 2) / 8 + (diam_acc_mass_min ** 2) / 8 - (self.intDiameter ** 2)/4) * math.pi * self.height * self.part.windingDensity / 1000000
                return acc_mass
        return 0.0

    def calculate_safetyFactor(self):
        if self.finODiam:
            if self.intDiameter and isinstance(self.extDiameter, (int, float)):
                return str(round((self.finODiam - self.intDiameter) / (self.extDiameter - self.intDiameter)*100))+"%"
        elif self.finAccSection:
            if self.totalSection:
                return str(round(self.finAccSection / self.totalSection))+"%"
        return "--"
    
class Link(models.Model):
    """ InterfaceTable """
    ########   2   ########
    linkName = models.CharField(verbose_name="Link Name", max_length=30)
    interface1 = models.ForeignKey(Interface, related_name='link_interface1', on_delete=models.CASCADE)
    interface2 = models.ForeignKey(Interface, related_name='link_interface2', on_delete=models.CASCADE)
    # length = models.FloatField(verbose_name="Length[mm]", null=True, blank=True, editable=False)
    # linkType = models.CharField(verbose_name="Link Type", max_length=30, null=True, blank=True)
    armDiam = models.FloatField(verbose_name="Arm Diam.[mm]", null=True, blank=True)
    armSection = models.FloatField(verbose_name="Arm Section[mm²]", max_length=30, null=True, blank=True)

    cycle = models.IntegerField(verbose_name="Cycle", null=True, blank=True)
    sequence = models.CharField(verbose_name="Sequence", max_length=50, null=True, blank=True)
    ratio = models.FloatField(verbose_name="Ratio", null=True, blank=True)
    # finArmSection = models.FloatField(verbose_name="Fin. Arm Section[mm²]", null=True, blank=True, editable=False)
    # finArmDiam = models.FloatField(verbose_name="Fin. Arm Diam.[mm]", null=True, blank=True, editable=False)
    # finArmRadius = models.FloatField(verbose_name="Fin. Arm Radius[m]", null=True, blank=True, editable=False)
    # mass = models.FloatField(verbose_name="Mass[g]", null=True, blank=True, editable=False)
    angle = models.FloatField(verbose_name="Angle", null=True, blank=True)
    # valid = models.BooleanField(verbose_name="Validation", default=False)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE, to_field='id')
    # interface = models.ForeignKey(verbose_name="Interface Name", to=Interface, on_delete=models.CASCADE, to_field='id')

    # interface1 = models.ForeignKey(Interface,related_name='link_interface1', on_delete=models.CASCADE)
    # interface2 = models.ForeignKey(Interface,related_name='link_interface2', on_delete=models.CASCADE)

    def __str__(self):
        return self.linkName
    
    @property
    def length(self):
        return self.calculate_length()

    @property
    def finArmSection(self):
        return self.calculate_finArmSection()

    @property
    def finArmDiam(self):
        return self.calculate_finArmDiam()

    @property
    def finArmRadius(self):
        return self.calculate_finArmRadius()

    @property
    def mass(self):
        return self.calculate_mass()
    
    @property
    def lengthShow(self):
        return round(self.length,2)

    @property
    def finArmSectionShow(self):
        return round(self.finArmSection,2)

    @property
    def finArmDiamShow(self):
        return round(self.finArmDiam,2)

    @property
    def finArmRadiusShow(self):
        return round(self.finArmRadius,6)

    @property
    def massShow(self):
        return round(self.mass,2)

    def calculate_length(self):
        if self.interface1 and self.interface2:
            length = math.sqrt(
                (self.interface2.interfaceCenterX - self.interface1.interfaceCenterX) ** 2 +
                (self.interface2.interfaceCenterY - self.interface1.interfaceCenterY) ** 2 +
                (self.interface2.interfaceCenterZ - self.interface1.interfaceCenterZ) ** 2
            )
            return length
        return 0.0

    def calculate_finArmSection(self):
        if self.part.fiberSectionCalc and self.cycle:
            finArmSection = self.part.fiberSectionCalc * self.cycle
            return finArmSection
        return 0.0
    
    def calculate_finArmDiam(self):
        if self.finArmSection:
            finArmDiam = math.sqrt(self.finArmSection * 4 / math.pi)
            return finArmDiam
        return 0.0
    
    def calculate_finArmRadius(self):
        if self.finArmDiam:
            finArmRadius = self.finArmDiam / 2 /1000
            return finArmRadius
        return 0.0
    
    def calculate_mass(self):
        mass = 0
        if self.length and self.finArmSection and self.part.windingDensity:
            if self.sequence == "A":
                mass = float(self.length) * float(self.finArmSection) * float(self.part.fiberDensity)/1000000
            else:
                mass = float(self.length) * float(self.finArmSection) * float(self.part.fiberDensity)/1000000 * 2 
                
            return mass
        return 0.0
                                     
class SequenceType(models.Model):
    """ SequenceTypeTable """
    ########   3   ########
    sequenceType = models.CharField(verbose_name="Sequence Type", max_length=30, unique= True)
    description = models.CharField(verbose_name="Description", max_length=1023, null=True, blank=True)
    valid = models.BooleanField(verbose_name="Validation", default=False)

    def __str__(self):
        return self.sequenceType

class Winding(models.Model):
    """ WindingTable """
    ########   3   ########
    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE, to_field='id')
    # link = models.ForeignKey(verbose_name="Link Name", to=Link, on_delete=models.CASCADE, to_field='id')
    link = models.CharField(verbose_name="Link Name", max_length=30 )
    # interface = models.ForeignKey(verbose_name="Interface Name", to=Interface, on_delete=models.CASCADE, to_field='id')
    # interface1 = models.ForeignKey(Interface, related_name='interface1', on_delete=models.CASCADE, to_field='id')
    # interface2 = models.ForeignKey(Interface, related_name='interface2', on_delete=models.CASCADE, to_field='id')
    interface1 = models.CharField(verbose_name="Interface Start", max_length=30)
    interface2 = models.CharField(verbose_name="Interface Transition", max_length=30)
    interface3 = models.CharField(verbose_name="Interface End", max_length=30)
    # sequence = models.ForeignKey(verbose_name="WindingType Description", to=SequenceType, on_delete=models.CASCADE, to_field='id')
    # valid = models.BooleanField(verbose_name="Validation", default=False)
    def __str__(self):
        return self.link
