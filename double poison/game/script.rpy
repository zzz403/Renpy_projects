default coffee_cup_evidence = {
    "photo_taken": False,
    "note_taken": False,
    "sample_taken": False,
    "bagged": False
}

default note_book_opened = False

default environment_SM = SpriteManager(event = environmentEvents)
default environment_sprites = []
default environment_items = ["lantern", "tape"] # holds environment items
default environment_item_names = [] # holds environment item names


default toolbox_SM              = SpriteManager(update=toolboxUpdate, event=toolboxEvents)
default toolbox_sprites         = []    # 存放所有 toolbox 精灵
default toolbox_items           = []    # 存放所有 toolbox 物品
default toolbox_db_enabled      = False # 是否可向下翻页
default toolbox_ub_enabled      = False # 是否可向上翻页

default toolbox_slot_size       = (int(215/2), int(196/2))
default toolbox_slot_padding    = 120/2
default toolbox_first_slot_x    = 105
default toolbox_first_slot_y    = 300
default toolbox_drag            = False

# ─── TOOLBOX POP-UP 展开栏 ────────────────────────────
default toolboxpop_SM           = SpriteManager(update=toolboxPopUpdate, event=toolboxPopupEvents)
default toolboxpop_sprites      = []
default toolboxpop_items        = []
default toolboxpop_db_enabled   = False
default toolboxpop_ub_enabled   = False

default toolboxpop_slot_size    = (int(215/2), int(196/2))
default toolboxpop_slot_padding = 120/2
default toolboxpop_first_slot_x = 285
default toolboxpop_first_slot_y = 470
default toolboxpop_drag         = False

# ─── INVENTORY 证据栏 初始化 ────────────────────────────

default inventory_SM            = SpriteManager(update=inventoryUpdate, event=inventoryEvents)
default inventory_sprites       = []    # 存放所有 evidence 精灵
default inventory_items         = []    # 存放 evidence 物品
# 如果你用了 item names 的弹出文本，也一并声明
default inventory_item_names    = ["Evidence marker",]

default inventory_db_enabled    = False # 向下翻页箭头是否可用
default inventory_ub_enabled    = False # 向上翻页箭头是否可用

default inventory_slot_size     = (int(215/2), int(196/2))
default inventory_slot_padding  = 120/2
default inventory_first_slot_x  = 105
default inventory_first_slot_y  = 300

default inventory_drag          = False # 默认不拖拽

default desk_top_finish_mark = False
default desk_top_marks = {
    "marker1": False,
    "marker2": False,
    "marker3": False,
    "marker4": False,
    "marker5": False,
    "marker6": False,
    "marker7": False,
    "marker8": False,
}

default current_location = "menu"


##########################################################################
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

default water_bottle_get = False

default pill_bottle_get = False

default hair_get = False

# example data:
# {
#     "location": "desk_top",
#     "iso_index": 1,
#     "aperture_index": 1,
#     "zoom_level": 1.0,
#     "lens": "50mm",
#     "theme_x": 0.5,
#     "theme_y": 0.3,
# }

default show_animation_camera = False
default photo_show_index = 0

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
##########################################################################

default exhibit_no = ""
default picked_color = ""
default color_choice       = None
default show_color_picker  = False
default dropper_state = "empty"
default sample_vial_state = "not_taken"


##############################################################################
default scalebar_state = False

init python:
    # 定义图片序号列表
    manga_list = [ "manga%d" % i for i in range(8) ]

transform manga_zoom_begin:
    # 从 40% 大小缓入到 60%
    zoom 0.1
    xalign 0.5
    yalign 0.5
    # 纯白背景
    linear 0.3 zoom 0.6

transform manga_zoom:
    # 从 60% 大小缓入到 80%
    zoom 0.6
    xalign 0.5
    yalign 0.5

transform white_zoom:
    zoom 10

