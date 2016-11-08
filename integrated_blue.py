#!/usr/bin/env python3

'''
Control Cozmo using a webpage on your computer.
This example lets you control Cozmo by Remote Control, using a webpage served by Flask.
'''
import cozmo
import asyncio
import sys
import json
import os
import time
import flask_helpers
import random
import sched

from PIL import ImageDraw, ImageFont
try:
    from flask import Flask, request
    from flask import send_from_directory
except ImportError:
    sys.exit("Cannot import from flask: Do `pip3 install flask` to install")

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install Pillow` to install")

class SingBot():
    def __init__(self, robot):
        self._player = None
        self.happyQueue = 0
        self.angryQueue = 0
        self.score = 0
        self.total = 0
        self.bot = robot
        self.happyAnim = [
            cozmo.anim.Triggers.AcknowledgeFaceNamed,
            cozmo.anim.Triggers.CubePounceWinHand,
            cozmo.anim.Triggers.CubePounceWinRound,
            cozmo.anim.Triggers.KnockOverSuccess,
            cozmo.anim.Triggers.MeetCozmoFirstEnrollmentCelebration,
            cozmo.anim.Triggers.OnSimonCozmoHandComplete,
            cozmo.anim.Triggers.OnSimonCozmoWin,
            cozmo.anim.Triggers.OnWiggle
        ]
        self.happyText = [
            'Yay',
            'Good job',
            'Weeeeeee',
            'This is fun',
            'Time to party',
            'boom shaka la ka'
        ]
        self.angryAnim = [
            cozmo.anim.Triggers.AskToBeRightedLeft,
            cozmo.anim.Triggers.BlockReact,
            cozmo.anim.Triggers.CantHandleTallStack,
            cozmo.anim.Triggers.CubeMovedSense,
            cozmo.anim.Triggers.CubeMovedUpset,
            cozmo.anim.Triggers.CubePounceFake,
            cozmo.anim.Triggers.CubePounceGetIn,
            cozmo.anim.Triggers.CubePounceGetReady,
            cozmo.anim.Triggers.CubePounceLoseHand,
            cozmo.anim.Triggers.CubePounceLoseRound,
            cozmo.anim.Triggers.CubePounceLoseSession,
            cozmo.anim.Triggers.FacePlantRoll,
            cozmo.anim.Triggers.FrustratedByFailure,
            cozmo.anim.Triggers.KnockOverEyes,
            cozmo.anim.Triggers.MajorWin
        ]
        self.angryText = [
            'Noooooooo',
            'What are you doing?',
            'Stop it',
            'I am gonna get angry',
            'Next player please'
        ]

        self.scoreText = [
            'You are perfect',
            'You did a good job',
            'You can do better',
            'Are you even taking this seriously?'
        ]

    def start_speaking(self):
        if self._player:
            raise ValueError("speaking")
        async def _player():
            while True:
                if(self.angryQueue > 0):
                    if (random.randint(0, 1) == 1):
                        index = random.randint(0, len(self.angryAnim) - 1)
                        await self.bot.play_anim_trigger(self.angryAnim[index]).wait_for_completed()
                    else:
                        index = random.randint(0, len(self.angryText) - 1)
                        await self.bot.say_text(self.angryText[index]).wait_for_completed()
                    self.angryQueue -= 1
                elif(self.happyQueue > 0):
                    if (random.randint(0,1) == 1):
                        index = random.randint(0, len(self.happyAnim) - 1)
                        await self.bot.play_anim_trigger(self.happyAnim[index]).wait_for_completed()
                    else:
                        index = random.randint(0, len(self.happyText) - 1)
                        await self.bot.say_text(self.happyText[index]).wait_for_completed()
                        #await self.bot.say_text('save me master').wait_for_completed()
                await asyncio.sleep(0.1)
        self._player = asyncio.ensure_future(_player())

    async def evaluate(self):
        print(self.score)
        if(self.score/self.total  == 1.0):
            await self.bot.say_text(self.scoreText[0]).wait_for_completed()
            await self.bot.play_anim_trigger(self.happyAnim[6]).wait_for_completed()
        elif(self.score/self.total >= 0.75):
            await self.bot.say_text(self.scoreText[1]).wait_for_completed()
            await self.bot.play_anim_trigger(self.happyAnim[7]).wait_for_completed()
        elif(self.score/self.total >= 0.4):
            await self.bot.say_text(self.scoreText[2]).wait_for_completed()
            await self.bot.play_anim_trigger(self.angryAnim[2]).wait_for_completed()
        else:
            await self.bot.say_text(self.scoreText[3]).wait_for_completed()
            await self.bot.play_anim_trigger(self.angryAnim[10]).wait_for_completed()
        await self.displayScore()

    async def displayScore(self):
        '''Make a Pillow.Image with the current time printed on it

        Args:
            text_to_draw (string): the text to draw to the image
            x (int): x pixel location
            y (int): y pixel location
            font (PIL.ImageFont): the font to use

        Returns:
            :class:(`PIL.Image.Image`): a Pillow image with the text drawn on it
        '''
        end_font = None
        try:
            end_font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            try:
                end_font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
            except IOError:
                pass

        # make a blank image for the text, initialized to opaque black
        txt = Image.new('RGBA', cozmo.lcd_face.dimensions(), (0, 0, 0, 255))

        # get a drawing context
        dc = ImageDraw.Draw(txt)
        score = int(float(self.score/self.total*100))
        # draw the text
        dc.text((2, 2), 'Score:' + str(score) +'%', fill=(255, 255, 255, 255), font=end_font)

        lcd_face_data = cozmo.lcd_face.convert_image_to_screen_data(txt)

        # display for 1 second
        self.bot.display_lcd_face_image(lcd_face_data, 5000.0)

        return txt

    def stop_speaking(self):
        if self._player:
            self._player.cancel()
            self._player = None

    def get_random_anim(self, isHappy):
        if isHappy:
            index = random.randint(0, len(self.happyAnim) - 1)
            return self.happyAnim[index]
        elif not isHappy:
            index = random.randint(0, len(self.angryAnim) - 1)
            return self.angryAnim[index]

async def start_end_sequence(cubes):
    count = 5
    for y in range(0, count - 1):
        for i in range(0, 3):
            for x in range(0, len(cubes)):
                cols = [cozmo.lights.green_light] * 4
                cubes[x].set_light_corners(*cols)
                await asyncio.sleep(0.05)
                cols = [cozmo.lights.blue_light] * 4
                cubes[x].set_light_corners(*cols)
                await asyncio.sleep(0.05)
                cols = [cozmo.lights.red_light] * 4
                cubes[x].set_light_corners(*cols)
                await asyncio.sleep(0.05)

def get_random_lights():
    index = random.randint(0, 2)
    if (index == 0):
        return cozmo.lights.blue_light
    elif (index == 1):
        return cozmo.lights.green_light
    elif (index == 2):
        return cozmo.lights.red_light

async def cube_tap(cubes, newbot, total_taps, timeout):
    newbot.total = total_taps
    for x in range(0,total_taps):
        try:
            print (len(cubes))
            index = random.randint(0,2)
            light = get_random_lights()
            cols = [cozmo.lights.blue_light] * 4  # set all lights to off
            cubes[index].set_light_corners(*cols)  # set lights to on or off depending on initialised values
            tapped_cube = await cubes[index].wait_for_tap(timeout=timeout)
            print("Cube tapped")
            newbot.score += 1
            newbot.happyQueue += 1
            newbot.angryQueue = 0
            cols = [cozmo.lights.off_light] * 4
            cubes[index].set_light_corners(*cols)
        except asyncio.TimeoutError:
            newbot.happyQueue = 0
            newbot.angryQueue += 1
            cols = [cozmo.lights.off_light] * 4
            cubes[index].set_light_corners(*cols)
            print("No-one tapped our cube :-(")
            pass
        except cozmo.exceptions.RobotBusy:
            pass
    newbot.happyQueue = 0
    newbot.angryQueue = 0

'''
Start of remote _control
'''

def create_default_image(image_width, image_height, do_gradient=False):
    '''Create a place-holder PIL image to use until we have a live feed from Cozmo'''
    image_bytes = bytearray([0x70, 0x70, 0x70]) * image_width * image_height

    if do_gradient:
        i = 0
        for y in range(image_height):
            for x in range(image_width):
                image_bytes[i] = int(255.0 * (x / image_width))  # R
                image_bytes[i + 1] = int(255.0 * (y / image_height))  # G
                image_bytes[i + 2] = 0  # B
                i += 3

    image = Image.frombytes('RGB', (image_width, image_height), bytes(image_bytes))
    return image

app = Flask(__name__, static_folder='static')
remote_control_cozmo = None
_default_camera_image = create_default_image(320, 240)
robot = None

class RemoteControlCozmo:
    def __init__(self, coz):
        self.cozmo = coz
        self.drive_forwards = 0
        self.drive_back = 0
        self.turn_left = 0
        self.turn_right = 0
        self.lift_up = 0
        self.lift_down = 0
        self.head_up = 0
        self.head_down = 0

        self.go_fast = 0
        self.go_slow = 0

        self.action_queue = []

        self.cubes = []
        self.cube = None

    def handle_key(self, key_code, is_shift_down, is_ctrl_down, is_alt_down, is_key_down):
        '''Called on any key press or release
           Holding a key down may result in repeated handle_key calls with is_key_down==True
        '''

        # Update desired speed / fidelity of actions based on shift/alt being held
        was_go_fast = self.go_fast
        was_go_slow = self.go_slow

        self.go_fast = is_shift_down
        self.go_slow = is_alt_down

        speed_changed = (was_go_fast != self.go_fast) or (was_go_slow != self.go_slow)

        # print("handle_key", key_code, "is_key_down", is_key_down)
        # robot.say_text("hi").wait_for_completed()

        # Update state of driving intent from keyboard, and if anything changed then call update_driving
        update_driving = True
        if key_code == 12:
            self.drive_forwards = is_key_down
        elif key_code == 13:
            self.drive_back = is_key_down
        elif key_code == 14:
            self.turn_left = is_key_down
        elif key_code == 15:
            self.turn_right = is_key_down
        else:
            if not speed_changed:
                update_driving = False

        # Update state of lift move intent from keyboard, and if anything changed then call update_lift
        update_lift = True
        if key_code == 3:
            self.lift_up = is_key_down
            if self.lift_up:
                self.lift_down = False
        elif key_code == 0:
            self.lift_down = is_key_down
            if self.lift_down:
                self.lift_up = False
        else:
            if not speed_changed:
                update_lift = False

        # Update state of head move intent from keyboard, and if anything changed then call update_head
        update_head = True
        if key_code == 2:
            self.head_up = is_key_down
        elif key_code == 1:
            self.head_down = is_key_down
        else:
            if not speed_changed:
                update_head = False

        # Update driving, head and lift as appropriate
        if update_driving:
            self.update_driving()
        if update_lift:
            self.update_lift()
        if update_head:
            self.update_head()

    def func_to_name(self, func):
        if func == self.try_say_text:
            return "say_text"
        elif func == self.try_play_anim:
            return "play_anim"
        else:
            return "UNKNOWN"

    def action_to_text(self, action):
        func, args = action
        print (self.func_to_name(func))
        return self.func_to_name(func) + "( " + str(args) + " )"

    def action_queue_to_text(self, action_queue):
        out_text = ""
        i = 0
        for action in action_queue:
            out_text += "[" + str(i) + "] " + self.action_to_text(action)
            i += 1
        print ("action_queue_to_text", out_text)
        return out_text

    def queue_action(self, new_action):
        if len(self.action_queue) > 10:
            self.action_queue.pop(0)
        self.action_queue.append(new_action)

    def try_say_text(self, text_to_say):
        try:
            self.cozmo.say_text(text_to_say)
            return True
        except cozmo.exceptions.RobotBusy:
            return False

    def say_text(self, text_to_say):
        self.queue_action((self.try_say_text, text_to_say))
        self.update()

    def update(self):
        '''Try and execute the next queued action'''
        if len(self.action_queue) > 0:
            queued_action, action_args = self.action_queue[0]
            if queued_action(action_args):
                self.action_queue.pop(0)

    def pick_speed(self, fast_speed, mid_speed, slow_speed):
        if self.go_fast:
            if not self.go_slow:
                return fast_speed
        elif self.go_slow:
            return slow_speed
        return mid_speed

    def update_driving(self):
        drive_dir = (self.drive_forwards - self.drive_back)

        if (drive_dir > 0.1) and self.cozmo.is_on_charger:
            # cozmo is stuck on the charger, and user is trying to drive off - issue an explicit drive off action
            try:
                self.cozmo.drive_off_charger_contacts().wait_for_completed()
            except cozmo.exceptions.RobotBusy:
                # Robot is busy doing another action - try again next time we get a drive impulse
                pass

        turn_dir = (self.turn_right - self.turn_left)

        if drive_dir < 0:
            # It feels more natural to turn the opposite way when reversing
            turn_dir = -turn_dir

        # forward_speed = self.pick_speed(450, 225, 150)
        speed_up = score*100;
        forward_speed = self.pick_speed(150+speed_up, 50+speed_up, 50+speed_up)
        turn_speed = self.pick_speed(75, 25, 25)

        l_wheel_speed = (drive_dir * forward_speed) + (turn_speed * turn_dir)
        r_wheel_speed = (drive_dir * forward_speed) - (turn_speed * turn_dir)

        self.cozmo.drive_wheels(l_wheel_speed, r_wheel_speed, l_wheel_speed * 4, r_wheel_speed * 4)

    def update_lift(self):
        lift_speed = self.pick_speed(2, 1, 0.5)
        lift_vel = (self.lift_up - self.lift_down) * lift_speed
        # print("lift_vel", lift_vel)
        # print("self.lift_up", self.lift_up)
        # print("self.lift_down", self.lift_down)
        self.cozmo.move_lift(lift_vel)

    def update_head(self):
        head_speed = self.pick_speed(2, 1, 0.5)
        head_vel = (self.head_up - self.head_down) * head_speed
        self.cozmo.move_head(head_vel)

    def init_game(self):
        print("init_game")
        self.welcome()
        return

    def end_game(self):
        print("end_game")
        return

    def set_cube_light(self):
        print("set_cube_light")
        if self.cubes:
            for cube in self.cubes:
                cube.set_lights(cozmo.lights.blue_light.flash())

    def set_cube_light_off(self):
        print("set_cube_light_off")
        if self.cubes:
            for cube in self.cubes:
                cube.set_lights_off()

    def place_cube(self):
        return

    def pick_up_cube(self):
        return

    def welcome(self):
        print("welcome")
        #self.cozmo.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE)
        #self.cozmo.set_lift_height(0.0).wait_for_completed()
        #self.cozmo.say_text("Hello").wait_for_completed()
        self.cozmo.set_all_backpack_lights(cozmo.lights.blue_light)
        # self.cozmo.say_text("Hello, nice to meet you. My name is Cozmo. I am a really stupid robot.").wait_for_completed()

    def bye(self):
        print("bye")
        self.cozmo.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE).wait_for_completed()
        self.cozmo.set_lift_height(0.0).wait_for_completed()
        self.cozmo.say_text("I need a rest now. Bye.").wait_for_completed()

    def celebrate_it(self):
        anim = self.cozmo.play_anim_trigger(cozmo.anim.Triggers.OnSpeedtapGameCozmoWinHighIntensity)
        anim.wait_for_completed()

        self.cozmo.drive_wheels(150, 150, duration=1)

        # move head fully up. and lift down to the bottom, to make it easy to see Cozmo's face
        self.cozmo.set_lift_height(0.0).wait_for_completed()
        self.cozmo.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()

        self.cozmo.say_text("You are awesome").wait_for_completed()

        duration_s = 0.1
        duration_s_long = 3.0

        images = [0 for i in range(3)]
        for i in range(3):
            # load an image and resize it to Cozmo's screen dimensions
            images[i] = Image.open("images/heart_{}.png".format(i))
            images[i] = images[i].resize(cozmo.lcd_face.dimensions(), Image.BICUBIC)
            # convert the image to the format used bt the lcd screen
            images[i] = cozmo.lcd_face.convert_image_to_screen_data(images[i], invert_image=True)
            # display the image on Cozmo's face for duration_s seconds
            if i == 2:
                duration_s = duration_s_long
            self.cozmo.display_lcd_face_image(images[i], duration_s * 1000.0)
            # time.sleep(duration_s)


def handle_key_event(key_request, is_key_down):
    try:
        message = json.loads(key_request.data.decode("utf-8"))
    except ValueError as e:  # includes simplejson.decoder.JSONDecodeError
        print("Decoding JSON has failed: %s" % e)

    # print("handle_key_event",remote_control_cozmo.cozmo)

    if remote_control_cozmo:
        remote_control_cozmo.handle_key(key_code=(message['keyCode']), is_shift_down=message['hasShift'],
                                        is_ctrl_down=message['hasCtrl'], is_alt_down=message['hasAlt'],
                                        is_key_down=is_key_down)

    else:

        print ("remote_control_cozmo not exist")

    return ""


@app.route('/celebrate')
def celebrate():
    # if remote_control_cozmo:
    #     remote_control_cozmo.celebrate_it()
    return ""


@app.route('/pickup')
def pickup():
    print("pickup")
    if remote_control_cozmo:
        remote_control_cozmo.pick_up_cube()
    return ""


@app.route('/place')
def place():
    print("place")
    if remote_control_cozmo:
        remote_control_cozmo.place_cube()
    return ""


@app.route('/updateCozmo', methods=['POST'])
def handle_updateCozmo():
    '''Called very frequently from Javascript to provide an update loop'''
    if remote_control_cozmo:
        remote_control_cozmo.update()
    return ""


@app.route("/cozmoImage")
def handle_cozmoImage():
    '''Called very frequently from Javascript to request the latest camera image'''
    if remote_control_cozmo:
        image = remote_control_cozmo.cozmo.world.latest_image
        if image:
            return flask_helpers.serve_pil_image(image.raw_image)
    return flask_helpers.serve_pil_image(_default_camera_image)


@app.route('/keydown', methods=['POST'])
def handle_keydown():
    '''Called from Javascript whenever a key is down (note: can generate repeat calls if held down)'''
    # robot.say_text("handle keydown").wait_for_completed()
    return handle_key_event(request, is_key_down=True)


@app.route('/keyup', methods=['POST'])
def handle_keyup():
    '''Called from Javascript whenever a key is released'''
    return handle_key_event(request, is_key_down=False)


@app.route('/')
def hello_world():
    return app.send_static_file('index_black.html')


@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)


async def run(sdk_conn):
    cube = None
    robot = await sdk_conn.wait_for_robot()

    robot.set_all_backpack_lights(cozmo.lights.blue_light)
    await robot.say_text("Hello, my name is Cozmo. Please charge me up by tapping cubes.").wait_for_completed()
    await robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE/5).wait_for_completed()

    print(cozmo.robot.MAX_HEAD_ANGLE, " ", cozmo.robot.MIN_HEAD_ANGLE)

    print("Got initialized Cozmo")

    try:
        cubes = await robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=300)
    except asyncio.TimeoutError:
        print("Didn't find a cube :-(")
        return

    newbot = SingBot(robot)
    newbot.start_speaking()

    cols = [cozmo.lights.off_light] * 4
    for cube in cubes:
        cube.set_light_corners(*cols)

    await cube_tap(cubes, newbot, 20, 2.5)
    await asyncio.sleep(3.1)
    global score
    score = 0
    await newbot.evaluate()
    await asyncio.sleep(2)
    await start_end_sequence(cubes)
    score = newbot.score / newbot.total

def run2(sdk_conn):
    global remote_control_cozmo
    robot = sdk_conn.wait_for_robot()
    remote_control_cozmo = RemoteControlCozmo(robot)
    remote_control_cozmo.init_game()
    remote_control_cozmo.celebrate_it()
    flask_helpers.run_flask(app)

if __name__ == '__main__':
    cozmo.setup_basic_logging()
    try:
        cozmo.connect_with_tkviewer(run)
        cozmo.connect(run2)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
