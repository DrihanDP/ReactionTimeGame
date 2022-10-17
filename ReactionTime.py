# To run the app, the app name will need to be changed to 'main'. 
# It will then need to be placed on the root directory of an SD and inserted into a VBOX Touch.
# Once the VBOX Touch is powered, the app will load over the top of the main VBOX Touch app.

import gui
import vts

class GV:
    reaction_times_total = 0
    start_sequence = False
    is_out = False
    pressed = False
    chrono = vts.Chrono()
    reaction_t = None
    jump_start = False
    restart_pressed = False
    results_page_buttton_pressed = False
    reaction_time_list = []
    reset_data_button_pressed = True
    average_reaction_time = 0
    fastest_time = 0
    UTCTime_list = []


class scroll_controller:
    swipe_timer = None
    swipe_pos = 0
    scroll_point = 0

    @classmethod
    def set_scroll_pos(cls, pos):
        gui_input_list[cls.scroll_point][0] = gui.DL_VERTEX_TRANSLATE_Y(pos)


def vsync_cb(l):
    gui.redraw()


def swipe_cb(l, swiping):
    if swiping:
        scroll_controller.swipe_timer = vts.Timer(100, True)
        scroll_controller.swipe_timer.set_callback(scroll_cb)
    else:
        try:
            scroll_controller.swipe_pos += gui.swipe_info().dy
            if scroll_controller.swipe_pos > 0: scroll_controller.swipe_pos = 0
            if scroll_controller.swipe_pos < -480: scroll_controller.swipe_pos = -480
            scroll_controller.set_scroll_pos(scroll_controller.swipe_pos)
            scroll_controller.swipe_timer.set_callback(None)
            scroll_controller.swipe_timer.destroy()
        except TypeError:
            print("Tried to re-destroy Timer")
            pass


def scroll_cb():
    swipe = gui.swipe_info()
    scroll_controller.set_scroll_pos(scroll_controller.swipe_pos + swipe.dy)


