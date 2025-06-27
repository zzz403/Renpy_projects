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
    "marker5": False
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
##########################################################################

default exhibit_no = ""
default picked_color = ""
default color_choice       = None
default show_color_picker  = False
default dropper_state = "empty"
default sample_vial_state = "not_taken"


init python:
    def on_color_chosen(color):
        global picked_color
        picked_color = color
        renpy.hide_screen("color_picker")

label start:
    jump toolbox_init
    return

label toolbox_init:
    # Initialize the toolbox with items
    python:
        # adds tape and ziploc bag to inventory
        addToInventory(["evidence_bag"])
        # addToToolbox(["pvs_kit"])
        addToToolbox(["evidence_marker"])
        addToToolbox(["camera"])        
        # addToToolbox(["note_book"])
        addToToolbox(["dropper"])
        addToToolbox

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

    $environment_items.append("coffee_view_coffee_cup") # coffee cup theme
    $environment_items.append("coffee_view_sample_vial") # sample vial theme
    python:
        new_items = ["coffee_view_coffee_cup", "coffee_view_sample_vial"]
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
            if item == "coffee_view_sample_vial":
                environment_sprites[-1].width = 260
                environment_sprites[-1].height = 400
                environment_sprites[-1].x = 350
                environment_sprites[-1].y = 250

    jump location_selection

label location_selection:
    $current_location = "location_selection"
    show screen study_room3_inventory
    call screen study_room_hover

    # call screen camera_preview_ui
    "Please select a location to explore."
    $ renpy.pause()

transform half_size:
    zoom 0.5

label desk_top:
    $current_location = "desk_top"

    call screen desk_top_hover
    e "This is the desk top. You can see some books and a laptop here."

    # Add more interactions or choices here if needed.
    return

label floor_stain:
    call screen floor_stain_hover
    e "This is the floor stain. It looks like a coffee spill."
    return

label chair_backpack:
    call screen chair_backpack_hover
    e "This is the chair with a backpack on it. You can check the backpack for clues."
    return



label coffee_cup_theme_label:
    $current_location = "coffee_cup_theme"
    call screen coffee_cup_theme_viewer

label laptop_investigate:
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




transform button_zoom:
    zoom 0.4



transform photo_slide_out:
    xpos 0.9 ypos 0.0
    linear 1.0 xpos 0.1 ypos 0.8
    linear 0.3 alpha 0.0
    zoom 0.1
