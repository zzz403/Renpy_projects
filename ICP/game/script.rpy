default current_cursor = ''
default show_case_files = False
default show_toolbox = False
default location = "hallway"
default selected_elements = []
default element_selection_message = ""
default pill_process = 0  # 0: initial, 1: ready_to_digest, 2: ready_to_dilute, 3: ready_for_icp
default current_liquid_sample = ""  # Track which liquid sample is being processed (coffee/water)
default liquid_samples_obtained = []  # Track which liquid samples have been processed
default cal_blank_obtained = False  # Track if calibration blank has been obtained
default multi_element_added = False  # Track if multi-element stock has been added
default nitric_acid_added = False  # Track if nitric acid has been added to flask

# Sample completion tracking
default pill_completed = True  # Track if pill sample preparation is complete
default coffee_completed = False  # Track if coffee sample preparation is complete  
default water_completed = False  # Track if water sample preparation is complete
default samples_analyzed = []  # Track which samples have been analyzed with ICP

### entries on afis when search
default afis_search = []
default afis_search_coordinates = [{'score_xpos': 0.53, 'xpos':0.61, 'ypos':0.505}]
# default correct_dfo_mixture = {"dfo", "hfe", "acetic acid", "methanol"}
# default player_dfo_mixture = {}
# default player_tool = ""
define s = Character(name=("Nina"), image="nina")

init python:
    
    def hide_all_inventory():
        renpy.hide_screen("full_inventory")
        renpy.hide_screen("inventory")
        renpy.hide_screen("toolbox")
        renpy.hide_screen("inv_buttons")
        renpy.hide_screen("close_inv")
        renpy.hide_screen("toolboxpop")
        renpy.hide_screen("inventoryItemMenu")
        renpy.hide_screen("toolboxItemMenu")
        renpy.hide_screen("toolboxPopItemMenu")
        renpy.hide_screen("inspectItem")

    def toolbox_actions(item: str) -> None:
        print("Toolbox action initiated with item:", item)
        global tool
        global pill_process
        global cal_blank_obtained
        
        # DFO mixing reagents (if needed in future)
        # if ready_to_mix:
        #     hide_all_inventory()
        #     if item == "methanol":
        #         tool = "methanol"
        #         renpy.hide_screen("full_inventory")
        #         renpy.jump("pour_methanol")
        
        # Calibration blank preparation - available in liquid_sample_prep location
        if location == "liquid_sample_prep":
            if item == "nitric_acid":
                hide_all_inventory()
                tool = "nitric acid"
                renpy.hide_screen("full_inventory")
                renpy.jump("prepare_cal_blank")
        
        # Standard solution preparation - available in volumetric_flask location
        if location == "volumetric_flask":
            if item == "multi_element_stock":
                hide_all_inventory()
                tool = "multi element stock"
                renpy.hide_screen("full_inventory")
                renpy.jump("pipette_multi_element_stock")
            elif item == "nitric_acid":
                hide_all_inventory()
                tool = "nitric acid"
                renpy.hide_screen("full_inventory")
                renpy.jump("add_nitric_acid_cylinder")
        
        # Digestion reagents - only available when pill_process == 1
        if pill_process == 1:  # ready_to_digest
            if item == "nitric_acid":
                hide_all_inventory()
                tool = "nitric acid"
                renpy.hide_screen("full_inventory")
                renpy.jump("pour_nitric_acid")
            elif item == "hydrofluoric_acid":
                hide_all_inventory()
                tool = "hydrofluoric acid"
                renpy.jump("pour_hydrofluoric_acid")
            elif item == "hydrogen_peroxide":
                hide_all_inventory()
                tool = "hydrogen peroxide"
                renpy.jump("pour_hydrogen_peroxide")
        
        # Dilution process - only available when pill_process == 2
        if pill_process == 2:  # ready_to_dilute
            print("Dilution process initiated with item:", item)
            hide_all_inventory()
            if item == "deionized_water":
                tool = "deionized water"
                renpy.hide_screen("full_inventory")
                renpy.jump("add_deionized_water")
    
    def inventory_actions(item: str) -> None:
        global location
        global gin
        global pills
        global imported_print
        global pressed
        global pill_process
        global current_liquid_sample

        if item == "gin":
            if location == "fumehood" and not gin.processed:
                hide_all_inventory()
                renpy.jump("fumehood_bottle")
        elif item == "label" or item == "baked_label":
            label_function_alt()
        elif item == "pills":
            if location == "grinder" and not pills.processed:
                hide_all_inventory()
                renpy.jump("grinder_pills")
        elif item == "grinded_pills":
            if location == "grinder":
                hide_all_inventory()
                renpy.jump("bottle_filling")
        elif item == "teflon_pills":
            if location == "mds" and pill_process == 1:  # Only when ready to digest
                hide_all_inventory()
                renpy.jump("microwave_digestion_step1")
        elif item == "digested_sample":
            if location == "dilute" and pill_process == 2:  # Only when ready to dilute
                hide_all_inventory()
                renpy.jump("transfer_to_polypropylene")
        elif item == "diluted_sample":
            if location == "analytical_instruments":
                # Check if there are any completed samples ready for ICP
                completed_samples = []
                if pill_completed and "pill" not in samples_analyzed:
                    completed_samples.append("pill")
                if coffee_completed and "coffee" not in samples_analyzed:
                    completed_samples.append("coffee")  
                if water_completed and "water" not in samples_analyzed:
                    completed_samples.append("water")
                
                if len(completed_samples) > 0:
                    hide_all_inventory()
                    print("Entering ICP analysis")
                    renpy.jump("icp_analysis")
        elif item == "coffee":
            if location == "liquid_sample_prep":
                hide_all_inventory()
                current_liquid_sample = "coffee"
                renpy.jump("pour_coffee_sample")
        elif item == "water":
            if location == "liquid_sample_prep":
                hide_all_inventory()
                current_liquid_sample = "water"
                renpy.jump("pour_water_sample")
        elif item == "fingerprint":
            if location == "afis" and pressed == "import":
                imported_print = "print_1"
                renpy.jump("import_print")

