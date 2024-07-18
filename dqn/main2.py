import gymnasium as gym

env = gym.make('CartPole-v1', render_mode="human")

env.reset()

env.render()
env.step(env.action_space.sample())

env.close()
