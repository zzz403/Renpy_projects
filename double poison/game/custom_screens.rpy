screen study_room_hover():
    frame:
        background "#FFFFFF"
        xfill True
        yfill True

    imagemap:
        xalign 0.5
        ground "location_selection.png"
        hover "location_selection_hover.png"
        hotspot (50, 160, 650, 450) action Jump("desk_top")
        hotspot (50, 620, 550, 400) action Jump("floor_stain")
        hotspot (600, 620, 650, 400) action Jump("chair_backpack")

screen camera_preview_ui():

    # 全屏黑背景
    frame:
        background "#000"
        xysize (config.screen_width, config.screen_height)

    # 中上方预览图
    if aperture_group[aperture] == "F5.6":
        add "camera/[current_location]-5.6.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F8":
        add "camera/[current_location]-8.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F11":
        add "camera/[current_location]-11.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F16":
        add "camera/[current_location]-16.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)

    # imagemap 实现底部按钮 hover 切换效果
    imagemap:
        ground "camera/camera-idle.png"
        hover  "camera/camera-hover.png"
        xpos 0.5 ypos 1.0 anchor (0.5, 1.0)

        # left button
        hotspot (1555, 830, 110, 110) action SetVariable("theme_x", theme_x + 0.02)

        # right button
        hotspot (1755, 829, 110, 110) action SetVariable("theme_x", theme_x - 0.02)

        # up button
        hotspot (1655, 729, 110, 110) action SetVariable("theme_y", theme_y + 0.02)

        # down button
        hotspot (1658, 929, 110, 110) action SetVariable("theme_y", theme_y - 0.02)

        # zoom in button
        hotspot (1455, 740, 110, 110) action If(
            (focal_len == "50mm" and theme_zoom < 2.0) or (focal_len == "105mm" and theme_zoom < 4.0),
            SetVariable("theme_zoom", theme_zoom + 0.02)
        )

        # zoom out button
        hotspot (1460, 929, 110, 110) action If(
            (focal_len == "50mm" and theme_zoom > 1.0) or (focal_len == "105mm" and theme_zoom > 3.0),
            SetVariable("theme_zoom", theme_zoom - 0.02)
        )

        
        # Aperture less button
        hotspot (1100, 890, 110, 110) action SetVariable("aperture", max(0, aperture - 1))

        # Aperture more button
        hotspot (1300, 890, 110, 110) action SetVariable("aperture", min(3, aperture + 1))

        text "[aperture_group[aperture]]" xpos 0.658 ypos 0.88 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        # take photo button
        hotspot (850, 780, 250, 250) action [
            Hide("camera_preview_ui"),
            Show("study_room3_inventory"),
            Function(renpy.jump, "{}_label".format(current_location)),
        ]

        # iso button +
        hotspot (550, 890, 110, 110) action SetVariable("iso_index", max(0, iso_index - 1))

        # iso button -
        hotspot (720, 890, 110, 110) action SetVariable("iso_index", min(4, iso_index + 1))

        text "[iso_group[iso_index]]" xpos 0.352 ypos 0.87 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        # switch focal length button 50mm
        hotspot (10, 730, 500, 150) action [ 
            SetVariable("focal_len", "50mm"), 
            SetVariable("theme_zoom", clamp(theme_zoom, 1.0, 2.0)) 
        ]
        # switch focal length button 105mm
        hotspot (10, 900, 500, 150) action [ 
            SetVariable("focal_len", "105mm"), 
            SetVariable("theme_zoom", clamp(theme_zoom, 3.0, 4.0)) 
        ]

        text "50mm" xpos 0.15 ypos 0.74 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        text "105mm" xpos 0.15 ypos 0.897 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        # frame:
        #     background "#e61212"
        #     xpos 10
        #     ypos 900
        #     xsize 500
        #     ysize 150

init python:
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))



