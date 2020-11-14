import csv
from object_simulator import ObjectWithConstants


class Reader:
    @classmethod
    def parse_file(cls, filename: str):
        ret_obj = []
        with open(filename) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                owc = ObjectWithConstants()
                owc.m_stud = float(row[0])
                owc.m_chair = float(row[1])
                owc.m_balloon = float(row[2])
                owc.balloon_v = float(row[3])
                owc.ro_balloon = float(row[4])
                owc.balloon_counts = float(row[5])
                owc.h_critical = float(row[6])
                owc.ob_name = row[7]
                ret_obj.append(owc)

        return ret_obj