# Non-inventory related functions -----------------------------------
    config.mouse = {
        "default": [("cursor.png", 0, 0)],
        "dropper": [("dropper.png", 0, 49)],
        "dropper filled": [("dropper filled.png", 0, 49)],
        "hand": [("default_hand.png", 0, 0)]
    }

    default_mouse = "default"

    def set_cursor(cursor):
        global default_mouse
        global current_cursor
        if current_cursor == cursor:
            default_mouse = ''
            current_cursor = ''
        else:
            default_mouse = cursor
            current_cursor = cursor
    
    def analyzed_everything() -> None:
        return prints["print_1"].processed and prints["print_4"].processed
    
    def check_all_reagents_added():
        global reagents_added
        return all(reagents_added.values())
    
    def toggle_element(element):
        global selected_elements, element_selection_message
        if element in selected_elements:
            selected_elements.remove(element)
            element_selection_message = f"{element} deselected from analysis."
        else:
            selected_elements.append(element)
            element_selection_message = f"{element} selected for analysis."
        # Clear message after a short time
        renpy.restart_interaction()
    
    def clear_element_message():
        global element_selection_message
        element_selection_message = ""
        renpy.restart_interaction()
    
    def set_timer(item: str):
        item = False
    
    def disable_timer(item: str):
        item = True

    def calculate_afis(evidence):
        global afis_search
        afis_search = []
        evidence.processed = True
    
        for e in afis_evidence:
            if e.processed and e!= evidence:
                afis_search.append(e)

    def close_menu():
        if renpy.get_screen("casefile_physical"):
            renpy.hide_screen("casefile_physical")
        elif renpy.get_screen("casefile_photos"):
            renpy.hide_screen("casefile_photos")
        elif renpy.get_screen("casefile"):
            renpy.hide_screen("casefile")
        else:
            renpy.show_screen("casefile")

    
    class Evidence:
        def __init__(self, name, afis_details):
            self.name = name
            self.afis_details = afis_details
            self.processed = False
    
    ### declare each piece of evidence
    laptop_fingerprint = Evidence(name = 'laptop_fingerprint',
                                afis_details = {
                                    'image': 'laptop_fingerprint',
                                    'xpos':0.18, 'ypos':0.3,
                                    'score': '70'})
    screwdriver = Evidence(name = 'screwdriver',
                        afis_details = {
                            'image': 'screwdriver_fingerprint',
                            'xpos':0.18, 'ypos':0.3,
                            'score': '70'})
    
    ### declare afis relevant evidence
    afis_evidence = [laptop_fingerprint, screwdriver]

    ### set current_evidence to track which evidence is currently active
    current_evidence = screwdriver


#################################### START #############################################
label start:
    # Dial variables
    play music "Science.mp3"
    $ dial_image = "images/dial.png"
    $ dial_size = (660 / 2, 660 / 2)
    $ t = Transform(child = dial_image, zoom = 0.5)
    $ dial_sprite_manager = SpriteManager(event = dial_events)
    $ dial_sprite = dial_sprite_manager.create(t)
    $ dial_sprite.x = config.screen_width / 2 - dial_size[0] / 2
    $ dial_sprite.y = config.screen_height / 2 - dial_size[1] / 2
    $ dial_rotate = False
    $ dial_sprite.rotate_amount = 0
    $ dial_offset = 68.2
    $ dial_start_rotate = False
    $ dial_number = 0
    $ dial_text = 0
    $ previous_dial_text = 0
    $ dial_changed = False

    # Other variables
    $ old_mousepos = (0.0, 0.0)
    $ degrees = 0
    $ old_degrees = 0
    $ combinations = {"safe_1" : 50, "safe_2" : [23, 5, 75, 44]}
    $ completed_combination_numbers = {}
    $ combination_check = None
    $ current_safe = 1
    $ combination_length = 0
    scene entering_lab_screen
    with Dissolve(1.5)

