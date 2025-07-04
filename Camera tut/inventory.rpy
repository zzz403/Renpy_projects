init python:
    def toolboxEvents(event, x, y, at):
            global mousepos
            global dialogue
            global toolbox_drag
            global i_overlap
            global ie_overlap
            global all_evidence_markers
            global dropper_state
            global sample_vial_state
            global current_location

            # ...................
                                            
            if event.type == renpy.pygame_sdl2.MOUSEMOTION:
                mousepos = (x, y)
                if toolbox_drag == False:
                    for item in toolbox_sprites:
                        if item.visible == True:
                            if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                                if item.type == "camera":
                                    renpy.show_screen("toolboxItemCamera", item=item)
                                    renpy.restart_interaction()
                                    break
                                else:
                                    renpy.show_screen("toolboxItemMenu", item = item)
                                    renpy.restart_interaction()
                                    break
                            else:
                                if item.type == "camera":
                                    renpy.hide_screen("toolboxItemCamera")
                                else:
                                    renpy.hide_screen("toolboxItemMenu")
                                renpy.restart_interaction()
            def inventoryEvents(event, x, y, at):
                global mousepos
                global dialogue
                global inventory_drag
                global i_overlap
                global ie_overlap
                global sample_vial_state

                # ...................

                if event.type == renpy.pygame_sdl2.MOUSEMOTION:
                    mousepos = (x, y)
                    if inventory_drag == False:
                        for item in inventory_sprites:
                            if item.visible == True:
                                if item.x <= x <= item.x + item.width and item.y <= y <= item.y + item.height:
                                    if item.type == "images":
                                        renpy.show_screen("inventoryItemPhoto", item = item)
                                        renpy.restart_interaction()
                                        break
                                    else:
                                        renpy.show_screen("inventoryItemMenu", item = item)
                                        renpy.restart_interaction()
                                        break
                                    break
                                else:
                                    if item.type == "images":
                                        renpy.hide_screen("inventoryItemPhoto")
                                    else:
                                        renpy.hide_screen("inventoryItemMenu")
                                    renpy.restart_interaction()


screen toolboxItemCamera(item):
    zorder 7
    frame:
        xysize (toolbox_slot_size[0], toolbox_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)

        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [ Show("inspectItem", items=[item.type]), Hide("toolboxItemCamera") ]

        imagebutton auto "UI/expand-inventory-item-%s.png" align (1.0, 0.5) at half_size action [
            Hide("toolbox"),
            Function(renpy.show_screen, "camera_preview_ui"),
            Hide("toolboxItemCamera"),
            Function(renpy.hide_screen, "study_room3_inventory") 
        ]


screen inventoryItemPhoto(item):
    zorder 7
    frame:
        xysize (inventory_slot_size[0], inventory_slot_size[1])
        background "#FFFFFF30"
        xpos int(item.x)
        ypos int(item.y)
        imagebutton auto "UI/view-inventory-item-%s.png" align (0.0, 0.5) at half_size action [Show("inspectItem", items = [item.type]), Hide("inventoryItemPhoto")]
        imagebutton auto "UI/expand-inventory-item-%s.png" align (1.0, 0.5) at half_size action [
            Hide("inventory"),
            Hide("inventoryItemPhoto"),
            Hide("study_room3_inventory"),
            Jump("photo_album_label")
        ]


"""
you should change study_room3_inventory to the name of the ui in your game.
"""
# screen study_room3_inventory:
#     zorder 1
#     image "UI/inv-icon-bg.png" xpos 0.014 ypos -0.03 at half_size
#     imagebutton auto "UI/inventory-icon-%s.png" action If(renpy.get_screen("inventory") == None, true= [Show("inventory"), Hide("toolbox"), Hide("toolboxpop")], false= [Hide("inventory"), Hide("toolboxpop")]) xpos 0.087 ypos 0.02 at half_size
#     imagebutton auto "UI/tool-inventory-icon-%s.png" action If(renpy.get_screen("toolbox") == None, true= [Show("toolbox"), Hide("inventory")], false= [Hide("toolbox"), Hide("toolboxpop")]) xpos 0.037 ypos 0.02 at half_size
