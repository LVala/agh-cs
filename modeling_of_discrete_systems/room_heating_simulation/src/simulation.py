from enum import Enum

class Types(Enum):
    air = 1
    wall_poor = 2
    wall_good = 3
    window = 4
    heat_source = 5

class Cell:
    def __init__(self, cell_type, temperature, length):
        self.type = cell_type
        self.temperature = temperature
        self.new_temperature = temperature
        self.length = length
        self.neigh = []
        self.init_values(self.type)

    def init_values(self, type):
        if type == Types.air:
            self.cond = 0.026
            self.dens = 1.225
            self.shc = 713
            self.htc = 2.5
        elif type == Types.wall_poor:
            self.uvalue = 1.5
        elif type == Types.wall_good:
            self.uvalue = 0.25
        elif type == Types.window:
            self.uvalue = 2.2
        elif type == Types.heat_source:
            self.uvalue = 5

    def set_behind_temp(self, temp):
        if self.type is Types.air:
            pass
        elif self.type is Types.heat_source:
            self.behind_temp = temp
            self.temperature = temp
        else:
            self.behind_temp = temp

    def add_neigh(self, neigh):
        self.neigh.append(neigh)

    def count_cond(self, d_t):
        d_Q = 0
        for neigh in self.neigh:
            if neigh.type is Types.air:
                d_Q -= neigh.cond * (self.temperature - neigh.temperature) * d_t * self.length
            else:
                d_Q -= self.length * self.length * neigh.uvalue * (self.temperature - neigh.behind_temp)

        d_T = d_Q/(self.shc * self.dens * self.length**3)
        return d_T

    def count_conv(self, d_t):
        d_Q = 0
        if self.neigh[4].type is Types.air and self.neigh[4].temperature > self.temperature:
            d_Q -= self.htc * self.length**2 * (self.temperature - self.neigh[4].temperature) * d_t
        if self.neigh[5].type is Types.air and self.neigh[5].temperature < self.temperature:
            d_Q -= self.htc * self.length**2 * (self.temperature - self.neigh[5].temperature) * d_t

        if self.neigh[5].type is not Types.air:
            for i in range(4):
                if self.neigh[i].type is Types.air:
                    d_Q -= 0.25 * self.htc * self.length**2 * (self.temperature - self.neigh[i].temperature) * d_t

        d_T = d_Q/(self.shc * self.dens * self.length**3)
        return d_T

    def update_temp(self, d_t):
        self.new_temperature = 0
        if self.type is Types.air:
            self.new_temperature += self.temperature + self.count_cond(d_t)
            self.new_temperature += self.count_conv(d_t) 
    
    def set_new_temp(self):
        if self.type is Types.air:
            self.temperature = self.new_temperature

class Space:
    def __init__(self, length, width, height, cell_length, outside_temp, inside_temp, heat_temp, d_t):
        length_in_cells = int(length // cell_length)
        width_in_cells = int(width // cell_length)
        height_in_cells = int(height // cell_length)
        self.d_t = d_t
        
        self.space = [[[None]*height_in_cells for _ in range(width_in_cells)] for _ in range(length_in_cells)]
        self.init_room(cell_length, outside_temp, inside_temp, heat_temp)
        self.init_neigh()

    def init_neigh(self):
        for i in range(1, len(self.space)-1):
            for j in range(1, len(self.space[0])-1):
                for k in range(1, len(self.space[0][0])-1):
                    self.space[i][j][k].add_neigh(self.space[i-1][j][k])
                    self.space[i][j][k].add_neigh(self.space[i+1][j][k])
                    self.space[i][j][k].add_neigh(self.space[i][j-1][k])
                    self.space[i][j][k].add_neigh(self.space[i][j+1][k])
                    self.space[i][j][k].add_neigh(self.space[i][j][k-1])
                    self.space[i][j][k].add_neigh(self.space[i][j][k+1])

    def init_room(self, cell_length, outside_temp, inside_temp, heat_temp):
        x = len(self.space) - 1
        y = len(self.space[0]) - 1
        z = len(self.space[0][0]) - 1
        # free space - air
        self.define_space_type((0, 0, 0), (x, y, z), Types.air, inside_temp, inside_temp, cell_length)
        # floor
        self.define_space_type((0, 0, 0), (x, y, 0), Types.wall_good, inside_temp, inside_temp, cell_length)
        # ceiling
        self.define_space_type((0, 0, z), (x, y, z), Types.wall_good, inside_temp, inside_temp, cell_length)
        # three poorly isolated walls
        self.define_space_type((0, 0, 0), (0, y, z), Types.wall_poor, inside_temp, inside_temp, cell_length)
        self.define_space_type((0, 0, 0), (x, 0, z), Types.wall_poor, inside_temp, inside_temp, cell_length)
        self.define_space_type((x, 0, 0), (x, y, z), Types.wall_poor, inside_temp, inside_temp, cell_length)
        # well isolated wall with window
        self.define_space_type((0, y, 0), (x, y, z), Types.wall_good, outside_temp, outside_temp, cell_length)
        self.define_space_type((0 + x // 3, y, 0 + z // 3), (x - x // 3, y, z - z // 3), Types.window, inside_temp, outside_temp, cell_length)
        # heat source - under the window, one cell inside the room
        self.define_space_type((0 + x // 3, y - 1, 0), (x - x // 3, y - 1, z // 3), Types.heat_source, inside_temp, heat_temp, cell_length)
        #self.define_space_type((x // 2, y // 2, z // 2), (x // 2, y // 2, z // 2), Types.heat_source, inside_temp, heat_temp, cell_length)

    def define_space_type(self, coordinates1, coordinates2, cell_type, init_tem, behind_temp, cell_length):
        (x1, y1, z1) = coordinates1
        (x2, y2, z2) = coordinates2

        for x in range (x1, x2 + 1):
            for y in range (y1, y2 + 1):
                for z in range (z1, z2 + 1):
                    self.space[x][y][z] = Cell(cell_type, init_tem, cell_length)
                    self.space[x][y][z].set_behind_temp(behind_temp)

    def iter(self):
        for i in range(1, len(self.space)-1):
            for j in range(1, len(self.space[0])-1):
                for k in range(1, len(self.space[0][0])-1):
                    self.space[i][j][k].update_temp(self.d_t)

        for i in range(1, len(self.space)-1):
            for j in range(1, len(self.space[0])-1):
                for k in range(1, len(self.space[0][0])-1):
                    self.space[i][j][k].set_new_temp()