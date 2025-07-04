default current_location = "menu"
# ─── CAMERA  ────────────────────────────
default theme_x = 0.5
default theme_y = 0.3

default theme_zoom = 2

default aperture = 1
default aperture_group = ["F5.6", "F8", "F11", "F16"]

default iso_index = 1
default iso_group = [100, 200, 300, 400, 800]
default iso_to_alpha = {100: 0.2, 200: 0.4, 300: 0.6, 400: 0.8, 800: 1.0}

default focal_len = "50mm"

default photo_data = []

default show_animation_camera = False
default photo_show_index = 0


# example location dictionary
default location_name_dict = {
    "coffee_cup_theme": "Coffee Cup Theme",
    "desk_top": "Desk Top",
    "laptop": "Laptop",
    "note": "Note",
    "pill": "The Pill Bottle",
    "water_bottle": "Water Bottle",
    "note_fingerprint": "Note with Fingerprint",
    "floor_stain": "Floor Stain",
    "coffee_on_floor": "Coffee on Floor",
    "hair": "Hair on the Floor",
    "backpack": "Backpack",
}

init python:
    from math import ceil

    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))
    def safe_camera_data(theme_x, theme_y, theme_zoom, aperture, iso_index, focal_len):
        print("Saving camera data...")
        global photo_data
        photo_data.append({
            "location": current_location,
            "iso_index": iso_index,
            "aperture_index": aperture,
            "zoom_level": theme_zoom,
            "lens": focal_len,
            "theme_x": theme_x,
            "theme_y": theme_y
        })
    def open_photo_viewer_with_index(index):
        global photo_show_index
        global photo_data
        photo_show_index = index
        if index >= 0 and index < len(photo_data):
            renpy.jump("photo_viewer_label")

label photo_viewer_label:
    call screen photo_viewer(index=photo_show_index)

label photo_album_label:
    call screen photo_album


screen camera_preview_ui():
    frame:
        background "#000"
        xysize (config.screen_width, config.screen_height)

    # preview camera UI
    if aperture_group[aperture] == "F5.6":
        add "camera/[current_location]-5.6.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F8":
        add "camera/[current_location]-8.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F11":
        add "camera/[current_location]-11.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)
    elif aperture_group[aperture] == "F16":
        add "camera/[current_location]-16.png" xpos theme_x ypos theme_y anchor (0.5 , 0.5) zoom theme_zoom alpha iso_to_alpha.get(iso_group[iso_index], 1.0)

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
            Function(safe_camera_data, theme_x, theme_y, theme_zoom, aperture, iso_index, focal_len),
            SetVariable("show_animation_camera", True),
            Function(renpy.jump, "{}_label".format(current_location))
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

        text "Current Focal Length: \n        [focal_len]" xpos 0.125 ypos 0.6 anchor (0.5, 0.5) size 40 color "#ffffff" font "ConcertOne-Regular.ttf"

        text "50mm" xpos 0.15 ypos 0.74 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"

        text "105mm" xpos 0.15 ypos 0.897 anchor (0.5, 0.5) size 63 color "#ffffff" font "ConcertOne-Regular.ttf"


