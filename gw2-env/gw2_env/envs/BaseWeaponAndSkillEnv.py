import gym

from gym import spaces
import pygame
import numpy as np

from spaces import CondiSpace, BoonSpace


class BaseWeaponAndSkillEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}
    
    def __init__(self, render_mode=None, health=4000000, input_lag = 0.1):
        self.target_health = health  # The size of the square grid
        self.window_size = 512  # The size of the PyGame window
        self.input_lag = input_lag  # The delay between the agent's action and the environment's response

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "time": spaces.Box(low=0, shape=(), dtype=np.float32),
                "agent": spaces.Dict(
                    {
                        "cast_time": spaces.Box(low=0, shape=(), dtype=np.float32),
                        "dps": spaces.Box(low=0, shape=()),
                        "applied_boons": spaces.Dict(
                            {
                                "aegis": BoonSpace(spaces.Discrete(2)),
                                "stability": BoonSpace(spaces.Box(low=0, space=(), dtype=np.int16)),
                                "fury": BoonSpace(spaces.Discrete(2)),
                                "regeneration": BoonSpace(spaces.Discrete(2)),
                                "swiftness": BoonSpace(spaces.Discrete(2)),
                                "protection": BoonSpace(spaces.Discrete(2)),
                                "vigor": BoonSpace(spaces.Discrete(2)),
                                "alacrity": BoonSpace(spaces.Discrete(2)),
                                "quickness": BoonSpace(spaces.Discrete(2)),
                                "resolution": BoonSpace(spaces.Discrete(2)),
                                "might": BoonSpace(spaces.Box(low=0, high=25, shape=(), dtype=np.int16)),
                                "resistance": BoonSpace(spaces.Discrete(2)),
                            }
                        ),
                        "applied_conditions": spaces.Dict(
                            {
                                "bleeding": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                "burning": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                "confusion": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                "poisoned": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                "torment": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                "blinded": CondiSpace(spaces.Discrete(2)),
                                "crippled": CondiSpace(spaces.Discrete(2)),
                                "chilled": CondiSpace(spaces.Discrete(2)),
                                "immobilized": CondiSpace(spaces.Discrete(2)),
                                "fear": CondiSpace(spaces.Discrete(2)),
                                "weakness": CondiSpace(spaces.Discrete(2)),
                                "vulnerability": CondiSpace(spaces.Box(low=0, high=25, shape=(), dtype=np.int16)),
                                "slow": CondiSpace(spaces.Discrete(2)),
                                "taunt": CondiSpace(spaces.Discrete(2)),
                            }
                        ),
                    }),
                "target": spaces.Dict (
                        {
                            "health": spaces.Box(low=0, high=self.target_health, shape=()),
                            "boons": spaces.Dict(
                                {
                                    "aegis": BoonSpace(spaces.Discrete(2)),
                                    "stability": BoonSpace(spaces.Box(low=0, space=(), dtype=np.int16)),
                                    "fury": BoonSpace(spaces.Discrete(2)),
                                    "regeneration": BoonSpace(spaces.Discrete(2)),
                                    "swiftness": BoonSpace(spaces.Discrete(2)),
                                    "protection": BoonSpace(spaces.Discrete(2)),
                                    "vigor": BoonSpace(spaces.Discrete(2)),
                                    "alacrity": BoonSpace(spaces.Discrete(2)),
                                    "quickness": BoonSpace(spaces.Discrete(2)),
                                    "resolution": BoonSpace(spaces.Discrete(2)),
                                    "might": BoonSpace(spaces.Box(low=0, high=25, shape=(), dtype=np.int16)),
                                    "resistance": BoonSpace(spaces.Discrete(2)),
                                }
                            ),
                            "conditions": spaces.Dict(
                                {
                                    "bleeding": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                    "burning": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                    "confusion": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                    "poisoned": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                    "torment": CondiSpace(spaces.Box(low=0, high=1500, shape=(), dtype=np.int16)),
                                    "blinded": CondiSpace(spaces.Discrete(2)),
                                    "crippled": CondiSpace(spaces.Discrete(2)),
                                    "chilled": CondiSpace(spaces.Discrete(2)),
                                    "immobilized": CondiSpace(spaces.Discrete(2)),
                                    "fear": CondiSpace(spaces.Discrete(2)),
                                    "weakness": CondiSpace(spaces.Discrete(2)),
                                    "vulnerability": CondiSpace(spaces.Box(low=0, high=25, shape=(), dtype=np.int16)),
                                    "slow": CondiSpace(spaces.Discrete(2)),
                                    "taunt": CondiSpace(spaces.Discrete(2)),
                                }
                            ),
                        }
                    ),
            }
        )

        # We have 4 actions, corresponding to "right", "up", "left", "down"
        self.action_space = spaces.Discrete(10)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the skill we will use if that action is taken.
        I.e. 0 corresponds to weapon 1st, 1 to weapon 2, 5 to healing skill,  etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
        
    # these methods need that reset and step are implemented to be effectively implemented
    def _get_obs(self):
        return {"time": self._agent_location, "dps": self._target_location, "target_health": self.target_health}
    
    def _get_info(self):
        return {"distance": np.linalg.norm(self._agent_location - self._target_location, ord=1)}
    
    def _action_to_skill(self, action):
        raise NotImplementedError()
    
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Choose the agent's location uniformly at random
        self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)

        # We will sample the target's location randomly until it does not coincide with the agent's location
        self._target_location = self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, info
    
    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]
        # We use `np.clip` to make sure we don't leave the grid
        self._agent_location = np.clip(
            self._agent_location + direction, 0, self.size - 1
        )
        # An episode is done iff the agent has reached the target
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0  # Binary sparse rewards
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.window_size / self.size
        )  # The size of a single grid square in pixels

        # First we draw the target
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(
                pix_square_size * self._target_location,
                (pix_square_size, pix_square_size),
            ),
        )
        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (self._agent_location + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # Finally, add some gridlines
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
            
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()