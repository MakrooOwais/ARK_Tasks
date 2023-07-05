import math
import numpy as np
from PIL import Image, ImageDraw

class Node:
    def __init__(self, n):
        self.x = int(n[0])
        self.y = int(n[1])
        self.parent = None


class RrtConnect:
    def __init__(
        self, s_start, s_goal, step_len, goal_sample_rate, iter_max, env, delta=0.5
    ):
        self.s_start = Node(s_start)
        self.s_goal = Node(s_goal)
        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.iter_max = iter_max
        self.V1 = [self.s_start]
        self.V2 = [self.s_goal]

        self.env = env

        self.x_range = self.env.shape[1]
        self.y_range = self.env.shape[0]
        self.delta = delta

    def planning(self):
        for i in range(self.iter_max):
            node_rand = self.generate_random_node(self.s_goal, self.goal_sample_rate)
            node_near = self.nearest_neighbor(self.V1, node_rand)
            node_new = self.new_state(node_near, node_rand)

            if node_new and not self.is_collision(node_near, node_new):
                self.V1.append(node_new)
                node_near_prim = self.nearest_neighbor(self.V2, node_new)
                node_new_prim = self.new_state(node_near_prim, node_new)

                if node_new_prim and not self.is_collision(
                    node_new_prim, node_near_prim
                ):
                    self.V2.append(node_new_prim)

                    while True:
                        node_new_prim2 = self.new_state(node_new_prim, node_new)
                        if node_new_prim2 and not self.is_collision(
                            node_new_prim2, node_new_prim
                        ):
                            self.V2.append(node_new_prim2)
                            node_new_prim = self.change_node(
                                node_new_prim, node_new_prim2
                            )
                        else:
                            break

                        if self.is_node_same(node_new_prim, node_new):
                            break

                if self.is_node_same(node_new_prim, node_new):
                    return self.extract_path(node_new, node_new_prim), i

            if len(self.V2) < len(self.V1):
                list_mid = self.V2
                self.V2 = self.V1
                self.V1 = list_mid

        return None

    @staticmethod
    def change_node(node_new_prim, node_new_prim2):
        node_new = Node((node_new_prim2.x, node_new_prim2.y))
        node_new.parent = node_new_prim

        return node_new

    @staticmethod
    def is_node_same(node_new_prim, node_new):
        if node_new_prim.x == node_new.x and node_new_prim.y == node_new.y:
            return True

        return False

    def generate_random_node(self, sample_goal, goal_sample_rate):
        delta = self.delta

        if np.random.random() > goal_sample_rate:
            return Node(
                (
                    np.random.uniform(delta, self.x_range - delta),
                    np.random.uniform(delta, self.y_range - delta),
                )
            )

        return sample_goal

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[
            int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y) for nd in node_list]))
        ]

    def is_collision(self, node_1, node_2):
        if self.is_inside_obs(node_1) or self.is_inside_obs(node_2):
            return True

        u_hat = self.unit_vector(node_1, node_2)
        test_point = np.array([0, 0])
        for i in range(1, self.step_len):
            try:
                test_point[0] = node_1.x + i / 10 * u_hat[0]
            except:
                test_point[0] = 0

            try:
                test_point[1] = node_2.y + i / 10 * u_hat[1]
            except:
                test_point[1] = 0

            
            if self.is_inside_obs(Node(test_point)):
                return True
        return False

    def is_inside_obs(self, node: Node):
        # print(type(node.x))
        return not self.env[node.x][node.y]

    def unit_vector(self, start: Node, end: Node):
        v = np.array([end.x - start.x, end.y - start.y])
        u_hat = v / np.linalg.norm(v)
        return u_hat

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)

        dist = min(self.step_len, dist)
        node_new = Node(
            (
                node_start.x + dist * math.cos(theta),
                node_start.y + dist * math.sin(theta),
            )
        )
        node_new.parent = node_start

        return node_new

    @staticmethod
    def extract_path(node_new, node_new_prim):
        path1 = [(node_new.x, node_new.y)]
        node_now = node_new

        while node_now.parent is not None:
            node_now = node_now.parent
            path1.append((node_now.x, node_now.y))

        path2 = [(node_new_prim.x, node_new_prim.y)]
        node_now = node_new_prim

        while node_now.parent is not None:
            node_now = node_now.parent
            path2.append((node_now.x, node_now.y))

        return list(list(reversed(path1)) + path2)

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)

def reverse_coordinates(coor):
    return coor[1], coor[0]

def main():
    # try:
        maze_easy = (np.array(Image.open("maze_easy_bin.png")))
        # print(maze_easy)

        x_start = (maze_easy.shape[0] - 1, int(maze_easy.shape[1] / 4))
        x_goal = (maze_easy.shape[0] - 1, int(maze_easy.shape[1] * 3 / 4))
        print(x_start)
        print(x_goal)

        rrt_conn = RrtConnect(x_start, x_goal, 6, 0.05, 5000, maze_easy)
        path, num_itr = rrt_conn.planning()

        print(path)

        #map_img = Image.new("RGB", (maze_easy.shape[1], maze_easy.shape[0]))
        map_img = Image.open('maze_easy.png')
        draw = ImageDraw.Draw(map_img)
        path_rev = [reverse_coordinates(x) for x in path]
        draw.line(path_rev, fill='red')
        map_img.save('maze_easy_sol.png')
        print('Number of iterations: ', num_itr)
    # except:
    #     main()

if __name__ == "__main__":
    main()
