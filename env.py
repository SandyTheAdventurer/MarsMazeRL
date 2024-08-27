import pygame
import numpy as np
from typing import Any
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
from gymnasium.utils.env_checker import check_env
from gen import generate_maze, maze_modify

class Mars(Env):
  def __init__(self, xlen, ylen, fuel) -> None:
    super().__init__()
    maze, start, end=gen_maze(xlen, ylen) if xlen%2==1 and ylen%2==1 else gen_maze(xlen+1, ylen+1)
    self.maze, self.start, self. end= maze, start, end
    self.xlen=xlen
    self.ylen=ylen
    self.pos=list(self.start)
    self.dec_fuel=fuel
    self.fuel=xlen*ylen+50
    self.observation_space = Box(low=0, high=4, shape=(3, 3), dtype=int)
    self.action_space=Discrete(4)

  def get_obs(self):
    obs=[[self.maze[self.pos[0]-1][self.pos[1]-1],self.maze[self.pos[0]-1][self.pos[1]],self.maze[self.pos[0]-1][self.pos[1]+1]],
       [self.maze[self.pos[0]][self.pos[1]-1],self.maze[self.pos[0]][self.pos[1]],self.maze[self.pos[0]][self.pos[1]+1]],
       [self.maze[self.pos[0]+1][self.pos[1]-1],self.maze[self.pos[0]+1][self.pos[1]],self.maze[self.pos[0]+1][self.pos[1]+1]]]
    info={}
    return np.array(obs), info
  
  def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
    super().reset(seed=seed, options=options)
    self.__init__(self.xlen, self.ylen, fuel=self.dec_fuel)
    return self.get_obs()
  
  def get_reward(self):
    cell_value = self.maze[self.pos[0]][self.pos[1]]
    reward = 0
    if cell_value == 3:
      self.maze[self.pos[0]][self.pos[1]] = 0
      reward += 10
    elif cell_value == 2:
      reward -= 10
      self.fuel -= 5
    if self.pos == self.end:
      reward += 100
    reward += self.fuel-100

    return reward

  def step(self, action: list[int]) -> tuple[Any, float, bool, dict[str, Any]]:
    prev_pos = self.pos.copy()
    self.pos = move(self.maze, action, self.pos)
    done = False
    reward = 0
    terminate = False
    if self.pos == prev_pos:
        reward -= 10
        terminate = True
    if self.fuel <= 0:
        print("You have reached the end of the maze")
        done = True
    if self.dec_fuel:
        self.fuel -= 1
    reward += self.get_reward()  # Calculate the reward for the current step
    obs, info = self.get_obs()

    return obs, reward, done, terminate, info


def gen_maze(width, height):
  maze ,start ,end= generate_maze(width, height)
  maze = maze_modify(maze)
  return maze, start, end

def move(array,user_input,pos):
  if user_input==0:
    if array[pos[0]-1][pos[1]]==1:
      return pos
    else:
      pos[0]-=1
      return pos
  if user_input==1:
    if array[pos[0]][pos[1]+1]==1:
      return pos
    else:
      pos[1]+=1
      return pos         
  if user_input==2:
    if array[pos[0]+1][pos[1]]==1:
      return pos
    else:
      pos[0]+=1
      return pos
  if user_input==3:
    if array[pos[0]][pos[1]-1]==1:
      return pos
    else:
      pos[1]-=1
      return pos
  
check_env(Mars(5,5, True))

if __name__=="__main__":
  print(gen_maze(5,5))
