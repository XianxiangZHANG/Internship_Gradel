from django.db import models


class Department(models.Model):
    """ DepartmentTable """
    title = models.CharField(verbose_name="title", max_length=16)

    def __str__(self):
        return self.title


class User(models.Model):
    """ UserTable """
    username = models.CharField(verbose_name="Username", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)
    depart = models.ForeignKey(verbose_name="Department", to=Department, on_delete=models.CASCADE)


class Project(models.Model):
    """ ProjectTable """
    projectName = models.CharField(verbose_name="Project Name", max_length=32, unique= True)
    equipment = models.CharField(verbose_name="Equipment", max_length=32, null=True, blank=True)
    customer = models.CharField(verbose_name="Customer", max_length=32, null=True, blank=True)
    projectNo = models.CharField(verbose_name="Project No", max_length=32, null=True, blank=True)
    partsNumber = models.PositiveIntegerField(verbose_name="Parts Number", default=0, null=True, blank=True)


    relativeDesign = models.CharField(verbose_name="Relative Design", max_length=32, null=True, blank=True)
    structureDrawingNb = models.CharField(verbose_name="Structure Drawing Nb", max_length=32, null=True, blank=True)
    documentNb = models.CharField(verbose_name="Document Nr", max_length=32, null=True, blank=True)
    revision = models.CharField(verbose_name="Revision", max_length=32, null=True, blank=True)
    lastUpdate = models.DateTimeField(verbose_name="Last Update M/D/Y", null=True, blank=True)

    def __str__(self):
        # if self.lastUpdate is not None:
        #     formatted_date = self.lastUpdate.strftime("%m-%d-%Y")
        # else:
        #     formatted_date = "N/A"  # 或者其他你想要显示的默认值
        return self.projectName

class Part(models.Model):
    """ PartTable """
    ########   1   ########
    partName = models.CharField(verbose_name="Part Name", max_length=32, unique=True)

    resinName = models.CharField(verbose_name="Resin Name", max_length=32, null=True, blank=True)
    resinDensity = models.FloatField(verbose_name="Resin Density[kg/m^3]", null=True, blank=True)
    fiberName = models.CharField(verbose_name="FiberName", max_length=32, null=True, blank=True)
    totalTowNumber = models.IntegerField(verbose_name="Total Tow Number", null=True, blank=True)
    fiberDensity = models.FloatField(verbose_name="Fiber Density[kg/m^3]", null=True, blank=True)

    fiberVolumeRatio = models.FloatField(verbose_name="Fiber Volume Ratio[%]", null=True, blank=True)

    windingDensity = models.FloatField(verbose_name="Winding Density[kg/m^3]", null=True, blank=True)
    fiberSectionCalc = models.FloatField(verbose_name="Fiber Section calc.[mm^2]", null=True, blank=True)
    fiberSectionAcc = models.FloatField(verbose_name="Fiber Section acc.[mm^2]", null=True, blank=True)

    defaultInterfaceHeight = models.IntegerField(verbose_name="Default Interface Height[mm]", null=True, blank=True)
    defaultInterfaceIntDiam = models.IntegerField(verbose_name="Default Interface Int. Diam.[mm]", null=True, blank=True)
    defaultLinkType = models.CharField(verbose_name="Default Link(Element) Type", max_length=32, null=True, blank=True)
    defaultLinkDefined = models.CharField(verbose_name="Default Link defined by", max_length=32, null=True, blank=True)
    defaultCycleNumber = models.IntegerField(verbose_name="Default Cycle Number", null=True, blank=True)

    tensileYoungModulus = models.FloatField(verbose_name="Tensile Young's Modulus", null=True, blank=True)
    tensileUtimateStress = models.FloatField(verbose_name="Tensile Utimate Stress", null=True, blank=True)
    tensileYieldStress = models.FloatField(verbose_name="Tensile Yield Stress", null=True, blank=True)
    compressionYoungModulus = models.FloatField(verbose_name="Compression Young's Modulus", null=True, blank=True)
    flexuralModulus = models.FloatField(verbose_name="Flexural Modulus", null=True, blank=True)


    ########   2   ########
    numberLink = models.IntegerField(verbose_name="Number of Links", null=True, blank=True)
    numberBushing = models.IntegerField(verbose_name="Number of Bushings", null=True, blank=True)

    totalMassLink = models.FloatField(verbose_name="Total Mass of Links[g]", null=True, blank=True)
    totalMassAccumulation = models.FloatField(verbose_name="Total Mass of Accumulation[g]", null=True, blank=True)
    totalMassWinding = models.FloatField(verbose_name="Total Mass of Winding[g]", null=True, blank=True)
    totalMassBushing = models.FloatField(verbose_name="Total Mass of Bushings[g]", null=True, blank=True)
    additionalMass = models.FloatField(verbose_name="Additional Masses[g]", null=True, blank=True)
    totalMassStructure = models.FloatField(verbose_name="Total Mass of Structure[g]", null=True, blank=True)

    totalFiberLength = models.FloatField(verbose_name="Total Fiber Length[m]", null=True, blank=True)
    totalFiberMass = models.FloatField(verbose_name="Total Fiber Mass[kg]", null=True, blank=True)
    totalResinMass = models.FloatField(verbose_name="Total Resin Mass[g]", null=True, blank=True)

    projectImage = models.FileField(upload_to='uploads/', verbose_name="Project Image", null=True, blank=True)


    ########   3   ########
    part_gh = models.CharField(verbose_name="Document.gh", max_length=32, null=True, blank=True)
    part_mod = models.CharField(verbose_name="Document.mod", max_length=32, null=True, blank=True)
    part_csv = models.CharField(verbose_name="Document.csv", max_length=32, null=True, blank=True)
    part_rs = models.CharField(verbose_name="Document.rs", max_length=32, null=True, blank=True)
    part_log = models.CharField(verbose_name="Document.log", max_length=32, null=True, blank=True)
    part_mp4 = models.CharField(verbose_name="Document.mp4", max_length=32, null=True, blank=True)
    part_jpg = models.CharField(verbose_name="Document.jpg", max_length=32, null=True, blank=True)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    # project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.partName