label lab_hallway_intro:  
    scene lab_hallway_idle
    show nina normal1 

        # REQUIRED FOR INVENTORY:
    $config.rollback_enabled = False # disables rollback
    $quick_menu = False # removes quick menu (at bottom of screen) - might put this back since inventory bar moved to right side
    
    # environment:
    $environment_SM = SpriteManager(event = environmentEvents) # sprite manager that manages environment items; triggers function environmentEvents() when event happens with sprites (e.g. button click)
    $environment_sprites = [] # holds all environment sprite objects
    $environment_items = [] # holds environment items
    $environment_item_names = [] # holds environment item names
    
    # inventory
    $inventory_SM = SpriteManager(update = inventoryUpdate, event = inventoryEvents) # sprite manager that manages evidence items; triggers function inventoryUpdate 
    $inventory_sprites = [] # holds all evidence sprite objects
    $inventory_items = [] # holds evidence items
    $inventory_item_names = ["Tape on acetate", "Tapeglo in bag", "Tape photo", "Duct tape tapeglo", "Distilled water", "Tape in tweezers", "Duct tape", "Tapeglo", 
    "Fingerprint on card", "Backing card","Scalebar", "Lifting tape", "Jar photo", "Lid in tweezers", "Camel brush", "Lid with soot", "Lid", "Camphor smoke", "Lighter", 
    "Tweezers", "Gloves box", "Evidence bag", "Jar in bag", "Tape in bag", "Pvs in bag"] # holds names for inspect pop-up text 
    $inventory_db_enabled = False # determines whether up arrow on evidence hotbar is enabled or not
    $inventory_ub_enabled = False # determines whether down arrow on evidence hotbar is enabled or not
    $inventory_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for evidence bar
    $inventory_slot_padding = 120 / 2 # sets padding size between evidence slots
    $inventory_first_slot_x = 110 # sets x coordinate for first evidence slot
    $inventory_first_slot_y = 175 # sets y coordinate for first evidence slot
    $inventory_drag = False # by default, item isn't draggable

    # toolbox:
    $toolbox_SM = SpriteManager(update = toolboxUpdate, event = toolboxEvents) # sprite manager that manages toolbox items; triggers function toolboxUpdate 
    $toolbox_sprites = [] # holds all toolbox sprite objects
    $toolbox_items = [] # holds toolbox items
    # $toolbox_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolbox_db_enabled = False # determines whether up arrow on toolbox hotbar is enabled or not
    $toolbox_ub_enabled = False # determines whether down arrow on toolbox hotbar is enabled or not
    # $toolbox_slot_size = (int(215 / 2), int(196 / 2)) # sets slot size for toolbox bar
    $toolbox_slot_size = (100, 100)
    # $toolbox_slot_padding = 125 / 2 # sets padding size between toolbox slots
    $toolbox_slot_padding = 69
    $toolbox_first_slot_x = 110 # sets x coordinate for first toolbox slot
    $toolbox_first_slot_y = 175 # sets y coordinate for first toolbox slot
    $toolbox_drag = False # by default, item isn't draggable

    # toolbox popup:
    $toolboxpop_SM = SpriteManager(update = toolboxPopUpdate, event = toolboxPopupEvents) # sprite manager that manages toolbox pop-up items; triggers function toolboxPopUpdate
    $toolboxpop_sprites = [] # holds all toolbox pop-up sprite objects
    $toolboxpop_items = [] # holds toolbox pop-up items
    # $toolboxpop_item_names = ["Tape", "Ziploc bag", "Jar in bag", "Tape in bag", "Gun all", "Empty gun", "Cartridges", "Gun with cartridges", "Tip", "Pvs in bag"] # holds names for inspect pop-up text 
    $toolboxpop_db_enabled = False # determines whether up arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_ub_enabled = False # determines whether down arrow on toolbox pop-up hotbar is enabled or not
    $toolboxpop_slot_size = (100, 100) # sets slot size for toolbox pop-up bar
    $toolboxpop_slot_padding = 69 # sets padding size between toolbox pop-up slots
    $toolboxpop_first_slot_x = 406 # sets x coordinate for first toolbox pop-up slot
    $toolboxpop_first_slot_y = 445 # sets y coordinate for first toolbox pop-up slot
    $toolboxpop_drag = False # by default, item isn't draggable

    $current_scene = "scene1" # keeps track of current scene
    
    $dialogue = {} # set that holds name of character saying dialogue and dialogue message
    $item_dragged = "" # keeps track of current item being dragged
    $mousepos = (0.0, 0.0) # keeps track of current mouse position
    $i_overlap = False # checks if 2 inventory items are overlapping/combined
    $ie_overlap = False # checks if an inventory item is overlapping with an environment item

    $all_pieces = 0

    # python code block
    python:
        addToToolbox(["nitric_acid","hydrofluoric_acid","hydrogen_peroxide","deionized_water","multi_element_stock"])
        addToInventory(["pills","coffee","water"])
        # Track reagent addition status
        reagents_added = {
            "nitric_acid": False,
            "hydrofluoric_acid": False, 
            "hydrogen_peroxide": False
        }


    # scene scene-1-bg at half_size - sets background image, don't need rn

label hallway:
    $ location = ""
    $ hide_all_inventory()
    scene lab_hallway_idle
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    call screen lab_hallway_screen

label data_analysis_lab:
    $ location = ""
    hide screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('hallway') onlayer over_screens  
    call screen data_analysis_lab_screen

label afis:
    hide screen back_button_screen onlayer over_screens
    hide screen full_inventory
    show screen back_button_screen('data_analysis_lab') onlayer over_screens  
    call screen afis_screen

label materials_lab:
    $ location = ""
    $ hide_all_inventory()
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    hide screen back_button_screen onlayer over_screens
    show screen back_button_screen('hallway') onlayer over_screens
    hide screen grinder
    call screen materials_lab_screen

