import math, re
from django.db.models import Sum

class PartCalculator:
    def __init__(self, part):
        self.part = part

    @property
    def fiber_density(self):
        return self.part.fiber.density * 1000 if self.part.fiber.density else 0.0

    @property
    def resin_density(self):
        return self.part.resin.densityR * 1000 if self.part.resin.densityR else 0.0

    @property
    def winding_density(self):
        if self.fiber_density and self.part.fiberVolumeRatio and self.resin_density:
            return self.fiber_density * self.part.fiberVolumeRatio + self.resin_density * (1 - self.part.fiberVolumeRatio)
        return 0.0

    def number_link(self):
        return self.part.link_set.count()
    
    def number_bushing(self):
        return self.part.bushing_set.count()

    def total_mass_link(self):
        links = self.part.link_set.all()
        total_mass = sum(LinkCalculator(link).mass() for link in links)
        return round(total_mass, 2)

    def total_mass_accumulation(self):
        interfaces = self.part.interface_set.all()
        total_accumulation = sum(InterfaceCalculator(interface).acc_mass() for interface in interfaces)
        return round(total_accumulation, 2)

    def total_mass_winding(self):
        return round(self.total_mass_link() + self.total_mass_accumulation(), 2)

    def total_mass_bushing(self):
        bushings = self.part.bushing_set.all()
        total_mass = sum(BushingCalculator(bushing).total_bushing_mass() for bushing in bushings)
        return round(total_mass, 2)

    def total_mass_structure(self):
        total_mass_structure = self.total_mass_winding() + self.total_mass_bushing() + (self.part.additionalMass or 0.0)
        return round(total_mass_structure, 2)

    def total_fiber_length(self):
        if self.total_mass_accumulation() and self.total_mass_link() and self.winding_density and self.part.fiberSectionAcc and self.part.fiberSectionCalc:
            mass = self.total_mass_accumulation() + self.total_mass_link()
            total_length = mass / (self.winding_density * (self.part.fiberSectionAcc + self.part.fiberSectionCalc) / 2) * 1000
            return round(total_length, 2)
        return 0.0

    def total_fiber_mass(self):
        if self.total_mass_accumulation() and self.total_mass_link() and self.winding_density and self.part.fiberVolumeRatio and self.fiber_density:
            mass = self.total_mass_accumulation() + self.total_mass_link()
            fiber_mass = mass / self.winding_density * self.part.fiberVolumeRatio * self.fiber_density / 1000
            return round(fiber_mass, 3)
        return 0.0

    def total_resin_mass(self):
        if self.total_mass_accumulation() and self.total_mass_link() and self.winding_density and self.part.fiberVolumeRatio and self.resin_density:
            mass = self.total_mass_accumulation() + self.total_mass_link()
            resin_mass = mass / self.winding_density * (1 - self.part.fiberVolumeRatio) * self.resin_density
            return round(resin_mass, 2)
        return 0.0

class BushingCalculator:
    def __init__(self, bushing):
        self.bushing = bushing

    def acc_on_bushing(self):
        interfaces = self.bushing.part.interface_set.filter(interfaceName__startswith=self.bushing.bushingName + '.')
        total_acc_mass = sum(InterfaceCalculator(interface).acc_mass() for interface in interfaces)
        return round(total_acc_mass, 2)

    def total_bushing_mass(self):
        acc_mass = self.acc_on_bushing()
        return round(acc_mass + (self.bushing.bushingMass if self.bushing.bushingMass else 0), 2)

