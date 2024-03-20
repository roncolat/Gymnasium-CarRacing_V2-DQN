import gymnasium as gym
import pygame

is_pressed_left  = False # control left
is_pressed_right = False # control right
is_pressed_space = False # control gas
is_pressed_shift = False # control break
is_pressed_esc   = False # exit the game
is_pressed_ret   = False # restart the game
steering_wheel = 0 # init to 0
gas            = 0 # init to 0
break_system   = 0 # init to 0


def register_input():
    global is_pressed_left
    global is_pressed_right
    global is_pressed_space
    global is_pressed_shift
    global is_pressed_esc
    global is_pressed_ret

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                is_pressed_left = True
            if event.key == pygame.K_RIGHT:
                is_pressed_right = True
            if event.key == pygame.K_SPACE:
                is_pressed_space = True
            if event.key == pygame.K_LSHIFT:
                is_pressed_shift = True
            if event.key == pygame.K_RETURN:
                is_pressed_ret = True
            if event.key == pygame.K_ESCAPE:
                is_pressed_esc = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                is_pressed_left = False
            if event.key == pygame.K_RIGHT:
                is_pressed_right = False
            if event.key == pygame.K_SPACE:
                is_pressed_space = False
            if event.key == pygame.K_LSHIFT:
                is_pressed_shift = False
            
def update_action():
    global steering_wheel
    global gas
    global break_system

    if is_pressed_left ^ is_pressed_right:
        if is_pressed_left:
            if steering_wheel > -1:
                steering_wheel -= 0.1
            else:
                steering_wheel = -1
        if is_pressed_right:
            if steering_wheel < 1:
                steering_wheel += 0.1
            else:
                steering_wheel = 1
    else:
        if abs(steering_wheel - 0) < 0.1:
            steering_wheel = 0
        elif steering_wheel > 0:
            steering_wheel -= 0.1
        elif steering_wheel < 0:
            steering_wheel += 0.1
    if is_pressed_space:
        if gas < 1:
            gas += 0.1
        else:
            gas = 1
    else:
        if gas > 0:
            gas -= 0.1
        else:
            gas = 0
    if is_pressed_shift:
        if break_system < 1:
            break_system += 0.1
        else:
            break_system = 1
    else:
        if break_system > 0:
            break_system -= 0.1
        else:
            break_system = 0

if __name__ == '__main__':
    env = gym.make('CarRacing-v2', render_mode="human")
    while not is_pressed_esc:
        state = env.reset()
        counter = 0
        total_reward = 0
        print("Restart game after {} timesteps. Total Reward: {}".format(counter, total_reward))
             
        while True:
            register_input()
            update_action()
            action = [steering_wheel, gas, break_system]
            state, reward, terminated, truncated, info = env.step(action)
            counter += 1
            total_reward += reward
            print('Action:[{:+.1f}, {:+.1f}, {:+.1f}] Reward: {:.3f}'.format(action[0], action[1], action[2], reward))
            if terminated or truncated or is_pressed_ret or is_pressed_esc:
                break
        
    env.close()
