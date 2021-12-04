import heapq
import matplotlib.pyplot as plt
import numpy as np
import pyodbc

blue = (0, 0, 255)
red = (255, 0, 0)

# pygame.init()
# screen = pygame.display.set_mode([500, 500])

fig, ax = plt.subplots(figsize=(1, 1))


# def onclick(event):
#     tena_x = int(event.xdata)
#     tena_y = int(event.ydata)
#     print('button=%d, x=%d, y=%d, tena_x=%d, tena_y=%d' %
#           (event.button, event.x, event.y, tena_x, tena_y))
#     plt.plot(tena_x, tena_y, ',')
#     fig.canvas.draw()


class node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.large = 4


class chemin:
    def __init__(self, data):
        self.idChemin = data[0]
        self.sens = data[1]
        self.start = (int(data[2].split("|")[0]), int(data[2].split("|")[1]))
        self.finish = (int(data[3].split("|")[0]), int(data[3].split("|")[1]))
        self.points = []
        self.largeur = 5
        if self.start[0] == self.finish[0]:
            for y in range(self.start[1], self.finish[1]):
                self.points.append(node(self.start[0], y))
        elif self.start[1] == self.finish[1]:
            for x in range(self.start[0], self.finish[0]):
                self.points.append(node(x, self.start[1]))

        if self.sens == "U":
            self.color = red
        else:
            self.color = blue

    # def draw(self):
    #     for point in self.points:
    #         pygame.draw.rect(screen, self.color, (point.x, point.y, 5, 5))


def generate_matrix(map_width, map_height):
    return np.ones((map_width, map_height), dtype=int)


def generatre_matrixpoint(map_width, map_height):
    return np.full((map_width, map_height), node)


def initialize_matrixpoint(mat, matp):
    for i in range(mat.shape[1]):
        for j in range(mat.shape[0]):
            matp[j, i] = node(j, i)


# def heuristic(p1: node, p2: node):
#     h = abs(p2.x - p1.x) + abs(p2.y - p1.y)
#     return h

class vehicle:
    def __init__(self, large, speed):
        self.large = large
        self.speed = speed


class maps:
    def __init__(self, width, height, paths, start: node, finish: node):
        """

        :type finish: node
        """
        self.width = width
        self.height = height
        self.paths = paths
        self.start = start
        self.finish = finish
        self.cid = fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        real_x = int(event.xdata)
        real_y = int(event.ydata)
        if event.dblclick:
            self.finish = node(real_x, real_y)
        else:
            self.start = node(real_x, real_y)

        print((self.start.x, self.start.y))
        print((self.finish.x, self.finish.y))

    # def draw(self):
    #     for path in self.paths:
    #         path.draw()

    def init_matrix(self, mat):
        for path in self.paths:
            for point in path.points:
                mat[point.y, point.x] = 0


# def onclick(m: maps, event):
#     real_x = int(event.xdata)
#     real_y = int(event.ydata)
#     print('button=%d, x=%d, y=%d, real_x=%d, real_y=%d' %
#           (event.button, event.x, event.y, real_x, real_y))
#     if event.dblclick:
#         m.finish = node(real_x, real_y)
#     else:
#         m.start = node(real_x, real_y)

def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(array, array_node, vam:vehicle, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()

    came_from = {}

    gscore = {start: 0}

    fscore = {start: heuristic(start, goal)}

    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:

            data = []

            while current in came_from:
                data.append(current)

                current = came_from[current]

            return data

        close_set.add(current)

        for i, j in neighbors:

            neighbor = current[0] + i, current[1] + j

            tentative_g_score = gscore[current] + heuristic(current, neighbor)

            if 0 <= neighbor[1] < array.shape[0]:

                if 0 <= neighbor[0] < array.shape[1]:

                    if array[neighbor[1]][neighbor[0]] == 1 or array_node[neighbor[1]][neighbor[0]].large < vam.large:
                        continue

                else:
                    continue

            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current

                gscore[neighbor] = tentative_g_score

                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False


if __name__ == "__main__":

    # conn = pyodbc.connect('Driver={SQL Server};'
    #                       'Server=DESKTOP-FB9Q3GV;'
    #                       'Database=Maps;'
    #                       'Trusted_Connection=yes;')
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=P13B-08-ERICKO;'
                          'Database=Maps;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Maps.dbo.Path')
    chemins = []
    for row in cursor:
        chemins.append(chemin(row))

    start = (100, 220)
    finish = (250, 400)
    moto = vehicle(4, 10)
    myMap = maps(500, 500, chemins, node(22, 10), node(22, 200))
    matrix = generate_matrix(500, 500)
    matrix_point = generatre_matrixpoint(500, 500)
    initialize_matrixpoint(matrix, matrix_point)
    myMap.init_matrix(matrix)
    route = astar(matrix, matrix_point, moto, start, finish)
    print(route)
    route = route + [start]
    route = route[::-1]
    x_coords = []

    y_coords = []

    for i in (range(0, len(route))):
        x = route[i][1]

        y = route[i][0]

        x_coords.append(x)

        y_coords.append(y)

    ax.imshow(matrix, cmap=plt.cm.viridis)
    ax.plot(y_coords, x_coords, color="cyan", linewidth=4)
    plt.show()

    # cid = fig.canvas.mpl_connect('button_press_event', onclick)
    # running = True
    # while running:
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #
    #     screen.fill((255, 255, 255))
    #     click = pygame.mouse.get_pressed()
    #
    #     if click[0]:
    #         pygame.display.set_caption(str(pygame.mouse.get_pos()[0]) + "," + str(pygame.mouse.get_pos()[1]))
    #         pos = pygame.mouse.get_pos()
    #         pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], 5, 5))
    #
    #     for chem in chemins:
    #         chem.draw()
    #
    #     pygame.display.flip()
    # pygame.quit()
