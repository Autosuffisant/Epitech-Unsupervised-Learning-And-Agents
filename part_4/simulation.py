import os

import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from maxime_owaller_policy import maxime_owaller_policy

WORLD_SIZE = 8
WORLD_UPDATE_PERIOD = 10
NB_PERIODS = int(2e3)
TOTAL_NUMBER_OF_STEPS = NB_PERIODS * WORLD_UPDATE_PERIOD
MAX_REWARD = 100
NB_REWARDS = 3


def reset_rewards(world_size: int) -> np.ndarray:
    rewards = np.zeros(world_size)
    for _ in range(NB_REWARDS):
        reward = np.random.randint(MAX_REWARD)
        position = np.random.randint(world_size)
        rewards[position] = reward
    return rewards


def run_simulation() -> list:
    rewards = reset_rewards(WORLD_SIZE)

    # initially, the agent does not know
    # the rewards distribution and the rewards
    # that are known to the agent are set to 0
    known_rewards = np.zeros(WORLD_SIZE)
    initial_position = int(WORLD_SIZE / 2)
    agent = Agent(initial_position, known_rewards)

    accumulated_reward = 0
    averaged_rewards = list()

    for step in range(TOTAL_NUMBER_OF_STEPS):

        # update world periodically
        # when the world is updated, the agent knows nothing
        # about the rewards anymore
        if step % (WORLD_UPDATE_PERIOD) == 0:
            rewards = reset_rewards(WORLD_SIZE)
            agent.known_rewards = np.zeros(WORLD_SIZE)
            # print("\n---\nreset the rewards\n---")
            # print(f"rewards: {rewards}\n")

        # choose action and move agent
        action = maxime_owaller_policy(agent)
        agent.move(action, WORLD_SIZE)
        # print(f"move {action}")
        # print(f"position: {agent.position}")

        # get reward
        reward = rewards[agent.position]
        agent.known_rewards[agent.position] = reward
        # print(f"found reward {reward}")
        # print(f"known rewards: {agent.known_rewards}\n")

        # update and average the obtained rewards
        accumulated_reward += reward
        averaged_reward = accumulated_reward / (step + 1)
        averaged_rewards.append(averaged_reward)
    return averaged_rewards


def main():
    averaged_rewards = run_simulation()
    final_averaged_reward = averaged_rewards[-1]
    print(f"final reward: {final_averaged_reward:.3f}")
    plt.plot(range(TOTAL_NUMBER_OF_STEPS), averaged_rewards, "o", markersize=1)
    plt.xlabel("simulation steps")
    plt.ylabel("accumulated reward")
    plt.ylim([-0.1 * final_averaged_reward, 2.1 * final_averaged_reward])
    title = (
        f"Averaged accumulated reward\n" f"averaged reward: {final_averaged_reward:.3f}"
    )
    plt.title(title)
    figname = f"{final_averaged_reward:.3f}.pdf"
    figpath = os.path.join("images", figname)
    plt.savefig(figpath)
    plt.close()


def clean(folder: str) -> None:
    for filename in os.listdir(folder):
        os.remove(os.path.join(folder, filename))


if __name__ == "__main__":
    main()