label wet_lab:
    $ location = ""
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen wet_lab_screen

label analytical_instruments:
    show screen full_inventory
    python:
        if analyzed_everything():
            renpy.hide_screen("full_inventory")
            renpy.jump("end")
    show screen back_button_screen('materials_lab') onlayer over_screens
    call screen analytical_instruments_screen

label mds:
    $ location = "mds"
    show screen full_inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene expression "materials_lab/mds_idle.png"
    
    "Click on the Teflon digestion vessel to start the microwave digestion process."
    
    call screen full_inventory

label end:
    hide screen back_button_screen onlayer over_screens
    show nina normal1 
    s "It looks like you've analyzed all the evidence. Great work!"
    s "I hope you took note of the results. Tomorrow, you'll be testifying in court about your findings."
    show nina normal3 
    s "But for now, give yourself a pat on the back and go get some rest!"
    return

# Microwave Digestion System - Three Step Process
label microwave_digestion_step1:
    scene expression "materials_lab/mds_idle.png"
    
    "Step 1 of 3: Setting up the first microwave digestion cycle."
    "Please select the correct power and time settings for the first step:"
    
    menu:
        "5 minutes @ 150W":
            "Incorrect! This power is too low and time too short for effective digestion."
            jump microwave_digestion_step1
        
        "10 minutes @ 250W":
            "Correct! Starting the first digestion cycle: 10 minutes @ 250W"
            jump microwave_digestion_step2
        
        "15 minutes @ 300W":
            "Incorrect! This would be too intense for the initial digestion step."
            jump microwave_digestion_step1

label microwave_digestion_step2:
    scene expression "materials_lab/mds_idle.png"
    
    "Step 1 completed successfully! The sample has been partially digested."
    "Step 2 of 3: Setting up the second microwave digestion cycle."
    "Please select the correct power and time settings for the second step:"
    
    menu:
        "10 minutes @ 400W":
            "Correct! Starting the second digestion cycle: 10 minutes @ 400W"
            jump microwave_digestion_step3
        
        "8 minutes @ 350W":
            "Incorrect! The power is too low for this intermediate step."
            jump microwave_digestion_step2
        
        "12 minutes @ 450W":
            "Incorrect! This would be too aggressive for the second step."
            jump microwave_digestion_step2

label microwave_digestion_step3:
    scene expression "materials_lab/mds_idle.png"
    
    "Step 2 completed successfully! The sample digestion is progressing well."
    "Step 3 of 3: Setting up the final microwave digestion cycle."
    "Please select the correct power and time settings for the final step:"
    
    menu:
        "10 minutes @ 600W":
            "Correct! Starting the final digestion cycle: 10 minutes @ 600W"
            jump microwave_digestion_complete
        
        "8 minutes @ 550W":
            "Incorrect! The time is too short for complete digestion."
            jump microwave_digestion_step3
        
        "12 minutes @ 650W":
            "Incorrect! This power would be too high and could damage the sample."
            jump microwave_digestion_step3

label microwave_digestion_complete:
    scene expression "materials_lab/mds_idle.png"
    
    "Excellent! All three digestion cycles completed successfully!"
    "The sample has been completely digested following the proper protocol:"
    "• Step 1: 10 minutes @ 250W"
    "• Step 2: 10 minutes @ 400W" 
    "• Step 3: 10 minutes @ 600W"
    
    "The Teflon digestion vessel now contains a clear, digested sample ready for dilution."
    
    # Add the digested sample to inventory and proceed
    python:
        addToInventory(["digested_sample"])
        # Remove teflon_pills from inventory since it's now processed
        removeInventoryItem(inventory_sprites[inventory_items.index("teflon_pills")])
        teflon_pills.disable_evidence()  # Remove the undigested vessel
        pill_process = 2  # Sample is digested, ready for transfer and dilution
    
    "Digested sample added to inventory. Proceeding to dilution step..."
    
    jump dilute

# Step 4: Dilution Process
label dilute:
    $ location = "dilute"
    show screen full_inventory
    scene expression "materials_lab/dilute_idle.png"
    
    "Step 4: Dilution - Transfer the digested solution to a polypropylene liner"
    if pill_process == 2:
        "Click on the digested sample to transfer it to the polypropylene container."
        "After transfer, click on deionized water in the toolbox to dilute the sample to 50 mL."
    
    call screen full_inventory

# Dilution process animations
label transfer_to_polypropylene:
    scene expression "materials_lab/dilute_idle.png"
    
    $ transfer_x = 435
    $ transfer_y = 251
    
    # Show the digested sample moving to the polypropylene container
    show expression "Inventory Items/Inventory-digested_sample.png" as sample_transfer:
        xpos 100 ypos 100
        linear 2.0 xpos transfer_x ypos transfer_y - 50
        linear 1.0 rotate 15  # Slight tilt for pouring
    
    "Transferring the digested sample to the polypropylene liner..."
    
    # Pouring effect
    show expression "images/liquid_pour.png" as pour_sample:
        xpos transfer_x ypos transfer_y - 30
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide sample_transfer
    hide pour_sample
    
    "Sample successfully transferred to polypropylene container."
    "Now add deionized water to dilute the solution to 50 mL total volume."
    
    jump dilute

