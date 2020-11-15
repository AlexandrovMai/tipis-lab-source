from graph import Graph
from object_simulator import ObjectWithConstants, FlyingObject
from log import FileLogger, FileLoggerMock


class RCounter:

    def __init__(self, log_file: str, graph_file: str):
        self.time_arr = []
        self.a_arr = []
        self.v_arr = []
        self.h_arr = []
        self.b_cnt = []
        self.m_arr = []
        self.graph_file = graph_file
        if log_file is None:
            self.logger = FileLoggerMock()
        else:
            self.logger = FileLogger(log_file)

    def calc(self, ob1: ObjectWithConstants, ob2: ObjectWithConstants):
        self.logger.write_str("Preparing for count: " + ob1.ob_name + " R " + ob2.ob_name)
        ob_logger = ObjectWithConstants()
        ob_logger.ob_name = ob1.ob_name + " R " + ob2.ob_name
        ob_logger.m_stud = ob2.m_stud
        ob_logger.m_chair = ob1.m_chair
        ob_logger.h_critical = ob1.h_critical
        ob_logger.ro_balloon = ob1.ro_balloon
        ob_logger.balloon_v = ob1.balloon_v
        ob_logger.balloon_counts = ob1.balloon_counts
        ob_logger.m_balloon = ob1.m_balloon

        self.logger.write_str(ob1.ob_name + " R " + ob2.ob_name + " parameters:")
        self.logger.write_arr_to_file([ob_logger, ])
        self.logger.write_str("Creating object and preparing for sim")

        is_in_r, cur_p = self._calc(ob_logger)

        self.logger.write_str("IS in R is:" + str(is_in_r))
        if self.graph_file:
            Graph.print_graph(self.a_arr,
                              self.v_arr,
                              self.h_arr,
                              self.b_cnt,
                              self.m_arr,
                              self.time_arr,
                              self.graph_file
                              )
            self.logger.write_str("Graph saved to file " + self.graph_file)
        self.logger.close()
        return is_in_r, cur_p

    def _calc(self, ob_s: ObjectWithConstants):
        fo = FlyingObject(ob_s.create_object_emulator())
        cur_p = None
        is_in_r = False

        for params, iteration in fo:
            self.time_arr.append(params.t)
            self.v_arr.append(params.v)
            self.h_arr.append(params.h)
            self.a_arr.append(params.a)
            self.b_cnt.append(fo.get_balloons())
            self.m_arr.append(fo.get_mass())

            if iteration % 100 == 0:
                self.logger.write_str(str(params))

            if iteration == 280000000 or params.v <= 0.0 or params.h >= 3000:
                cur_p = params
                break

        self.logger.write_str("ITERATION PROCESS STOPPED WITH FOLOWING PARAMS")
        self.logger.write_str(str(cur_p))

        if cur_p.h >= 3000:
            is_in_r = True

        return is_in_r, cur_p
