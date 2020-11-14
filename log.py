import time
from prettytable import PrettyTable


class FileLogger:
    def __init__(self, filename: str):
        self._file = open(filename, "w")
        self._time_beg = time.time()
        self._file.write("------LOGGER CREATED------\n")
        self._file.write("Creation time: " + str(self._time_beg)+"\n")
        self._file.write("--------------------------\n")

    def close(self):
        if self._file:
            td = time.time()
            self._file.write("------LOGGER DESTROYING------\n")
            self._file.write("Del time: " + str(td) + "\n")
            self._file.write("Exec time: " + str(td - self._time_beg)+'\n')
            self._file.write("-----------------------------\n")
            self._file.close()
            self._file = None

    def write_arr_to_file(self, arr):
        t = PrettyTable(["#Obj", "m(st)", "m(ch)", "m(bal)", "ct(bal)", "V(bal)", "ro(bal)", "h(crit)"])
        for obj in arr:
            cm = []
            cm.append(obj.ob_name)
            cm.append(obj.m_stud)
            cm.append(obj.m_chair)
            cm.append(obj.m_balloon)
            cm.append(obj.balloon_counts)
            cm.append(obj.balloon_v)
            cm.append(obj.ro_balloon)
            cm.append(obj.h_critical)
            t.add_row(cm)

        self._file.write(str(t)+"\n")

    def write_str(self, str_msg: str):
        self._file.write(str_msg+"\n")

    def write_r_table(self, r_arr, ob_arr):
        headers = ["#"]+[ob.ob_name for ob in ob_arr]
        t = PrettyTable(headers)
        for ct in range(len(r_arr)):
            k = [ob_arr[ct].ob_name, ] + r_arr[ct]
            t.add_row(k)

        self._file.write(str(t)+'\n')


class FileLoggerMock:
    def __init__(self):
        pass

    def close(self):
        pass

    def write_str(self, str_msg: str):
        pass

    def write_arr_to_file(self, arr):
        pass

    def write_r_table(self, r_arr, ob_arr):
        pass