class Bushing(models.Model):
    """ BushingTable """
    ########   1   ########
    bushingName = models.CharField(verbose_name="Bushing Name", max_length=32)

    numberInterface = models.IntegerField(verbose_name="Number of Interface", null=True, blank=True)

    bushingDrawNb = models.CharField(verbose_name="Bushing Draw. Nb", max_length=32, null=True, blank=True)
    AccOnBushing = models.FloatField(verbose_name="Acc. On Bushing[g]", null=True, blank=True)
    bushingMass = models.FloatField(verbose_name="Bushing Mass[g]", null=True, blank=True)
    totalBushingMass = models.FloatField(verbose_name="Total Bushing Mass[g]", null=True, blank=True)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE,  to_field='id')

    def __str__(self):
        return self.bushingName


class Interface(models.Model):
    """ InterfaceTable """
    ########   2   ########
    interfaceName = models.CharField(verbose_name="Interface Name", max_length=32)

    height = models.IntegerField(verbose_name="Height[mm]", null=True, blank=True)
    intDiameter = models.IntegerField(verbose_name="Int. Diameter[mm]", null=True, blank=True)
    totalLink = models.IntegerField(verbose_name="Total Link", null=True, blank=True)
    totalArm = models.IntegerField(verbose_name="Total Arm", null=True, blank=True)

    totalSection = models.FloatField(verbose_name="Total Section[mm^2]", null=True, blank=True)
    extDiameter = models.FloatField(verbose_name="Ext. Diameter[mm]", null=True, blank=True)
    theoHeight = models.FloatField(verbose_name="Theo. Height[mm]", null=True, blank=True)
    accMass = models.FloatField(verbose_name="Acc. Mass[g]", null=True, blank=True)
    finODiam = models.FloatField(verbose_name="Fin. O. Diam.[mm]", null=True, blank=True)
    finAccSection = models.FloatField(verbose_name="Fin. Acc. Section[mm^2]", null=True, blank=True)

    safetyFactor = models.IntegerField(verbose_name="Safety Factor[%]", null=True, blank=True)

    interfaceCenterX = models.FloatField(verbose_name="Interface Center X", null=True, blank=True)
    interfaceCenterY = models.FloatField(verbose_name="Interface Center Y", null=True, blank=True)
    interfaceCenterZ = models.FloatField(verbose_name="Interface Center Z", null=True, blank=True)
    directionVectorX = models.FloatField(verbose_name="Direction Vector X", null=True, blank=True)
    directionVectorY = models.FloatField(verbose_name="Direction Vector Y", null=True, blank=True)
    directionVectorZ = models.FloatField(verbose_name="Direction Vector Z", null=True, blank=True)

    ########   3   ########
    divisionStep = models.IntegerField(verbose_name="Division Step", null=True, blank=True)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE,  to_field='id')
    # bushing = models.ForeignKey(verbose_name="Bushing Name", to=Bushing, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return self.interfaceName

class Link(models.Model):
    """ InterfaceTable """
    ########   2   ########
    linkName = models.CharField(verbose_name="Link Name", max_length=32)

    length = models.FloatField(verbose_name="Length[mm]", null=True, blank=True)
    linkType = models.CharField(verbose_name="Link Type", max_length=32, null=True, blank=True)
    armDiam = models.FloatField(verbose_name="Arm Diam.[mm]", null=True, blank=True)
    armSection = models.FloatField(verbose_name="Arm Section[mm^2]", max_length=32, null=True, blank=True)

    cycle = models.IntegerField(verbose_name="Cycle", null=True, blank=True)
    sequence = models.CharField(verbose_name="Sequence", max_length=32, null=True, blank=True)
    finArmSection = models.FloatField(verbose_name="Fin. Arm Section[mm^2]", null=True, blank=True)
    finArmDiam = models.FloatField(verbose_name="Fin. Arm Diam.[mm]", null=True, blank=True)
    finArmRadius = models.FloatField(verbose_name="Fin. Arm Radius[m]", null=True, blank=True)
    mass = models.FloatField(verbose_name="Mass[g]", null=True, blank=True)
    angle = models.FloatField(verbose_name="Angle", null=True, blank=True)

    project = models.ForeignKey(verbose_name="Project Name", to=Project, on_delete=models.CASCADE, to_field='id')
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE, to_field='id')
    interface = models.ForeignKey(verbose_name="Interface Name", to=Interface, on_delete=models.CASCADE, to_field='id')

    def __str__(self):
        return self.linkName
                                     
class WindingType(models.Model):
    """ WindingTypeTable """
    ########   3   ########
    description = models.CharField(verbose_name="Description", max_length=32)

class Winding(models.Model):
    """ WindingTable """
    ########   3   ########
    part = models.ForeignKey(verbose_name="Part Name", to=Part, on_delete=models.CASCADE)
    link = models.ForeignKey(verbose_name="Link Name", to=Link, on_delete=models.CASCADE)
    interface = models.ForeignKey(verbose_name="Interface Name", to=Interface, on_delete=models.CASCADE)
    windingType = models.ForeignKey(verbose_name="WindingType Description", to=WindingType, on_delete=models.CASCADE)
