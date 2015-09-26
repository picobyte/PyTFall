label char_equip:
    python:
        focusitem = False
        selectedslot = None
        item_direction = None
        eqtarget.inventory.set_page_size(16)
        # eqtarget.inventory.famale_filter = True
        hero.inventory.set_page_size(16)
        # hero.inventory.famale_filter = True
        inv_source = eqtarget
        dummy = None
    
    scene bg gallery3
    
    $ global_flags.set_flag("hero_equip")
    $ renpy.retain_after_load()
    show screen pyt_char_equip
    
    python:
        
        inv_source.inventory.apply_filter("all")
        
        while 1:
            
            result = ui.interact()
            
            if result[0] == "jump":
                renpy.hide_screen("pyt_char_equip")
                if result[1] == "item_transfer":
                    renpy.hide_screen("pyt_girl_control")
                    pytfall.it = GuiItemsTransfer("personal_transfer", char=eqtarget, last_label=last_label)
                    jump("items_transfer")
                    
            elif result[0] == "equip_for":
                renpy.show_screen("pyt_equip_for", renpy.get_mouse_pos())
                
            elif result[0] == "item":
                if result[1] == 'equip/unequip':
                    if item_direction == 'equip':
                        # Common to any eqtarget:
                        if not can_equip(focusitem, eqtarget, silent=False):
                            focusitem = False
                            continue
                        if eqtarget == hero: # Simpler MCs logic:
                            equip_item(focusitem, eqtarget)
                        else: # Actors: Maybe it's a good idea to encapsulate this:
                            if eqtarget.status == "slave" and focusitem.slot in ["weapon"] and not focusitem.type.lower().startswith("nw"):
                                renpy.show_screen('pyt_message_screen', "Slaves are forbidden to equip large weapons by law!")
                                focusitem = False
                            else:
                                if inv_source == eqtarget:
                                    if all([eqtarget.status != "slave", eqtarget.disposition < 850]) or all([eqtarget.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                        eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "Don't want to..."]))
                                    else:
                                        equip_item(focusitem, eqtarget)
                                        # eqtarget.equip(focusitem)
                                else:
                                    if all([eqtarget.status != "slave", (focusitem.badness > 90 or focusitem.eqchance < 10)]):
                                        eqtarget.say(choice(["No way!", "I do not want this!", "No way in hell!"]))
                                    else:
                                        if transfer_items(inv_source, eqtarget, focusitem):
                                            equip_item(focusitem, eqtarget)
                            
                    elif item_direction == 'unequip':
                        if eqtarget == hero:
                            hero.unequip(focusitem)
                        else:    
                            if eqtarget.status != "slave" and eqtarget.disposition < 850:
                                eqtarget.say(choice(["I can manage my own things!", "Get away from my stuff!", "I'll think about it..."]))
                            else:
                                if inv_source == hero and eqtarget.status != "slave":
                                    if any([(focusitem.slot == "misc" and item.mdestruct), eqtarget.given_items.get(focusitem.id, 0) - 1 < 0]):
                                        eqtarget.say(choice(["Like hell am I giving away!", "Go get your own!", "Go find your own %s!" % item.id, "Would you like fries with that?",
                                                                 "Perhaps you would like me to give you the key to my flat where I keep my money as well?"]))
                                    else:
                                        eqtarget.unequip(focusitem)
                                        transfer_items(eqtarget, hero, focusitem)
                                else: # Slave condition:
                                    eqtarget.unequip(focusitem)
                                    eqtarget.inventory.remove(focusitem)
                                    inv_source.inventory.append(focusitem)
                            
                    selectedslot = False
                    focusitem = False
                     
                elif result[1] == 'equip':
                    focusitem = result[2]
                    selectedslot = focusitem.slot
                    item_direction = 'equip'
                    
                    # # To Calc the effects:
                    # dummy = copy_char(eqtarget)
                    # equip_item(focusitem, dummy, silent=True)
                    # renpy.show_screen("diff_item_effects", eqtarget, dummy)
                        
                elif result[1] == 'unequip':
                    selectedslot = result[2].slot
                    if selectedslot:
                        focusitem = result[2]
                        item_direction = 'unequip'
                        
                    # To Calc the effects:
                    # dummy = copy_char(eqtarget)
                    # dummy.unequip(focusitem)
                    # renpy.show_screen("diff_item_effects", eqtarget, dummy)
            
            elif result[0] == 'con':
                if result[1] == 'return':
                    selectedslot = False
                    focusitem = False
            
            elif result[0] == 'control':
                if result[1] == 'return':
                    break
    
    hide screen pyt_char_equip
    $ global_flags.del_flag("hero_equip")
    
    python:
        eqtarget.inventory.set_page_size(15)
        hero.inventory.set_page_size(15)
        # eqtarget.inventory.female_filter = False
        # hero.inventory.female_filter = False
        if eqtarget.location == "After Life":
            renpy.call_screen("pyt_message_screen", "Either your 'awesome' item handling or my 'brilliant' programming have killed %s..." % eqtarget.fullname)
            jump("mainscreen")
            
    if came_to_equip_from:
        $ last_label, came_to_equip_from = came_to_equip_from, None
        jump expression last_label
    else:
        jump girl_profile

