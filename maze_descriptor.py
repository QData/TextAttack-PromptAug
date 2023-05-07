"""
This file is used to generate random maze infomation. 
"""

import json
import random
import os

# The folder to store the information about each maze
maze_folder = "maze_json"


"""
A class represent the information about the maze and the objects in the maze. 
"""

class maze:
        """
        Initialize the maze.

        Args:
                canvas_size: A number represents the height and width of the maze.
                s_pos: A tuple represent the start position of the agent.
                e_pos: A tuple represent the end position of the agent.
                obs_x: A list of number represent the horizontal position of the obstacles.
                obs_x: A list of number represent the vertical position of the obstacles.
                maze_name: A string to distingiush different mazes.
        """
        def __init__(self, canvas_size, s_pos, e_pos, obs, maze_name):
                self.canvas_size = canvas_size
                self.s_pos = s_pos
                self.e_pos = e_pos
                self.obs = obs
                self.maze_name = maze_name

        """
        Generate the json file represents the maze. 
        """

        def generate_data(self):
                data = {"maze name": self.maze_name,
                        "canvas size": self.canvas_size,
                         "start position": self.s_pos,
                           "end position": self.e_pos,
                        #    "number of obstacles": self.obs,
                           "obstacles": self.obs}

                # for i in range(len(self.obs)):
                #         ob_name = "obstacles " + str(i)
                #         obs = []
                # data["obstacles"] = (self.obs[i][0], self.obs[i][1])

                with open(maze_folder + "/" + self.maze_name + ".json", "w") as f:
                        json.dump(data, f)

"""
A class to generate random mazes.
"""

class random_maze_generate:
        """
        Initialize the maze generator

        Args:
                num_maze: number of mazes to generate.
                num_obstacles: number of obstacles placed in the maze.
                canvas_size: The size of the canvas.      
        """
        def __init__(self, num_maze, num_obstacles, canvas_size):
              self.num_maze = num_maze
              self.num_obstacles = num_obstacles
              self.canvas_size = canvas_size
        
        # Generate one random maze.
        def generate_one(self):
                s_pos = (random.randint(0, self.canvas_size - 1), random.randint(0, self.canvas_size - 1))
                e_pos = (random.randint(0, self.canvas_size - 1), random.randint(0, self.canvas_size - 1))
                while e_pos == s_pos:
                        e_pos = (random.randint(0, self.canvas_size - 1), random.randint(0, self.canvas_size - 1))
                obs_list = []
                exist = 0
                while exist < self.num_obstacles:
                        new_obs = (random.randint(0, self.canvas_size - 1), random.randint(0, self.canvas_size - 1))
                        while (new_obs in obs_list or new_obs == s_pos or new_obs == e_pos):
                                new_obs = (random.randint(0, self.canvas_size - 1), random.randint(0, self.canvas_size - 1))
                        exist += 1
                        obs_list.append(new_obs)
                return s_pos, e_pos, obs_list
                
        #generate the required number of random maze and store their info in the folder.
        def generate_all(self):
                folder_contents = os.listdir(maze_folder)

                # Loop through each item in the folder and remove it
                for item in folder_contents:
                        item_path = os.path.join(maze_folder, item)
                        os.remove(item_path)

                for i in range(self.num_maze):
                        s_pos, e_pos, obs_list = self.generate_one()
                        maze_name = "maze " + str(i)
                        m = maze(self.canvas_size, s_pos, e_pos, obs_list, maze_name)
                        m.generate_data()



if __name__ == '__main__':
        inputs = input("Enter three number to indicate the number of mazes, number of obstacles and the size of maze separately: ")
        input_list = inputs.split(" ")
        num_maze = input_list[0].strip()
        num_obs = input_list[1].strip()
        maze_size = input_list[2].strip()
        a = random_maze_generate(int(num_maze), int(num_obs), int(maze_size))        
        a.generate_all()
