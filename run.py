from env import Mars
from stable_baselines3 import A2C as algo

env=Mars(20, 20, True)
model=algo("MlpPolicy", env=env)
model.load("model")
done=False
ter=False
obs, _=env.reset()
while (not done or not ter):
    action=model.predict(obs)
    obs, rew, done, ter, info=env.step(action[0])
    print(rew)