label add_deionized_water:
    $ print("Adding deionized water...")
    scene expression "materials_lab/dilute_idle.png"
    
    $ dilute_x = 435
    $ dilute_y = 251
    
    # Show the deionized water bottle moving to the container
    show expression "Toolbox Items/toolbox-deionized_water.png" as water_bottle:
        xpos 150 ypos 100
        linear 2.0 xpos dilute_x ypos dilute_y - 80
        linear 1.0 rotate 30  # Tilt for pouring
    
    "Adding deionized water to dilute the solution to 50 mL..."
    
    # Pouring effect for water (longer duration)
    show expression "images/liquid_pour.png" as pour_water:
        xpos dilute_x ypos dilute_y - 50
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 3.0 alpha 1.0  # Longer pour for dilution
        linear 0.5 alpha 0.0
    
    hide water_bottle
    hide pour_water
    
    "Excellent! The sample has been diluted to 50 mL with deionized water."
    "The diluted sample is now ready for ICP analysis."
    
    # Replace digested_sample with diluted_sample
    python:
        addToInventory(["diluted_sample"])
        # Remove digested_sample from inventory since it's now diluted
        removeInventoryItem(inventory_sprites[inventory_items.index("digested_sample")])
        digested_sample.disable_evidence()
        pill_process = 3  # Ready for ICP analysis
        pill_completed = True  # Mark pill sample as completed
    
    show nina normal1
    s "Perfect! Sample preparation is complete."
    s "Now let's head back to the materials lab to access the analytical instruments for ICP analysis."
    
    jump materials_lab

# ICP Analysis System
label icp_analysis:
    $ location = "icp"
    # show screen full_inventory
    show screen back_button_screen('analytical_instruments') onlayer over_screens
    scene expression "materials_lab/ICP_periodic_idle.png"
    
    # Check which samples are completed and not yet analyzed
    python:
        completed_samples = []
        if pill_completed and "pill" not in samples_analyzed:
            completed_samples.append("pill")
        if coffee_completed and "coffee" not in samples_analyzed:
            completed_samples.append("coffee")  
        if water_completed and "water" not in samples_analyzed:
            completed_samples.append("water")
    
    show nina normal1
    
    # Different dialogues based on number of completed samples
    if len(completed_samples) == 0:
        s "Let's go prepare some samples first before we can run ICP analysis!"
        s "We need to complete the sample preparation process."
        hide nina
        jump materials_lab
    elif len(completed_samples) == 1:
        if completed_samples[0] == "pill":
            s "Great! We have the pill sample ready for ICP analysis."
            s "Let's analyze the pill sample to determine its elemental composition."
        elif completed_samples[0] == "coffee":
            s "Perfect! We have the coffee sample ready for ICP analysis."
            s "Let's analyze the coffee sample to check for any trace elements."
        elif completed_samples[0] == "water":
            s "Excellent! We have the water sample ready for ICP analysis."
            s "Let's analyze the water sample to determine its purity."
    else:
        s "We have multiple samples ready for analysis!"
        s "Which sample would you like to analyze first?"
        
        hide nina
        
        # Create menu for sample selection
        menu:
            "Which sample would you like to analyze?"
            
            "Pill sample" if "pill" in completed_samples:
                $ current_sample_for_analysis = "pill"
                
            "Coffee sample" if "coffee" in completed_samples:
                $ current_sample_for_analysis = "coffee"
                
            "Water sample" if "water" in completed_samples:
                $ current_sample_for_analysis = "water"
        
        show nina normal1
        if current_sample_for_analysis == "pill":
            s "Great choice! Let's analyze the pill sample."
        elif current_sample_for_analysis == "coffee":
            s "Good selection! Let's analyze the coffee sample."
        elif current_sample_for_analysis == "water":
            s "Perfect! Let's analyze the water sample."
    
    hide nina
    
    "ICP Analysis: Click on elements in the periodic table to analyze their concentration in the sample."
    "Click an element once to select it, click again to deselect."
    
    # Initialize selected elements tracking
    python:
        if "selected_elements" not in globals():
            selected_elements = []
        # Set current sample if only one available
        if len(completed_samples) == 1:
            current_sample_for_analysis = completed_samples[0]
    
    call screen icp_periodic_table