screen pyt_equip_for(pos=()):
    zorder 3
    modal True
    
    key "mousedown_4" action NullAction()
    key "mousedown_5" action NullAction()
    
    python:
        x, y = pos
        if x > 1000:
            xval = 1.0
        else:
            xval = 0.0
        if y > 500:
            yval = 1.0
        else:
            yval = 0.0
    frame:
        style_group "dropdown_gm"
        pos (x, y)
        anchor (xval, yval)
        vbox:
            text "Equip For:" xalign 0 style "della_respira" color ivory
            null height 5
            for t in ["Combat", "Sex", "Service", "Striptease"]:
                if t == "Combat" and eqtarget.status == "slave":
                    pass
                else:
                    textbutton "[t]":
                        xminimum 200
                        action [Function(eqtarget.equip_for, t), Hide("pyt_equip_for")]
            textbutton "Close":
                action Hide("pyt_equip_for")
    
screen pyt_char_equip():
    
    # Useful keymappings (first time I try this in PyTFall): ====================================>
    if focusitem:
        key "mousedown_2" action Return(["item", "equip/unequip"])
    else:
        key "mousedown_2" action NullAction()
    key "mousedown_3" action Return(['control', 'return'])
    key "mousedown_4" action Function(inv_source.inventory.next)
    key "mousedown_5" action Function(inv_source.inventory.prev)
    key "mousedown_6" action Return(['con', 'return'])
    
    default stats_display = "stats"
    default tt = Tooltip("")
    
    # BASE FRAME 2 "bottom layer" ====================================>
    add "content/gfx/frame/equipment2.png"
    
    # Equipment slots
    frame:
        pos (425, 10)
        xminimum 298
        xmaximum 298
        ymaximum 410
        yminimum 410
        background Frame(Transform("content/gfx/frame/Mc_bg3.png", alpha=0.3), 10, 10)
        use pyt_eqdoll(active_mode=True, char=eqtarget, frame_size=[70, 70], scr_align=(0.98, 1.0), return_value=['item', "unequip"], txt_size=17, fx_size=(455, 400))
    
    # BASE FRAME 3 "mid layer" ====================================>
    add "content/gfx/frame/equipment.png"
    
    # Item Info: ====================================>
    hbox:
        align (0.388, 1.0)
        spacing 1
        style_group "content"
        
        # Item Desciption:
        showif focusitem:
            frame:
                xalign 0.6
                xpadding 13
                ypadding 5
                at fade_in_out()
                background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
                xysize (710, 296)
                use itemstats2(item=focusitem, size=(710, 296))
        
    # Left Frame: =====================================>
    fixed:
        pos (0, 2)
        xysize (220,724) 
        style_group "content"
        
        # NAME =====================================>
        text (u"{color=#ecc88a}[eqtarget.name]") font "fonts/TisaOTM.otf" size 28 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.53 ypos 126
        
        # PORTRAIT ============================>
        add eqtarget.show("portrait", resize=(100, 100), cache=True) pos (64, 11)
            
        # LVL ============================>
        hbox:
            spacing 1
            if (inv_source.level) <10:
                xpos 95
            elif (inv_source.level) <100:
                xpos 93
            elif (inv_source.level) <1000:
                xpos 89
            elif (inv_source.level) <10000:
                xpos 83
            else:
                xpos 79
            label "{color=#CDAD00}Lvl" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
            label "{color=#CDAD00}[inv_source.level]" text_font "fonts/Rubius.ttf" text_size 16 text_outlines [(1, "#3a3a3a", 0, 0)] ypos 173
        
        # Left Frame Buttons: =====================================>
        hbox:
            style_group "pb"
            xalign 0.55
            ypos 198
            spacing 1
            button:
                xsize 100
                action SetScreenVariable("stats_display", "stats"), With(dissolve)
                text "Stats" style "pb_button_text"
            button:
                xsize 100
                action SetScreenVariable("stats_display", "pro"), With(dissolve)
                text "Pro Stats" style "pb_button_text"
        
        vbox:
            yfill True
            yoffset 195
            spacing 2
            xmaximum 218
            
            if stats_display == "stats":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    pos (4, 40)
                    yminimum 285
                    
                    # STATS ============================>
                    hbox:
                        xanchor -2
                        if eqtarget == hero:
                            $ stats = ["constitution", "charisma", "intelligence", "fame", "reputation", "libido"]
                        else:
                            $ stats = ["constitution", "charisma", "intelligence", "character", "reputation", "joy", "disposition"]
                        vbox:
                            style_group "stats"
                            spacing -7
                            xanchor 2
                            xmaximum 113
                            frame:
                                xysize (207, 8)
                                text "{color=#CD4F39}Health:" xalign (0.02)
                            frame:
                                xysize (207, 8)
                                text "{color=#43CD80}Vitality:" xalign (0.02)
                            for stat in stats:
                                frame:
                                    xysize (207, 8)
                                    text ('{color=#79CDCD}%s'%stat.capitalize()) color ivory size 17 xalign (0.02) 
                        vbox:
                            yalign (0.65)
                            spacing 8
                            xanchor 20
                            xfill True
                            xminimum 0
                            xmaximum 120
                            
                            if eqtarget.health <= eqtarget.get_max("health")*0.3:
                                text (u"{color=[red]}%s/%s"%(eqtarget.health, eqtarget.get_max("health"))) style "stats_value_text" xalign (1.0)
                            else:
                                text (u"{color=#F5F5DC}%s/%s"%(eqtarget.health, eqtarget.get_max("health"))) style "stats_value_text" xalign (1.0)
                            if eqtarget.vitality <= eqtarget.get_max("vitality")*0.3:
                                text (u"{color=[red]}%s/%s"%(eqtarget.vitality, eqtarget.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                            else:
                                text (u"{color=#F5F5DC}%s/%s"%(eqtarget.vitality, eqtarget.get_max("vitality"))) style "stats_value_text" xalign (1.0)
                        
                            for stat in stats:
                                text ('{color=#F5F5DC}%d/%d'%(getattr(eqtarget, stat), eqtarget.get_max(stat))) style "stats_value_text" xalign (1.0)
            
                # BATTLE STATS ============================>
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    yalign 1.0
                    xpos 4
                    yoffset -201
                    xmaximum 218
                    ypadding 10
                    
                    vbox:
                        text (u"{size=18}{color=#CDCDC1}{b}Battle Stats:") xalign(0.49) style_group "ddlist"
                        style_group "stats"
                        spacing -6
                        $ stats = [("Attack", "#CD4F39"), ("Defence", "#dc762c"), ("Magic", "#8470FF"), ("MP", "#009ACD"), ("Agility", "#1E90FF"), ("Luck", "#00FA9A")]
                        
                        null height 10
                    
                        for stat, color in stats:
                            frame:
                                xysize (207, 31)
                                text "[stat]" color color size 16 align (0.02, 0.5)
                                text "{}/{}".lower().format(getattr(eqtarget, stat.lower()), eqtarget.get_max(stat.lower())) style "stats_value_text" color color size 16 align (0.98, 0.5)
            
            elif stats_display == "pro":
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    pos (4, 40)
                    ymaximum 460
    
    # Right Frame: =====================================>
    vbox:
        align (1.0, 1.0)
        fixed:
            xalign 0.5
            xysize (350, 260)
            vbox:
                yoffset 3
                xalign 0.55
                yfill True
                style_group "pb"
                
                python:
                    if len(eqtarget.traits.basetraits) == 1:
                        classes = list(eqtarget.traits.basetraits)[0].id
                    elif len(eqtarget.traits.basetraits) == 2:
                        classes = list(eqtarget.traits.basetraits)
                        classes.sort()
                        classes = ", ".join([str(c) for c in classes])
                    else:
                        if eqtarget != hero:
                            raise Exception("Character without prof basetraits detected! line: 267, girlsprofile screen")
                        else:
                            classes = "MC baseclasses are still AFK :("
                
                # TOOLTIP TEXT ====================================>
                frame:
                    background Frame(Transform("content/gfx/frame/ink_box.png", alpha=0.4), 10, 10)
                    xoffset -2
                    xpadding 10
                    xysize (346, 110)
                    has hbox spacing 1
                    xfill True
                    yfill True
                    
                    $ t = "{vspace=17}Classes: [classes]\nLocation: [eqtarget.location]\nAction: [eqtarget.action]{/color}"
                    
                    if (not tt.value and inv_source == eqtarget) and eqtarget.status == "slave":
                        text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Slave%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
                    elif (not tt.value and inv_source == eqtarget) and eqtarget.status == "free":
                        text (u"{color=[gold]}[eqtarget.name]{/color}{color=#ecc88a}  is Free%s" % t) size 14 align (0.55, 0.65) font "fonts/TisaOTM.otf" line_leading -5
                    
                    #if isinstance(tt.value, BE_Action):
                        #$ element = tt.value.get_element()
                        #if element:
                            #fixed:
                                #xysize (80, 80)
                                #yalign 0.5
                                #if element.icon:
                                    #$ img = ProportionalScale(element.icon, 70, 70)
                                    #add img align (0.5, 0.5)
                        #text tt.value.desc style "content_text" size 18 color "#ecc88a" yalign 0.1
                    
                    elif tt.value:
                        text (u"{color=#ecc88a}%s" % tt.value) size 14 align (0.5, 0.5) font "fonts/TisaOTM.otf" line_leading -5
                
                # Right Frame Buttons ====================================>
                hbox:
                    xalign 0.5
                    ypos 3
                    spacing 2
                    button:
                        align (0.5, 0.5)
                        xsize 70
                        action SelectedIf(eqtarget == hero or inv_source == hero), If(eqtarget != hero, true=[SetVariable("inv_source", hero), Function(eqtarget.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return']), With(dissolve)]) 
                        hovered tt.Action("Equip from [hero.nickname]'s Inventory")
                        text "Hero" style "pb_button_text"
                    null width 100
                    button:
                        align (0.5, 0.5)
                        xsize 70
                        action SelectedIf(inv_source != hero), SensitiveIf(eqtarget != hero), If(eqtarget != hero, true=[SetVariable("inv_source", eqtarget), Function(eqtarget.inventory.apply_filter, hero.inventory.filter), Return(['con', 'return']), With(dissolve)])
                        hovered tt.Action("Equip from [eqtarget.nickname]'s Inventory")
                        text "Girl" style "pb_button_text"
                button:
                    ypos 17
                    align (0.5, 0.5)
                    xysize (110, 30)
                    action If(eqtarget != hero, true=Show("pyt_girls_list1"))
                    text "Girls List" style "pb_button_text"
                
                frame:
                    background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
                    align (0.5, 1.0)
                    xysize (345, 80)
                    vbox:
                        align (0.55, 0.5)
                        spacing 1
                        hbox:
                            button:
                                align (0.5, 0.5)
                                xysize (140, 30)
                                action Return(["equip_for"])
                                text "Auto Equip" style "pb_button_text"
                            button:
                                align (0.5, 0.5)
                                xysize (140, 30)
                                action If(eqtarget != hero, true=Return(["jump", "item_transfer"]))
                                text "Items Transfer" style "pb_button_text"
                        
                        # Paging: ====================================>
                        use paging(ref=inv_source.inventory, use_filter=False, xysize=(250, 20), align=(0.5, 0.5))
        
        # Filters: ====================================>
        frame:
            style_group "dropdown_gm"
            background Null()
            xalign 0.5
            hbox:
                spacing 4
                xalign 0.5
                xminimum 350
                xmaximum 350
                box_wrap True
                for filter in inv_source.inventory.ALL_FILTERS:
                    frame:
                        xpadding 0
                        ymargin -8
                        background Null() 
                        $ img = ProportionalScale("content/gfx/interface/buttons/filters/%s.png" % filter, 44, 44)
                        $ img_hover = ProportionalScale("content/gfx/interface/buttons/filters/%s hover.png" % filter, 44, 44)
                        $ img_selected = ProportionalScale("content/gfx/interface/buttons/filters/%s selected.png" % filter, 44, 44)
                        imagebutton:
                            idle img
                            hover Transform(img_hover, alpha=1.1)
                            selected_idle img_selected
                            selected_hover Transform(img_selected, alpha=1.15)
                            action [Function(inv_source.inventory.apply_filter, filter), SelectedIf(filter == inv_source.inventory.filter)], With(dissolve)
                            focus_mask True
        
        # Inventory: ====================================>
        frame:
            xalign 0.55
            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.7)
            use items_inv(char=inv_source, main_size=(333, 333), frame_size=(80, 80), return_value=['item', 'equip'])
            ypos -2
        
    # BASE FRAME 1 "top layer" ====================================>
    add "content/gfx/frame/h1.png"
    
    #imagebutton: # Add this button when the screen is ready :Gismo
        #pos (178, 70)
        #idle im.Scale("content/gfx/interface/buttons/close2.png", 35, 35)
        #hover im.Scale("content/gfx/interface/buttons/close2h.png", 35, 35)
        #action Return(['control', 'return'])
        #hovered tt.Action("Return to previous screen!")
    
screen pyt_girls_list1(source=None, page=0, total_pages=1):
    modal True
    zorder 1
    
    key "mousedown_3" action Hide("pyt_girls_list1")
    
    frame:
        at fade_in_out()
        background Transform(Frame(im.MatrixColor("content/gfx/frame/Mc_bg3.png", im.matrix.brightness(-0.2)), 5, 5), alpha=0.3)
        xysize (710, 295)
        align (0.39, 0.998)
        vbox:
            align (0.5, 0.0)
            hbox:
                style_group "pb"
                align (0.5, 0.0)
                xfill True
                button:
                    align (0.5, 0.0)
                    xysize (100, 30)
                    action Return(["equip_for"])
                    text "Team" style "pb_button_text"
                button:
                    align (0.5, 0.0)
                    xysize (100, 30)
                    action Return(["equip_for"])
                    text "Status" style "pb_button_text"
                imagebutton:
                    #xoffset 9
                    yoffset -3
                    align (1.0, 0.0)
                    idle ("content/gfx/interface/buttons/close3.png")
                    hover ("content/gfx/interface/buttons/close3_h.png")
                    action Hide("pyt_girls_list1")
                
                    
screen itemstats2(item=None, char=None, size=(635, 380), style_group="content", mc_mode=False):
    if item:
        fixed:
            maximum (size[0], size[1])
            vbox:
                align (0.5, 0.5)
                yfill True
                hbox:
                    align (0.5, 0.5)
                    xfill True
                    imagebutton:
                        xoffset -9
                        yoffset -3
                        align (0.0, 0.5)
                        idle ("content/gfx/interface/buttons/discard.png")
                        hover ("content/gfx/interface/buttons/discard_h.png")
                        #hovered tt.Action("Discard item") ## (need to do) The girl equipment screen has its own Tooltip, need fix to show on him :Gismo
                        action NullAction() ## (need to do) Need to add ability to discard :Gismo
                    frame:
                        align (1.0, 0.5)
                        xoffset -29
                        xysize (439, 20)
                        background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                        label ('[item.id]') text_color gold xalign 0.5 text_size 19 text_outlines [(1, "#000000", 0, 0)] text_style "interactions_text"
                    imagebutton:
                        xoffset 9
                        yoffset -3
                        align (1.0, 0.5)
                        idle ("content/gfx/interface/buttons/close3.png")
                        hover ("content/gfx/interface/buttons/close3_h.png")
                        action Return(['con', 'return']) ## (need to do) In addition, need to add the ability to close with right-click  :Gismo
                        #hovered tt.Action("Close item info")
                vbox:
                    yfill True
                    align (0.5, 0.5)
                    null height -14
                    label ('{color=#ecc88a}_____________________________________') text_style "stats_value_text" align (0.5, 0.5)
                    hbox:
                        align (0.5, 0.5)
                        xfill True
                        frame:
                            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                            xysize (180, 130)
                            align (0.0, 0.5)
                            xoffset -5
                            vbox:
                                style_group "stats"
                                spacing -7
                                xfill True
                                null height 15
                                frame:
                                    xsize 170
                                    text ('Price:') color gold yalign 0.5
                                    label ('{size=-4}{color=[gold]}[item.price]') style "stats_value_text" align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                frame:
                                    xsize 170
                                    text ('{color=#F5F5DC}Slot:') yalign 0.5
                                    label ('{color=#F5F5DC}{size=-4}%s'%item.slot.capitalize()) style "stats_value_text" align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                frame:
                                    xsize 170
                                    text ('{color=#F5F5DC}Type:') yalign 0.5
                                    label ('{color=#F5F5DC}{size=-4}%s'%item.type.capitalize()) style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                frame:
                                    xsize 170
                                    text ('{color=#F5F5DC}Sex:') yalign 0.5
                                    if item.sex == 'male':
                                        label ('{color=#F5F5DC}{size=-4}{color=#FFA54F}%s'%item.sex.capitalize()) style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                    if item.sex == 'female':
                                        label ('{color=#F5F5DC}{size=-4}{color=#FFAEB9}%s'%item.sex.capitalize()) style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                    if item.sex == 'unisex':
                                        label ('{color=#F5F5DC}{size=-4}%s'%item.sex.capitalize()) style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                        
                        button:
                            style_group "pb"
                            align (0.0, 0.5)
                            xysize (80, 45)
                            action SensitiveIf(False), Return(['item', 'equip/unequip'])
                            if inv_source == hero: ## Item transfer - amount 1 :Gismo
                                text "Give to\n {color=#FFAEB9}Girl{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                            else:
                                text "Give to\n {color=#FFA54F}Hero{/color}" style "pb_button_text" align (0.5, 0.5) line_leading 3
                        
                        frame:
                            align (0.5, 0.5)
                            background Frame("content/gfx/frame/frame_it2.png", 5, 5)
                            xysize (120, 120)
                            add (ProportionalScale(item.icon, 100, 100)) align(0.5, 0.5)
                    
                        button:
                            style_group "pb"
                            align (1.0, 0.5)
                            xysize (80, 45)
                            if item_direction == 'unequip':
                                $ temp = "Unequip"
                            elif item_direction == 'equip':
                                $ temp = "Equip"
                            action Return(['item', 'equip/unequip'])
                            text "[temp]" style "pb_button_text" align (0.5, 0.5)
                    
                        frame:
                            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                            xysize (180, 130)
                            align (1.0, 0.5)
                            xoffset 5
                            side "c r":
                                xalign 0.5
                                viewport id "item_info":
                                    draggable True
                                    mousewheel True
                                    has vbox
                                    style_group "stats"
                                    vbox:
                                        spacing -7
                                        xysize (160, 10000)
                                        null height 5
                                        if item.mod:
                                            label ('Stats:') text_size 18 text_color gold align (0.6, 0.5)
                                            for stat, value in item.mod.items():
                                                vbox:
                                                    xfill True
                                                    frame:
                                                        xsize 170
                                                        text (u'{color=#F5F5DC}%s' % stat.capitalize()) size 16 yalign 0.5
                                                        label (u'{color=#F5F5DC}{size=-4}[value]') style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                        if item.mod:
                                            null height 7
                                        if item.max:
                                            label ('Max') text_size 16 text_color gold align (0.59, 0.5)
                                            for stat, value in item.max.items():
                                                vbox:
                                                    xfill True
                                                    frame:
                                                        xsize 170
                                                        text (u'{color=#F5F5DC}%s'%stat.capitalize()) size 16 yalign 0.5
                                                        label (u'{color=#F5F5DC}{size=-4}[value]') style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                                        if item.mod or item.max:
                                            null height 7
                                        if item.min:
                                            label ('Min') text_size 16 text_color gold align (0.59, 0.5)
                                            for stat, value in item.min.items():
                                                if True:
                                                    vbox:
                                                        xfill True
                                                        frame:
                                                            xsize 170
                                                            text(u'{color=#F5F5DC}%s'%stat.capitalize()) size 16 yalign 0.5
                                                            label (u'{color=#F5F5DC}{size=-4}%d'%value) style "stats_value_text" xalign 1.0 align (1.0, 0.5) text_outlines [(1, "#3a3a3a", 0, 0)]
                    
                    null height -14
                    label ('{color=#ecc88a}_____________________________________') text_style "stats_value_text" align (0.5, 0.5)
                    hbox:
                        align (0.5, 0.5)
                        xfill True
                        yoffset -3
                        frame:
                            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                            xysize (158, 104)
                            align (1.0, 0.5)
                            xoffset -5
                            side "c r":
                                xalign 0.5
                                viewport id "item_info":
                                    draggable True
                                    mousewheel True
                                    has vbox
                                    style_group "stats"
                                    vbox:
                                        xoffset 2
                                        spacing -7
                                        xysize (120, 10000)
                                        
                                        if (not mc_mode and item.addeffects) or (not mc_mode and item.removeeffects):
                                            hbox:
                                                align (0.8, 0.5)
                                                label ('Effects:') text_size 16 text_color gold xoffset 7
                                                add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 25
                                                add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 25
                                            vbox:
                                                spacing -7
                                                xfill True
                                                for effect in item.addeffects:
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#43CD80}%s'%effect.capitalize()) size 16 yalign 0.5
                                                for effect in item.removeeffects:
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#CD4F39}%s'%effect.capitalize()) size 16 yalign 0.5
                        frame:
                            xysize (382, 104)
                            xalign 0.5
                            xoffset -7
                            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.1)), 5, 5), alpha=0.9)
                            side "c r":
                                xalign 0.5
                                xysize (360, 94)
                                viewport:
                                    id "item.desc"
                                    mousewheel True
                                    text ('{color=#ecc88a}[item.desc]') font "fonts/TisaOTM.otf" size 16 outlines [(1, "#3a3a3a", 0, 0)] xalign 0.5
                                vbar value YScrollValue("item.desc")
                    
                        frame:
                            background Transform(Frame(im.MatrixColor("content/gfx/frame/p_frame5.png", im.matrix.brightness(-0.05)), 5, 5), alpha=0.9)
                            xysize (158, 104)
                            align (1.0, 0.5)
                            xoffset -9
                            side "c r":
                                xalign 0.5
                                viewport id "item_info":
                                    draggable True
                                    mousewheel True
                                    has vbox
                                    style_group "stats"
                                    vbox:
                                        xoffset -5
                                        spacing -7
                                        xysize (120, 10000)
                                        
                                        if (not mc_mode and item.addtraits) or item.removetraits:
                                            hbox:
                                                align (0.8, 0.5)
                                                label ('Traits:') text_size 16 text_color gold xoffset 8
                                                add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 26
                                                add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 26
                                            vbox:
                                                spacing -7
                                                xfill True
                                                for trait in item.addtraits:
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#43CD80}%s'%trait.capitalize()) size 16 yalign 0.5
                                                for trait in item.removetraits:
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#CD4F39}%s'%trait.capitalize()) size 16 yalign 0.5
                                        
                                        if (not mc_mode and item.addtraits) or item.removetraits:
                                            null height 7
                                        
                                        if item.add_be_spells or item.remove_be_spells: ## Need to check whether or not working :Gismo
                                            hbox:
                                                align (0.8, 0.5)
                                                label ('Skills:') text_size 16 text_color gold xoffset 8
                                                add "content/gfx/interface/images/add.png" yalign 0.7 xoffset 26
                                                add "content/gfx/interface/images/remove.png" yalign 0.9 xoffset 26
                                            for skill in item.add_be_spells:
                                                vbox:
                                                    xfill True
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#43CD80}%s'%skill.capitalize()) size 16 yalign 0.5
                                            for skill in item.remove_be_spells:
                                                vbox:
                                                    xfill True
                                                    frame:
                                                        xsize 142
                                                        text(u'{color=#CD4F39}%s'%skill.capitalize()) size 16 yalign 0.5
                                                        
                                                        
screen diff_item_effects(char, dummy):
    zorder 10
    textbutton "X":
        align (1.0, 0.0)
        action Hide("diff_item_effects")
    frame:
        xysize (1000, 500)
        background Solid("#F00", alpha=0.1)
        align (0.1, 0.5)
        has hbox
        
        vbox:
            text "Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(getattr(dummy, stat) - getattr(char, stat))
        vbox:
            text "Max Stats:"
            for stat in char.stats:
                text "[stat]: {}".format(dummy.get_max(stat) - char.get_max(stat))
        vbox:
            for skill in char.stats.skills:
                text "[skill]: {}".format(dummy.get_skill(skill) - char.get_skill(skill))
        vbox:
            text "Traits (any):"
            python:
                t_old = set(t.id for t in char.traits)
                t_new = set(t.id for t in dummy.traits)
                temp = t_new.difference(t_old)
                temp = sorted(list(temp))
            for t in temp:
                text "[t]"