image manga0 = "manga0.png"
image manga1 = "manga1.png"
image manga2 = "manga2.png"
image manga3 = "manga3.png"
image manga4 = "manga4.png"
image manga5 = "manga5.png"
image manga6 = "manga6.png"
image manga7 = "manga7.png"

init python:
    def on_color_chosen(color):
        global picked_color
        picked_color = color
        renpy.hide_screen("color_picker")

label start:
    jump show_manga_sequence
    return

label show_manga_sequence:
    # i 用来遍历 manga_list
    $ i = 0
    # 纯白 background zoom 6
    scene white at white_zoom
    show manga0 at manga_zoom_begin
    pause
    $ i += 1
    while i < len(manga_list):
        # 显示当前图片，并套用 zoom 动画
        show expression manga_list[i] at manga_zoom
        # 等待玩家点击或按键
        pause
        # 隐藏当前图片
        hide expression manga_list[i]

        # 进入下一张
        $ i += 1

    # 全部展示完毕后返回
    jump toolbox_init

label toolbox_init:
    # Initialize the toolbox with items
    python:
        # adds tape and ziploc bag to inventory
        addToInventory(["evidence_bag"])
        addToInventory(["images"])
        # addToToolbox(["pvs_kit"])
        addToToolbox(["evidence_marker"])
        addToToolbox(["camera"])        
        # addToToolbox(["note_book"])
        addToToolbox(["dropper"])
        addToToolbox(["uv_light"]) 
        addToToolbox(["scalebar"])
        addToToolbox(["swab"])

    $environment_items = ["marker1", "marker2", "marker3", "marker4", "marker5"]

    python:
        for item in environment_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "desk_top"
            if item == "marker1": # coffee cup
                environment_sprites[-1].width = 275
                environment_sprites[-1].height = 520
                environment_sprites[-1].x = 180
                environment_sprites[-1].y = 400
            if item == "marker2": # laptop
                environment_sprites[-1].width = 820
                environment_sprites[-1].height = 320
                environment_sprites[-1].x = 450
                environment_sprites[-1].y = 632
            if item == "marker3": # note
                environment_sprites[-1].width = 290
                environment_sprites[-1].height = 290
                environment_sprites[-1].x = 1280
                environment_sprites[-1].y = 820
            if item == "marker4": # water bottle
                environment_sprites[-1].width = 500
                environment_sprites[-1].height = 670
                environment_sprites[-1].x = 1320
                environment_sprites[-1].y = 130
            if item == "marker5": # poison pill
                environment_sprites[-1].width = 400
                environment_sprites[-1].height = 231
                environment_sprites[-1].x = 900
                environment_sprites[-1].y = 400
    $environment_items.append("marker6") # coffee blood
    $environment_items.append("marker7") # hair
    python:
        new_items = ["marker6", "marker7"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "floor_stain"
            if item == "marker6": # coffee blood
                environment_sprites[-1].width = 550
                environment_sprites[-1].height = 550
                environment_sprites[-1].x = 600
                environment_sprites[-1].y = 400
            if item == "marker7": # hair
                environment_sprites[-1].width = 290
                environment_sprites[-1].height = 190
                environment_sprites[-1].x = 1000
                environment_sprites[-1].y = 800

    $environment_items.append("coffee_view_coffee_cup") # coffee cup theme
    $environment_items.append("coffee_view_sample_vial") # sample vial theme
    $environment_items.append("coffee_evidence_bottle") # coffee evidence bottle
    python:
        new_items = ["coffee_view_coffee_cup", "coffee_view_sample_vial","coffee_evidence_bottle"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "coffee_cup_theme"
            if item == "coffee_view_coffee_cup":
                environment_sprites[-1].width = 500
                environment_sprites[-1].height = 800
                environment_sprites[-1].x = 740
                environment_sprites[-1].y = 250
            elif item == "coffee_view_sample_vial":
                environment_sprites[-1].width = 260
                environment_sprites[-1].height = 400
                environment_sprites[-1].x = 350
                environment_sprites[-1].y = 250
            elif item == "coffee_evidence_bottle":
                environment_sprites[-1].width = 400
                environment_sprites[-1].height = 600
                environment_sprites[-1].x = 380
                environment_sprites[-1].y = 400

    $environment_items.append("fingerprint")
    python:
        new_items = ["fingerprint"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "note_fingerprint"
            if item == "fingerprint":
                environment_sprites[-1].width = 200
                environment_sprites[-1].height = 180
                environment_sprites[-1].x = 1100
                environment_sprites[-1].y = 300

    $environment_items.append("pill_bottle")
    python:
        new_items = ["pill_bottle"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "pill"
            if item == "pill_bottle":
                environment_sprites[-1].width = 1200
                environment_sprites[-1].height = 700
                environment_sprites[-1].x = 500
                environment_sprites[-1].y = 300

    $environment_items.append("water_bottle")
    python:
        new_items = ["water_bottle"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "water_bottle"
            if item == "water_bottle":
                environment_sprites[-1].width = 700
                environment_sprites[-1].height = 1080
                environment_sprites[-1].x = 800
                environment_sprites[-1].y = 0
    
    $environment_items.append("hair")
    python:
        new_items = ["hair"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "hair"
            if item == "hair":
                environment_sprites[-1].width = 800
                environment_sprites[-1].height = 600
                environment_sprites[-1].x = 700
                environment_sprites[-1].y = 300

    $environment_items.append("coffee_on_floor")
    python:
        new_items = ["coffee_on_floor"]
        for item in new_items:
            t = Transform(zoom = 0.5)
            environment_sprites.append(environment_SM.create(t))
            environment_sprites[-1].type = item
            environment_sprites[-1].location = "coffee_on_floor"
            if item == "coffee_on_floor":
                environment_sprites[-1].width = 800
                environment_sprites[-1].height = 900
                environment_sprites[-1].x = 700
                environment_sprites[-1].y = 300

    jump location_selection_label

label location_selection_label:
    $current_location = "location_selection"
    show screen study_room3_inventory
    call screen study_room_hover

    # call screen camera_preview_ui
    "Please select a location to explore."
    $ renpy.pause()

transform half_size:
    zoom 0.5

label desk_top_label:
    $current_location = "desk_top"
    
    if show_animation_camera:
        image theme_pic = "desk_top_full.png"
        scene theme_pic
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen desk_top_hover
    e "This is the desk top. You can see some books and a laptop here."

    # Add more interactions or choices here if needed.
    return

label floor_stain_label:
    $current_location = "floor_stain"
    if show_animation_camera:
        image floor_stain_theme = "desk_under_idle.png"
        scene floor_stain_theme
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen floor_stain_hover
    e "This is the floor stain. It looks like a coffee spill."
    return

label backpack_label:
    $current_location = "backpack"

    if show_animation_camera:
        image backpack_theme = "desk_bag.png"
        scene backpack_theme
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black
    

    call screen chair_backpack_hover
    e "This is the chair with a backpack on it. You can check the backpack for clues."
    return



label coffee_cup_theme_label:
    $current_location = "coffee_cup_theme"
    
    if show_animation_camera:
        image coffee_cup_theme = "coffee_cup_theme.png"
        scene coffee_cup_theme
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen coffee_cup_theme_viewer

label laptop_label:
    $current_location = "laptop"

    if show_animation_camera:
        image theme_pic_laptop_label = "desk_top_full.png"
        scene theme_pic_laptop_label
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    $ chat_images = [
        "chat_1.jpg",
        "chat_2.jpg",
        "chat_3.jpg",
        "chat_4.jpg",
        "chat_5.jpg",
        "chat_6.jpg",
        "chat_7.jpg",
        "chat_8.jpg"
    ]
    $ chat_index = 7

    call screen chat_viewer(chat_images)
    return

label note_label:

    if scalebar_state:
        jump note_fingerprint_label

    $current_location = "note"

    if show_animation_camera:
        image theme_pic_note_label = "note_theme.png"
        scene theme_pic_note_label
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen note_viewer
    return

label note_fingerprint_label:
    $current_location = "note_fingerprint"

    if show_animation_camera:
        image theme_pic_note_fingerprint_label = "note_finger_theme.png"
        scene theme_pic_note_fingerprint_label
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black
    
    call screen note_viewer_with_fingerprints
    return

label pill_label:
    $current_location = "pill"
    if show_animation_camera:
        image theme_pic_pill_label = "pill_theme.png"
        scene theme_pic_pill_label
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black
    
    call screen pill_viewer
    return

label water_bottle_label:
    $current_location = "water_bottle"

    if show_animation_camera:
        image theme_pic_water_bottle_label = "water_bottle_theme.png"
        scene theme_pic_water_bottle_label
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen water_bottle_viewer
    return

label photo_album_label:
    call screen photo_album

label coffee_on_floor_label:
    $current_location = "coffee_on_floor"
    
    if show_animation_camera:
        image coffee_on_floor_theme = "coffee_on_floor_theme.png"
        scene coffee_on_floor_theme
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen coffee_on_floor_viewer
    return

label hair_label:
    $current_location = "hair"

    if show_animation_camera:
        image hair_theme = "hair_theme.png"
        scene hair_theme
        show screen photo_flying
        $ renpy.pause(1.2)
        scene black

    call screen hair_viewer
    return

label photo_viewer_label:
    call screen photo_viewer(index=photo_show_index)


transform button_zoom:
    zoom 0.4

label kastle_meyer_quiz:
    image kastle_meyer_quiz = "coffee_on_floor_theme.png"
    scene kastle_meyer_quiz
    # 简短介绍
    "Let's review the Kastle–Meyer presumptive blood test."

    # 问题 1
    "1) Which reagent is applied first to the swab tip?"
    menu:
        "Phenolphthalein indicator":
            jump km_q1_correct
        "Hydrogen peroxide":
            jump km_q1_wrong
        "Luminol":
            jump km_q1_wrong

label km_q1_correct:
    "Correct! Phenolphthalein indicator is added first."
    jump km_q2

label km_q1_wrong:
    "Incorrect. The first reagent to apply is phenolphthalein indicator."
    jump kastle_meyer_quiz

label km_q2:
    "2) After applying phenolphthalein, how long should you wait before adding hydrogen peroxide?"
    menu:
        "About 5 seconds":
            jump km_q2_correct
        "About 30 seconds":
            jump km_q2_wrong
        "Immediately, no wait":
            jump km_q2_wrong

label km_q2_correct:
    "Right! You should wait about 5 seconds."
    jump km_q3

label km_q2_wrong:
    "Not quite. You need to wait around 5 seconds."
    jump km_q2

label km_q3:
    "3) Which color change indicates a positive reaction for blood?"
    menu:
        "Pink":
            jump km_q3_correct
        "Blue":
            jump km_q3_wrong
        "Green":
            jump km_q3_wrong

label km_q3_correct:
    "Yes! A pink color indicates a positive Kastle–Meyer test."
    jump km_quiz_end

label km_q3_wrong:
    "That's not correct. A positive reaction produces a pink color."
    jump km_q3

label km_quiz_end:
    "Great job! Seems like this is not a blood, but a coffee stain."
    jump floor_stain_label
    
label collect_empty_pill:
    # 这句会用叙述者（白字）显示
    image empty_pill = "desk_bag.png"
    scene empty_pill

    "I see an empty pill inside the bag..."

    # 把 empty_pill 加进背包
    # $ addToInventory(["empty_pill"])

    # 可选暂停一下让玩家读
    pause

    # 返回到查看背包的流程
    jump backpack_label