# ICP Periodic Table Screen with Hotspots
# ICP Analysis Results
label icp_results:
    hide screen icp_periodic_table
    scene expression "materials_lab/ICP_periodic_idle.png"
    show screen back_button_screen('analytical_instruments') onlayer over_screens
    
    # Show which sample is being analyzed
    python:
        sample_name = current_sample_for_analysis if 'current_sample_for_analysis' in globals() else "unknown"
    
    "ICP Analysis Results for [sample_name] sample:"
    "Analyzing selected elements: [', '.join(selected_elements)]"
    
    # Generate random concentrations for demonstration
    python:
        analysis_results = {}
        import random
        for element in selected_elements:
            concentration = round(random.uniform(0.1, 100.0), 2)
            analysis_results[element] = concentration
    
    "Analysis complete! Results:"
    
    python:
        result_text = ""
        for element, concentration in analysis_results.items():
            result_text += f"{element}: {concentration} ppm\n"
    
    "[result_text]"
    
    show nina normal1
    
    # Check for specific toxic elements based on sample type
    python:
        has_arsenic = "As" in selected_elements
        has_barium = "Ba" in selected_elements
    
    if sample_name == "pill":
        if has_barium:
            s "This is concerning! The analysis shows elevated levels of Barium in the pill sample."
            s "This could indicate the presence of Barium salts, which are known acute poisons."
            s "Barium compounds can cause severe cardiovascular and neurological symptoms."
            s "This finding is crucial evidence for our forensic investigation."
            jump icp_results_final
        else:
            s "The analysis doesn't show any obvious toxic elements in the expected range."
            s "We should re-examine the sample and consider testing for other potential toxins."
            s "Let's run additional tests to get a complete picture."
            s "Please select different elements to analyze."
            call screen icp_periodic_table
    elif sample_name == "coffee":
        if has_arsenic:
            s "Alert! The coffee sample shows elevated Arsenic levels!"
            s "Arsenic is a dangerous chronic poison that can accumulate in the body over time."
            s "Even small amounts consumed regularly can lead to serious health problems."
            s "This is a significant finding that could explain chronic poisoning symptoms."
            jump icp_results_final
        else:
            s "The coffee sample analysis doesn't reveal the expected toxic markers."
            s "We should re-test this sample with a different analytical approach."
            s "There might be other substances we haven't detected yet."
            s "Please select different elements to analyze."
            call screen icp_periodic_table
    elif sample_name == "water":
        s "The water sample analysis looks perfectly normal."
        s "All detected elements are within acceptable limits for drinking water."
        s "This appears to be clean, safe water with typical mineral content."
        s "No toxic substances detected - this water is not the source of contamination."
        jump icp_results_final
    else:
        s "Excellent work! You've successfully completed the ICP analysis."
        s "These concentration values will help identify any potential toxic substances."
        jump icp_results_final

label icp_results_final:
    s "These analytical results will be important for your forensic report."
    
    # Mark this sample as analyzed and add results to inventory
    python:
        if sample_name not in samples_analyzed:
            samples_analyzed.append(sample_name)
        if sample_name == "pill":
            diluted_sample.processed = True
        # addToInventory([f"icp_results_{sample_name}"])
    
    "ICP analysis results for [sample_name] sample added to inventory."
    
    # Check if there are still samples to analyze
    python:
        remaining_samples = []
        if pill_completed and "pill" not in samples_analyzed:
            remaining_samples.append("pill")
        if coffee_completed and "coffee" not in samples_analyzed:
            remaining_samples.append("coffee")  
        if water_completed and "water" not in samples_analyzed:
            remaining_samples.append("water")
    
    
    if len(remaining_samples) > 0:
        show nina normal1
        s "We still have [len(remaining_samples)] more sample(s) to analyze."
        s "Let's continue with the remaining samples: [', '.join(remaining_samples)]"
        hide nina
        jump materials_lab
    else:
        show nina normal1
        s "Congratulations! You have successfully completed the ICP analysis of all samples!"
        s "All forensic samples have been thoroughly analyzed and documented."
        s "The analytical data collected will be crucial for the forensic investigation."
        s "Great work on completing the comprehensive elemental analysis!"
        hide nina
        jump materials_lab

# Grinder Equipment Introduction Labels
label grinder_introduction:
    $ location = "grinder"
    show screen grinder
    show screen full_inventory
    show nina normal1
    s "This is our laboratory grinder - an essential piece of equipment for sample preparation."
    s "It can pulverize solid samples like pills into fine powder, which is necessary for chemical analysis."
    s "The grinder ensures uniform particle size, which is crucial for accurate and reproducible results."
    s "To use it, simply place your sample inside and the rotating blades will do the work."
    hide nina
    call screen grinder

label scale_introduction:
    $ location = "grinder"
    show screen grinder
    show screen full_inventory
    show nina normal1
    s "This is our analytical balance - one of the most precise instruments in the lab."
    s "It can measure extremely small masses with high accuracy, down to milligram precision."
    s "Accurate weighing is fundamental in forensic chemistry for calculating concentrations and ratios."
    s "Always ensure the balance is level and the weighing chamber is clean before use."
    hide nina
    call screen grinder

# Liquid Sample Preparation System
label liquid_sample_preparation:
    $ location = "liquid_sample_prep"
    show screen full_inventory
    show screen back_button_screen('materials_lab') onlayer over_screens
    scene expression "materials_lab/autosampler_idle.png"

    "Liquid Sample Preparation - Prepare liquid samples for analysis."
    "This station is used for processing liquid evidence samples."
    "Click on coffee or water from your inventory to begin sample preparation."
    
    call screen full_inventory

# Liquid Sample Pouring Animations
label pour_coffee_sample:
    scene expression "materials_lab/autosampler_idle.png"
    
    "Preparing coffee sample for analysis..."
    
    # Show coffee bottle at starting position (smaller size)
    show expression "materials_lab/sample_bottle_coffee.png" as coffee_bottle:
        xpos 576 ypos 112
        zoom 0.7  # Scale down the bottle
        linear 2.0 xpos 600 ypos 250  # Move to sample preparation area (up and right)
        linear 1.0 rotate 45  # Tilt for pouring
    
    "Pouring coffee sample into the analysis vessel..."
    
    # Pouring effect (adjusted position)
    show expression "images/liquid_pour.png" as pour_effect:
        xpos 470 ypos 270
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.5 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide coffee_bottle
    hide pour_effect
    
    # Remove coffee from inventory and record the sample
    python:
        if "coffee" not in liquid_samples_obtained:
            liquid_samples_obtained.append("coffee")
        removeInventoryItem(inventory_sprites[inventory_items.index("coffee")])
    
    show nina normal1
    s "Coffee sample has been successfully prepared for analysis."
    s "The sample is now ready for further processing or testing."
    hide nina
    
    # Check if we can proceed to next stage
    python:
        if cal_blank_obtained and len(liquid_samples_obtained) > 0:
            renpy.jump("volumetric_flask_stage")
    
    jump liquid_sample_preparation

