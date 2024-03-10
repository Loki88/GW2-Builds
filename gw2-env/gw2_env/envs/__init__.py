from gym.envs.registration import register

register(
    id='gw2_env/BaseWeaponAndSkill-v0',
    entry_point='gw2_env.envs:BaseWeaponAndSkillEnv',
    max_episode_steps=300,
)