def lights_generator():
        vts.leds(50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        vts.delay_ms(1250)
        yield
        vts.leds(50, 0, 0, 50, 0, 0, 0, 0, 0, 0, 0, 0)
        vts.delay_ms(1250)
        yield
        vts.leds(50, 0, 0, 50, 0, 0, 50, 0, 0, 0, 0, 0)
        vts.delay_ms(1250)
        yield
        vts.leds(50, 0, 0, 50, 0, 0, 50, 0, 0, 50, 0, 0)
        vts.delay_ms(rand_int())
        yield
        vts.leds(*([0] * 12))
        GV.chrono.restart()
        GV.is_out = True
        yield


def out_check():
    GV.start_sequence = False
    vts.leds(* ([0] * 12))
    vts.delay_ms(5000)
    stage = lights_generator()
    while (not GV.jump_start) and (not GV.is_out):
        next(stage)


def rand_int(start=750,end=3000):
    """Generate a random integer between set values"""
    while True:
        rand = vts.rand32() # built-in to generate 32 bit number
        value = int((end/4294967295) * rand) # max 32 bit integer is 4,294,967,295, divide by max value to get small percentage
        if start < value: # if value is below start value, the 'while' loop starts again
            return value


def results(a):
    if GV.is_out == True:
        GV.pressed = True
        GV.restart_pressed = False
        UTCTime = vts.clock_get()
        GV.UTCTime_list.append("{}:{}:{} - {}/{}/{}".format(UTCTime['hours'], UTCTime['minutes'], UTCTime['seconds'],
                                                            UTCTime['day of month'], UTCTime['month'], UTCTime['year'],))
        GV.reaction_t = GV.chrono.read() // 1000
        GV.reaction_time_list.append(GV.reaction_t)
        game_reaction = 'Reaction time: {} ms'.format(GV.reaction_t)
        vts.leds(* ([0, 50, 0] * 4))
        gui.show([
            [gui.PARAM_CLRCOLOR, gui.RGB(0, 150, 0)],
            [gui.CTRL_TEXT, 400, 160, 30, gui.OPT_CENTER, "It's lights out and away we go"],
            [gui.CTRL_TEXT, 400, 200, 30, gui.OPT_CENTER, game_reaction],
            [gui.CTRL_BUTTON, 300, 240, 200, 60, 30, 'Restart', restart_game],
            [gui.CTRL_BUTTON, 580, 400, 200, 60, 30, 'Results', results_page],
            
            ])
    else:
        GV.pressed = True
        GV.jump_start = True
        GV.restart_pressed = False
        gui.show([
            [gui.PARAM_CLRCOLOR, gui.RGB(255, 0, 0)],
            [gui.CTRL_TEXT, 400, 200, 30, gui.OPT_CENTER, "Jump start!"],
            [gui.CTRL_BUTTON, 300, 240, 200, 60, 30, 'Restart', restart_game],
        ])
        vts.leds(* ([255, 75, 0] * 4))


def restart_game(b):
    GV.restart_pressed = True
    GV.is_out = False
    GV.reaction_t = None
    GV.jump_start = False
    GV.pressed = False
    vts.leds(*[0] * 12)
    main()


def main_screen():
    gui.show([
        [gui.PARAM_CLRCOLOR, gui.RGB(0, 0, 0)],
        [gui.CTRL_BUTTON, 300, 180, 200, 100, 30, 'PRESS ME', results],
        [gui.CTRL_TEXT, 30, 0, 30, 0, 'Get ready, when the red lights go out press the button'],
        ])
    gui.redraw()


def reset_data(d):
    GV.reset_data_button_pressed = True
    GV.reaction_time_list = []
    GV.reaction_times_total = 0
    GV.UTCTime_list = []
    results_page(d)


def draw_results_page():
    global gui_input_list
    vts.leds(* ([0] * 12))
    gui_input_list = [
        [gui.EVT_VSYNC, vsync_cb],
        [gui.EVT_SWIPE, 50, swipe_cb],
        [gui.DL_COLOR_RGB(25, 110, 0)],
        [gui.PRIM_RECTS, [
            gui.DL_VERTEX2F(0, 80),
            gui.DL_VERTEX2F(400, 480)]
            ],
        [gui.DL_COLOR_RGB(25, 25, 25)],
        [gui.PRIM_RECTS, [
            gui.DL_VERTEX2F(400, 80),
            gui.DL_VERTEX2F(800, 480)]
            ],
        [gui.PRIM_LINE_STRIP, [
            gui.DL_COLOR_RGB(255, 255, 255),
            gui.DL_LINE_WIDTH(2),
            gui.DL_VERTEX2F(400, 80),
            gui.DL_VERTEX2F(400, 480)
        ]],
        [gui.DL_COLOR_RGB(255, 255, 255)],
        [gui.CTRL_TEXT, 425, 160, 30, 0, 'Average time: '],
        [gui.CTRL_TEXT, 425, 130, 30, 0, 'Fast time: '],
        [gui.DL_COLOR_RGB(0, 255, 0)],
        [gui.CTRL_TEXT, 780, 160, 30, gui.OPT_RIGHTX, "{} ms".format(GV.average_reaction_time)],
        [gui.CTRL_TEXT, 780, 130, 30, gui.OPT_RIGHTX, "{} ms".format(GV.fastest_time)], 
        [gui.DL_COLOR_RGB(255, 255, 255)],
        [gui.CTRL_BUTTON, 500, 240, 200, 60, 30, 'Restart', restart_game],
        [gui.CTRL_BUTTON, 500, 370, 200, 60, 30, 'Reset Data', reset_data],
        [gui.DL_VERTEX_TRANSLATE_Y(0)],
        ]

    scroll_controller.scroll_point = gui_input_list.index([gui.DL_VERTEX_TRANSLATE_Y(0)])
    for i, value in enumerate(GV.reaction_time_list):
        gui_input_list.append([gui.CTRL_TEXT, 20, 100 + i * 90, 30, 0, str(i + 1) + '. ' + str(value)+'ms'])

    for j, UTC in enumerate(GV.UTCTime_list):
        gui_input_list.append([gui.CTRL_TEXT, 20, 140 + j * 90, 30, 0, UTC])
        gui_input_list.append([gui.CTRL_TEXT, 5, 165 + j * 90, 30, 0, "-" * 26])

    gui_input_list.append([gui.DL_VERTEX_TRANSLATE_Y(0)])

    gui_input_list.append([gui.DL_COLOR_RGB(25, 25, 110)])
    gui_input_list.append([gui.PRIM_RECTS, [
                            gui.DL_VERTEX2F(0, 0),
                            gui.DL_VERTEX2F(800, 78)]])
    gui_input_list.append([gui.DL_COLOR_RGB(255, 255, 255)])
    gui_input_list.append([gui.CTRL_TEXT, 400, 40, 31, gui.OPT_CENTER, "Results page"])
    gui_input_list.append([gui.PRIM_LINE_STRIP, [
            gui.DL_COLOR_RGB(255, 255, 255),
            gui.DL_LINE_WIDTH(2),
            gui.DL_VERTEX2F(0, 80),
            gui.DL_VERTEX2F(800, 80),
        ]],)

    gui.show(gui_input_list)


def results_page(j):
    GV.results_page_buttton_pressed = True
    GV.start_sequence = False
    if len(GV.reaction_time_list) != 0:
        GV.reaction_times_total = 0
        for reaction_times in GV.reaction_time_list:
            GV.reaction_times_total = int(reaction_times) + GV.reaction_times_total
        GV.average_reaction_time = int(GV.reaction_times_total / len(GV.reaction_time_list))
    else:
        GV.average_reaction_time = ""
    if len(GV.reaction_time_list) != 0:
        GV.fastest_time = sorted(GV.reaction_time_list)[0]
    else:
        GV.fastest_time = ""
    vts.leds(*([0] * 12))
    draw_results_page()


def main():
    GV.pressed = False
    GV.restart_pressed = False
    GV.results_page_buttton_pressed = False
    GV.reset_data_button_pressed = False
    main_screen()
    GV.start_sequence = True

if __name__ == '__main__':
    main()

while True:
    if GV.start_sequence:
        out_check()