from parcer import Reader
from r_counter import RCounter
from log import FileLogger

if __name__ == '__main__':
    fl = FileLogger("result/logs/mainlog.txt")
    fl.write_str("Reading table.csv")

    rd = Reader.parse_file('data/table.csv')
    fl.write_str("Parsed data from file:")

    fl.write_arr_to_file(rd)

    r_matrix = []
    for ob in rd:
        am = []
        for obn in rd:
            fl.write_str("Counting "+ob.ob_name+" R "+obn.ob_name)
            rc = RCounter("result/logs/"+ob.ob_name+"_R_"+obn.ob_name+".txt",
                          "result/graph/"+ob.ob_name+"_R_"+obn.ob_name+".jpg")
            rs, cur_p = rc.calc(ob, obn)
            fl.write_str("--[last_h: " + str(cur_p.h) + "]----- result: " + str(rs))
            am.append(int(rs))
        r_matrix.append(am)

    fl.write_str("R Matrix:")
    fl.write_r_table(r_matrix, rd)
    fl.close()
