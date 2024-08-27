from env import Mars
from stable_baselines3 import A2C as algo
env=Mars(20, 20, True)
model=algo("MlpPolicy", env, verbose=2)
model.learn(100000, progress_bar=True)
model.save("model")