class InterfaceCalculator:
    def __init__(self, interface):
        self.interface = interface

    def total_link(self):
        return self.interface.link_interface1.count() + self.interface.link_interface2.count()

    def total_arm(self):
        tot_arm = 0
        links = self.interface.link_interface1.all() | self.interface.link_interface2.all()
        for link in links:
            if link.sequence == "A":
                tot_arm += 1
            elif link.sequence == "B":
                tot_arm += 2
            elif any(x in link.sequence for x in ["C0", "C1", "B", "C1X", "C0X"]):
                tot_arm += 2
        return tot_arm

    def total_section(self):
        tot_sec_lnk = 0
        tot_sec_acc = 0
        links = self.interface.link_interface1.all() | self.interface.link_interface2.all()
        if self.interface.part.fiberSectionAcc:
            for link in links:
                if link.cycle and LinkCalculator(link).ratio():
                    link_final_section = link.cycle * self.interface.part.fiberSectionAcc
                    if link.sequence == "A":
                        tot_sec_lnk += link_final_section
                    elif link.sequence == "B":
                        tot_sec_lnk += link_final_section
                        tot_sec_acc += link_final_section
                    elif any(x in link.sequence for x in ["C0", "C1", "B", "C1X", "C0X"]):
                        ratio = LinkCalculator(link).ratio()
                        tot_sec_acc += link_final_section * ratio
                        tot_sec_lnk += link_final_section
        return tot_sec_acc + tot_sec_lnk

    def ext_diameter(self):
        if self.interface.height and self.interface.intDiameter and self.interface.height != 0:
            if self.total_section() != 0:
                return self.interface.intDiameter + 2 * self.total_section() / self.interface.height
        return "--"

    def acc_mass(self):
        total_sec_acc = 0
        links = self.interface.link_interface1.all() | self.interface.link_interface2.all()
        if self.interface.part.fiberSectionAcc:
            for link in links:
                if link.cycle and LinkCalculator(link).ratio():
                    link_final_section = link.cycle * self.interface.part.fiberSectionAcc
                    if link.sequence == "B":
                        total_sec_acc += link_final_section
                    elif any(x in link.sequence for x in ["C0", "C1", "B", "C1X", "C0X"]):
                        ratio = LinkCalculator(link).ratio()
                        total_sec_acc += link_final_section * ratio

        if self.interface.height and self.interface.intDiameter and self.interface.height != 0 and self.interface.part.fiberSectionAcc and self.interface.part.fiberSectionCalc:
            total_sec = self.total_section()
            if total_sec != 0 and PartCalculator(self.interface.part).winding_density:
                diam_acc_mass_max = self.interface.intDiameter + 2 * (total_sec / self.interface.part.fiberSectionAcc * ((self.interface.part.fiberSectionAcc + self.interface.part.fiberSectionCalc) / 2)) / self.interface.height
                diam_acc_mass_min = self.interface.intDiameter + 2 * (total_sec_acc / self.interface.part.fiberSectionAcc * ((self.interface.part.fiberSectionAcc + self.interface.part.fiberSectionCalc) / 2)) / self.interface.height
                return ((diam_acc_mass_max ** 2) / 8 + (diam_acc_mass_min ** 2) / 8 - (self.interface.intDiameter ** 2) / 4) * math.pi * self.interface.height * PartCalculator(self.interface.part).winding_density / 1000000
        return 0.0

    def safety_factor(self):
        if self.interface.finODiam:
            if self.interface.intDiameter and isinstance(self.ext_diameter(), (int, float)):
                return f"{round((self.interface.finODiam - self.interface.intDiameter) / (self.ext_diameter() - self.interface.intDiameter) * 100)}%"
        elif self.interface.finAccSection:
            if self.total_section():
                return f"{round(self.interface.finAccSection / self.total_section())}%"
        return "--"

class LinkCalculator:
    def __init__(self, link):
        self.link = link

    def length(self):
        if self.link.interface1 and self.link.interface2:
            return math.sqrt(
                (self.link.interface2.interfaceCenterX - self.link.interface1.interfaceCenterX) ** 2 +
                (self.link.interface2.interfaceCenterY - self.link.interface1.interfaceCenterY) ** 2 +
                (self.link.interface2.interfaceCenterZ - self.link.interface1.interfaceCenterZ) ** 2
            )
        return 0.0

    def fin_arm_section(self):
        if self.link.part.fiberSectionCalc and self.link.cycle:
            return self.link.part.fiberSectionCalc * self.link.cycle
        return 0.0

    def fin_arm_diam(self):
        if self.fin_arm_section():
            return math.sqrt(self.fin_arm_section() * 4 / math.pi)
        return 0.0

    def fin_arm_radius(self):
        if self.fin_arm_diam():
            return self.fin_arm_diam() / 2 / 1000
        return 0.0

    def mass(self):
        part_calculator = PartCalculator(self.link.part)
        mass = 0
        if self.length() and self.fin_arm_section() and part_calculator.winding_density:
            if self.link.sequence == "A":
                mass = float(self.length()) * float(self.fin_arm_section()) * float(part_calculator.fiber_density) / 1000000
            else:
                mass = float(self.length()) * float(self.fin_arm_section()) * float(part_calculator.fiber_density) / 1000000 * 2
        return mass

    def ratio(self):
        sequence = self.link.sequence.replace('B', 'C1')
        if sequence.startswith('[') and sequence.endswith(']'):
            sequence = sequence[1:-1]

        def expand_sequence(seq):
            pattern = re.compile(r'\[(.*?)\](\d+)')
            while pattern.search(seq):
                seq = re.sub(pattern, lambda m: (m.group(1) + ',') * int(m.group(2)), seq)
            return seq

        expanded_sequence = expand_sequence(sequence)
        substrings = ['C1X', 'C1', 'C0X', 'C0']
        counts = {substring: len(re.findall(substring, expanded_sequence)) for substring in substrings}
        total_c1_c1x = counts['C1X'] + counts['C1']
        total_target = counts['C1X'] + counts['C1'] + counts['C0X'] + counts['C0']
        return round(total_c1_c1x / total_target if total_target > 0 else 0, 2)