## Desktop Interaction Screen ###############################
screen desk_top_hover():

    imagemap:
        xalign 0.5
        ground "desk_top.png"
        hover "desk_top_hover.png"

        if desk_top_marks["marker1"] and desk_top_marks["marker2"] and desk_top_marks["marker3"] and desk_top_marks["marker4"] and desk_top_marks["marker5"]:
            hotspot (180, 400, 275, 520) action Jump("coffee_cup_theme_label")
            hotspot (450, 632, 820, 320) action Jump("laptop_investigate")
            hotspot (1280, 820, 290, 290) action Jump("note_investigate")
            hotspot (1320, 130, 500, 670) action Jump("water_bottle_investigate")
            hotspot (900, 400, 400, 231) action Jump("poision_pill_investigate")
        else:
            hotspot (180, 400, 275, 520) action Jump("desk_top")
            hotspot (450, 632, 820, 320) action Jump("desk_top")
            hotspot (1280, 820, 290, 290) action Jump("desk_top")
            hotspot (1320, 130, 500, 670) action Jump("desk_top")
            hotspot (900, 400, 400, 231) action Jump("desk_top")
    
    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection")
    
    if desk_top_marks["marker1"]:
        add "em1.png" xpos 0.07 ypos 0.7
    if desk_top_marks["marker2"]:
        add "em2.png" xpos 0.26 ypos 0.75
    if desk_top_marks["marker3"]:
        add "em3.png" xpos 0.63 ypos 0.8
    if desk_top_marks["marker4"]:
        add "em3.png" xpos 0.65 ypos 0.6
    if desk_top_marks["marker5"]:
        add "em3.png" xpos 0.48 ypos 0.45

screen chat_viewer(images):
    default index = 0

    key "K_UP" action If(index > 0, SetScreenVariable("index", index - 1))
    key "K_DOWN" action If(index < len(images) - 1, SetScreenVariable("index", index + 1))
    key "K_ESCAPE" action Return()

    frame:
        background "desk_top.png"
        yfill True
        add Solid("#00000080") 

    add images[index] xpos 0.5 ypos 0.5 anchor (0.5, 0.5) zoom 1.4

    text "[index+1]/[len(images)]" xpos 0.95 ypos 0.95 size 30

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top")

screen coffee_cup_theme_viewer():
    default note_book_opened = False

    frame:
        background "coffee_cup_theme.png"
        yfill True
    

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("desk_top")
    if sample_vial_state == "empty":
        add "sample_bottle_open.png" xpos 0.29 ypos 0.5 anchor (0.5, 0.5) zoom 0.4
    elif sample_vial_state == "coffee":
        add "sample_bottle_coffee.png" xpos 0.29 ypos 0.5 anchor (0.5, 0.5) zoom 0.5
    
    # frame:
    #         background "#e61212"
    #         xpos 350
    #         ypos 250
    #         xsize 260
    #         ysize 400

    # imagebutton:
    #     xpos 0.83 ypos 0.4
    #     idle "pipette_idle.png"
    #     hover "pipette_hover.png"
    #     if not coffee_cup_evidence["sample_taken"]:
    #         action [SetDict(coffee_cup_evidence, "sample_taken", True)]


screen photo_flying():
    add "coffee_cup_theme_small.png" at photo_slide_out
    timer 1.3 action Hide("photo_flying")


init python:
    import datetime

screen observation_form():
    
    imagemap:
        xalign 0.3
        ground "observation/stand_idle.png"
        hover "observation/stand_hover.png"

        text "[datetime.date.today().strftime('%Y-%m-%d')]" xalign 0.43 yalign 0.34 size 39 color "#363636" font "ConcertOne-Regular.ttf"

        input id "in1" value exhibit_no length 8 xalign 0.55 yalign 0.45 font "ConcertOne-Regular.ttf" size 39 color "#363636"

        input id "in2" value picked_color length 8 xalign 0.55 yalign 0.55 font "ConcertOne-Regular.ttf" size 39 color "#363636"

    # frame:
    #     background "#e61212"
    #     xpos 400
    #     ypos 300
    #     xsize 550
    #     ysize 120

### floor_stain Interaction Screen ###############################

screen floor_stain_hover():
    imagemap:
        xalign 0.5
        ground "desk_under_idle.png"
        hover "desk_under_hover.png"

        hotspot (600, 400, 550, 550) action Jump("floor_stain_investigate")

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection")


## chair_backpack_hover Screen ###############################

screen chair_backpack_hover():
    imagemap:
        xalign 0.5
        ground "desk_bag.png"
        hover "desk_bag_hover.png"

        hotspot (350, 150, 600, 900) action Jump("chair_backpack_investigate")

    imagebutton:
        xpos 0.98
        ypos 0.95
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action Jump("location_selection")