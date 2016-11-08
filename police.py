#!/usr/bin/env python3

import asyncio
import sys
import random
import cozmo

from cozmo.util import degrees

def run(sdk_conn):
	robot = sdk_conn.wait_for_robot()
	foundThief = False
	robot.set_all_backpack_lights(cozmo.lights.red_light)
	robot.set_head_angle(degrees(0.0)).wait_for_completed()
	robot.set_lift_height(0.0).wait_for_completed()

	while not foundThief:
		if not random.randint(0,5) == 10:
			print("turn")
			robot.turn_in_place(degrees(random.randint(60,180))).wait_for_completed()

			print("looking around")
			cube = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=3)

			print(len(cube))

			if cube is not None:
				if len(cube) <= 0:
					'robot.say_text("Where are you").wait_for_completed()'
					'lookaround.stop()'
				else:
					cube[0].set_lights(cozmo.lights.red_light)
					robot.say_text("Found You").wait_for_completed()
					'foundThief = True'
		else:
			sleep = robot.play_anim_trigger(cozmo.anim.Triggers.Sleeping).wait_for_completed()
			print("wakeup")

	while foundThief:
		win = robot.play_anim_trigger(cozmo.anim.Triggers.SuccessfulWheelie).wait_for_completed()


if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.connect_with_tkviewer(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
