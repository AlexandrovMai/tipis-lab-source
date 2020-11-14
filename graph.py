import matplotlib.pyplot as plt


class Graph:
    @classmethod
    def print_graph(cls, a_arr, v_arr, h_arr, b_cnt, m_arr, time_arr, graph_name):
        plt.figure(figsize=(16, 10))
        plt.subplot(5, 1, 1)
        plt.title("График a(t), h(t), v(t), b(t), m(t)")
        plt.xlabel("t")
        plt.grid()
        plt.ylabel("a(t)")
        plt.plot(time_arr, a_arr)

        plt.subplot(5, 1, 2)
        plt.xlabel("t")
        plt.ylabel("v(t)")
        plt.grid()
        plt.plot(time_arr, v_arr)

        plt.subplot(5, 1, 3)
        plt.xlabel("t")
        plt.grid()
        plt.ylabel("h(t)")
        plt.plot(time_arr, h_arr)

        plt.subplot(5, 1, 4)
        plt.xlabel("t")
        plt.grid()
        plt.ylabel("b(t)")
        plt.plot(time_arr, b_cnt)

        plt.subplot(5, 1, 5)
        plt.xlabel("t")
        plt.grid()
        plt.ylabel("m(t)")
        plt.plot(time_arr, m_arr)

        plt.savefig(graph_name)
        plt.close()