label pour_water_sample:
    scene expression "materials_lab/autosampler_idle.png"
    
    "Preparing water sample for analysis..."
    
    # Show water bottle at starting position  
    show expression "materials_lab/sample_water.png" as water_bottle:
        xpos 576 ypos 112
        zoom 0.7  # Scale down the bottle  
        linear 2.0 xpos 600 ypos 250  # Move to sample preparation area (up and right)
        linear 1.0 rotate 45  # Tilt for pouring
    
    "Pouring water sample into the analysis vessel..."
    
    # Pouring effect
    show expression "images/liquid_pour.png" as pour_effect:
        xpos 470 ypos 270
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide water_bottle
    hide pour_effect
    
    # Remove water from inventory and record the sample
    python:
        if "water" not in liquid_samples_obtained:
            liquid_samples_obtained.append("water")
        removeInventoryItem(inventory_sprites[inventory_items.index("water")])
    
    show nina normal1
    s "Water sample has been successfully prepared for analysis."
    s "The sample is now ready for further processing or testing."
    hide nina
    
    # Check if we can proceed to next stage
    python:
        if cal_blank_obtained and len(liquid_samples_obtained) > 0:
            renpy.jump("volumetric_flask_stage")
    
    jump liquid_sample_preparation# Calibration Blank Preparation
label prepare_cal_blank:
    scene expression "materials_lab/autosampler_idle.png"
    
    "Preparing calibration blank with nitric acid..."
    
    # Show nitric acid bottle moving for cal blank preparation
    show expression "Toolbox Items/toolbox-nitric_acid.png" as nitric_bottle:
        xpos 150 ypos 100
        linear 2.0 xpos 500 ypos 280
        linear 1.0 rotate 30  # Tilt for pouring
    
    "Adding nitric acid to create calibration blank..."
    
    # Pouring effect
    show expression "images/liquid_pour.png" as pour_nitric:
        xpos 520 ypos 300
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide nitric_bottle
    hide pour_nitric
    
    # Mark cal blank as obtained
    python:
        cal_blank_obtained = True
    
    show nina normal1
    s "Excellent! We have successfully prepared a calibration blank."
    s "This blank will be essential for accurate analysis results."
    hide nina
    
    # Check if we can proceed to next stage
    python:
        if cal_blank_obtained and len(liquid_samples_obtained) > 0:
            renpy.jump("volumetric_flask_stage")
    
    jump liquid_sample_preparation

# Volumetric Flask Stage
label volumetric_flask_stage:
    $ location = "volumetric_flask"
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    "Volumetric Flask Station - Precision dilution and measurement"
    "Preparing 10x standard solution for calibration and functional checks"
    # "Step 1: Use 5 mL pipette to transfer multi-element stock 5 mL to 50 mL volumetric flask"
    # "Step 2: Add 45 mL 2% HNO3 using graduated cylinder to get 10x solution"
    "Click on multi-element stock in the toolbox to begin pipetting."
    
    show nina normal1
    s "Great work! You've prepared all the necessary samples."
    s "Now we need to prepare a 10x standard solution for calibration."
    s "First, use the pipette to transfer 5 mL of multi-element stock to the volumetric flask."
    hide nina
    
    call screen full_inventory
# Standard Solution Preparation Labels
label pipette_multi_element_stock:
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    "Using 5 mL pipette to transfer multi-element stock..."
    
    # Show pipette first
    show expression "materials_lab/pipette.png" as pipette:
        xpos 200 ypos 150
        linear 1.5 xpos 400 ypos 200
    
    # Show multi-element stock bottle
    show expression "materials_lab/multi_element_stock.png" as stock_bottle:
        xpos 100 ypos 100
        linear 2.0 xpos 330 ypos 600
    
    "Pipetting 5 mL of multi-element stock solution..."
    
    # Move pipette to bottle for aspiration
    show pipette:
        linear 1.0 xpos 360 ypos 190
    
    "Aspirating stock solution into pipette..."
    
    pause 1.5
    
    # Move to volumetric flask in center
    show pipette:
        linear 2.0 xpos 930 ypos 0  # Center of screen
        linear 1.0 xpos 930 ypos 100  # Center of screen
    
    "Dispensing 5 mL into the 50 mL volumetric flask..."
    
    # Dispensing effect
    show expression "images/liquid_pour.png" as pour_stock:
        xpos 660 ypos 380
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 2.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide pipette
    hide stock_bottle
    hide pour_stock
    
    # Mark multi-element stock as added
    python:
        multi_element_added = True
    
    show nina normal1
    s "Excellent! You've successfully transferred 5 mL of multi-element stock."
    s "Now we need to add 45 mL of 2%% nitric acid to complete the 10x standard solution."
    hide nina
    
    # Check if both steps are complete
    python:
        if multi_element_added and nitric_acid_added:
            renpy.jump("dilution_series_quiz")
    
    jump volumetric_flask_stage

