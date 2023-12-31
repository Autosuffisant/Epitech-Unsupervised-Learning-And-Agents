from agent import Agent
import random

def maxime_owaller_policy(agent: Agent) -> str:
    """
    If the agent has no known rewards, it randomly chooses between moving left or right.
    Otherwise, it remains stationary.
    """
    if sum(agent.known_rewards) != 0:
        return "none"
    else:
        return random.choice(["left", "right"])