screen photo_album():

    add Solid("#000")

    default photo_index = 0
    default current_page = ceil(photo_index / 6.0)
    default total_photos = len(photo_data) if photo_data else 0
    default total_pages = ceil(len(photo_data) / 6.0) if photo_data else 0
    default current_location_local = "{}_label".format(current_location)

    default photo_location_list =[(440, 350), (950, 350), (1480, 350), (440, 780), (950, 780), (1480, 780)]
    
    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ p = photo_data[idx]
            $ aperture_number = aperture_group[p["aperture_index"]].replace("F", "")
            $ img_path = "camera/{}-{}.png".format(p["location"], aperture_number)
            $ alpha_value = iso_to_alpha.get(iso_group[p["iso_index"]], 1.0)
            $ zoom_value = p["zoom_level"] / 2.3
            $ location_name = p["location"]

            
            viewport:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xmaximum 400
                ymaximum 300
                draggable False
                mousewheel False
                add img_path xpos 0 ypos 0 zoom zoom_value alpha alpha_value
        
    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]

            button:
                xpos x
                ypos y
                anchor (0.5, 0.5)
                xsize 400
                ysize 300
                background None
                action Function(open_photo_viewer_with_index, idx)

    imagemap:
        ground "camera/photographs-idle.png"
        # hover "desk_top_hover.png"
        hover "camera/photographs-hover.png"

        # if desk_top_marks["marker1"] and desk_top_marks["marker2"] and desk_top_marks["marker3"] and desk_top_marks["marker4"] and desk_top_marks["marker5"]:
        if photo_index < total_photos:
            hotspot (230, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 0)
        if photo_index + 1 < total_photos:
            hotspot (720, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 1)
        if photo_index + 2 < total_photos:
            hotspot (1210, 120, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 2)

        if photo_index + 3 < total_photos:
            hotspot (230, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 3)
        if photo_index + 4 < total_photos:
            hotspot (720, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 4)
        if photo_index + 5 < total_photos:
            hotspot (1210, 570, 460, 460) action Function(open_photo_viewer_with_index, photo_index + 5)

    for i in range(6):
        if photo_data and photo_index + i < len(photo_data):
            $ idx = photo_index + i
            $ x, y = photo_location_list[i]
            $ p = photo_data[idx]
            $ location_name = p["location"]

            text "[location_name_dict[location_name]]" xpos x ypos y+200 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    text "[current_page + 1] / [total_pages]" xpos 0.5 ypos 0.95 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action [
            Show("study_room3_inventory"),
            Hide("photo_album"),
            Function(renpy.jump, "{}_label".format(current_location)),
        ]

    if photo_index > 0:
        imagebutton:
            xpos 0.12
            ypos 0.95
            at Transform(zoom=0.8)
            anchor (1.0, 1.0)
            idle "left_icon-idle.png"
            hover "left_icon-hover.png"
            action [SetScreenVariable("photo_index", max(0, photo_index - 6)),
                    SetScreenVariable("current_page", ceil((photo_index - 6) / 6.0)),
                    Function(renpy.restart_interaction)]
    if photo_index + 6 < total_photos:
        imagebutton:
            xpos 0.98
            ypos 0.95
            at Transform(zoom=0.8)
            anchor (1.0, 1.0)
            idle "right_icon-idle.png"
            hover "right_icon-hover.png"
            action [SetScreenVariable("photo_index", photo_index + 6), 
                    SetScreenVariable("current_page", ceil((photo_index + 6) / 6.0)),
                    Function(renpy.restart_interaction)]

screen photo_viewer(index=photo_show_index):
    tag photo_viewer
    modal True

    add Solid("#000")

    $ info = photo_data[index]
    $ aperture_value = aperture_group[info["aperture_index"]]
    $ zoom_value = "{:.1f}x".format(info["zoom_level"]* 0.8) 
    $ lens_value = info["lens"]
    $ iso_value = iso_group[info["iso_index"]]

    $ aperture_number = aperture_group[info["aperture_index"]].replace("F", "")
    $ img_path = "camera/{}-{}.png".format(info["location"], aperture_number)

    $ x = round(500 + 900 * info["theme_x"])
    $ y = round(330 + 670 * info["theme_y"])
    
    add img_path xpos x ypos y zoom info["zoom_level"] anchor (0.5, 0.5) alpha iso_to_alpha.get(iso_value, 1.0)
    
    add "camera/single-photo.png"

    text "Taken at [location_name_dict[info['location']]]" xpos 0.5 ypos 0.16 anchor (0.5, 0.5) size 45 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "Aperture: [aperture_value]" xpos 0.5 ypos 0.9 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "Lens: [lens_value]" xpos 0.3 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"
    text "ISO: [iso_value]" xpos 0.73 ypos 0.90 anchor (0.5, 0.5) size 40 color "#0f0f0f" font "ConcertOne-Regular.ttf"

    imagebutton:
        xpos 0.1
        ypos 0.2
        anchor (1.0, 1.0)
        idle "back_button.png"
        hover "back_button_hover.png"
        at button_zoom
        action [
            Hide("photo_viewer"),
            Jump("photo_album_label"),
        ]


screen photo_flying():
    default aperture_index_local = photo_data[-1]["aperture_index"]
    default aperture_number_local = aperture_group[aperture_index_local].replace("F", "")
    add "camera/[current_location]-[aperture_number_local].png" xpos theme_x ypos theme_y anchor (0.5, 0.5) alpha iso_to_alpha.get(iso_group[photo_data[-1]["iso_index"]], 1.0) at photo_slide_out
    timer 1.1 action [
        Hide("photo_flying"),
        SetVariable("show_animation_camera", False),
    ]

transform photo_slide_out:
    xpos 0.5 ypos 1.0 zoom 0.5
    linear 1.0 xpos 0 ypos -0.15 zoom 0.2