label add_nitric_acid_cylinder:
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    "Using graduated cylinder to add 45 mL 2%% HNO3..."
    
    # Show graduated cylinder
    show expression "materials_lab/graduated_cylinder.png":
        xpos 150 ypos 120
        linear 1.5 xpos 300 ypos 180
    
    # Show nitric acid bottle
    show expression "Toolbox Items/toolbox-nitric_acid.png":
        xpos 100 ypos 100
        linear 2.0 xpos 250 ypos 160
        linear 1.0 rotate 20  # Tilt for pouring into cylinder
    
    "Measuring 45 mL of 2%% nitric acid in graduated cylinder..."
    
    # Pouring into cylinder effect
    show expression "materials_lab/graduated_cylinder.png" as pour_cylinder:
        xpos 270 ypos 180
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 3.0 alpha 1.0  # Longer pour for 45 mL
        linear 0.5 alpha 0.0
    
    hide nitric_bottle
    hide pour_cylinder
    hide expression "materials_lab/graduated_cylinder.png"
    hide expression "Toolbox Items/toolbox-nitric_acid.png"
    
    "Now transferring 45 mL from graduated cylinder to volumetric flask..."
    
    # Move cylinder to volumetric flask
    show expression "materials_lab/graduated_cylinder.png":
        linear 2.0 xpos 600 ypos 340  # Move to volumetric flask
        linear 1.0 rotate 25  # Tilt for pouring
    
    "Pouring nitric acid into volumetric flask..."
    
    # Pouring into flask effect
    show expression "materials_lab/graduated_cylinder.png" as pour_flask:
        xpos 620 ypos 360
        alpha 0.0
        linear 0.5 alpha 1.0
        linear 3.0 alpha 1.0
        linear 0.5 alpha 0.0
    
    hide cylinder
    hide pour_flask
    
    # Mark nitric acid as added
    python:
        nitric_acid_added = True
    
    show nina normal1
    s "Perfect! You've successfully prepared the 10x standard solution."
    s "The volumetric flask now contains 5 mL multi-element stock + 45 mL 2%% HNO3."
    s "This gives us a 10x dilution standard for calibration and functional checks."
    hide nina
    
    "10x standard solution preparation complete!"
    
    # Check if both steps are complete
    python:
        if multi_element_added and nitric_acid_added:
            renpy.jump("dilution_series_quiz")
    
    jump volumetric_flask_stage
# Dilution Series Quiz
label dilution_series_quiz:
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    "Excellent! You have successfully prepared the 10x standard solution."
    "Now let's test your understanding of dilution series preparation."
    
    show nina normal1
    s "Great work completing the 10x standard! Now I want to test your knowledge."
    s "How would you prepare a 100x standard solution from the 10x solution we just made?"
    hide nina
    
    menu:
        "What is the correct method to prepare 100x standard solution?"
        
        "Take 10x solution 1 mL + 2%% HNO3 49 mL":
            "Incorrect. This ratio would give a different dilution factor."
            jump dilution_series_quiz
        
        "Take 10x solution 5 mL + 2%% HNO3 45 mL":
            "Correct! Taking 5 mL of 10x solution and adding 45 mL of 2%% HNO3 gives 100x dilution."
            jump quiz_1000x
        
        "Take 10x solution 10 mL + 2%% HNO3 40 mL":
            "Incorrect. This would give a different dilution factor."
            jump dilution_series_quiz

label quiz_1000x:
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    show nina normal1
    s "Excellent! You understand the 100x preparation."
    s "Now, how would you prepare a 1000x standard solution?"
    hide nina
    
    menu:
        "What is the correct method to prepare 1000x standard solution?"
        
        "Take 100x solution 5 mL + 2%% HNO3 45 mL":
            "Correct! Taking 5 mL of 100x solution and adding 45 mL of 2%% HNO3 gives 1000x dilution."
            jump quiz_complete
        
        "Take 10x solution 1 mL + 2%% HNO3 99 mL":
            "Incorrect. While this would give 1000x from 10x, the question asks about using 100x solution."
            jump quiz_1000x
        
        "Take 100x solution 10 mL + 2%% HNO3 40 mL":
            "Incorrect. This ratio would give a different dilution factor."
            jump quiz_1000x

label quiz_complete:
    scene expression "materials_lab/volumetric_flask_idle.png"
    
    show nina normal1
    s "Perfect! You have mastered the dilution series concept."
    s "You understand that:"
    s "• 100x standard: 10x solution 5 mL + 2%% HNO3 45 mL"
    s "• 1000x standard: 100x solution 5 mL + 2%% HNO3 45 mL"
    s "This systematic approach ensures accurate calibration standards."
    hide nina
    
    "Dilution series training complete!"
    "You are now ready for advanced ICP calibration procedures."
    
    # Mark liquid samples as completed
    python:
        if "coffee" in liquid_samples_obtained:
            coffee_completed = True
        if "water" in liquid_samples_obtained:
            water_completed = True
    
    jump materials_lab
