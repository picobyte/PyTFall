﻿label start:
    # Trying to fix Git...
    
    $ renpy.block_rollback()
    if config.debug:
        $ renpy.show_screen("debug_tools", _layer="pytfall")
        show screen debug_tools
        
    python:
        # Global variables and loading content:
        day = 1
        # difficulty = Difficulties()

        # load json schemas for validation
        jsstor.configure(timelog=tl)

        # Load random names selections for rGirls:
        tl.timer("Loading: Random Name Files")
        female_first_names = load_female_first_names(200)
        male_first_names = load_male_first_names(200)
        random_last_names = load_random_last_names(200)
        random_team_names = load_team_names(50)
        
        # Load random names selections for Teams:
        file = open(content_path("db/RandomTeamNames_1.txt"))
        randomTeamNames = file.readlines()
        shuffle(randomTeamNames)
        file.close()
        
        tl.timer("Loading: PyTFallWorld", nested=False)
        pytfall = PyTFallWorld()
        
        tl.timer("Loading: Menu Extensions", nested=False)
        menu_extensions = MenuExtension()
        menu_extensions["Abby The Witch Main"] = []
        menu_extensions["Xeona Main"] = []
        tl.timer("Loading: Menu Extensions")
        
        # Create locations:
        locations = dict()
        temp = Apartments()
        locations[temp.id] = temp
        temp = Streets()
        locations[temp.id] = temp
        del temp
            
        # Load all game elements:
        tl.timer("Loading: Traits")
        traits = load_traits()
        
        # This should be reorganized later:
        tgs = object() # TraitGoups!
        tgs.breasts = [i for i in traits.values() if i.breasts]
        tgs.body = [i for i in traits.values() if i.body]
        tgs.base = [i for i in traits.values() if i.basetrait and not i.mob_only]
        tgs.elemental = [i for i in traits.values() if i.elemental]
        tgs.el_names = set([i.id.lower() for i in tgs.elemental])
        tgs.ct = [i for i in traits.values() if i.character_trait]
        tgs.sexual = [i for i in traits.values() if i.sexual] # This is a subset of character traits!
        tgs.race = [i for i in traits.values() if i.race]
        tgs.client = [i for i in traits.values() if i.client]
        
        tl.timer("Loading: Items", nested=False)
        items = load_items()
        items.update(load_gifts())
        
    $ tl.timer("Loading: Battle Skills", nested=False)
    $ battle_skills = dict()
    call load_battle_skills
    $ tl.timer("Loading: Battle Skills")
    
    python:
        # MC:
        hero = Player()
        
        ilists = ListHandler()
        
        tl.timer("Loading: SimpleJobs")
        # This jobs are usually normal, most common type that we have in PyTFall
        temp = [TestingJob(), WhoreJob(), StripJob(), ServiceJob(), BarJob(), Manager(), CleaningJob(), GuardJob()]
        simple_jobs = {j.id: j for j in temp}
        del temp
        
        tl.timer("Loading: Businesses", nested=False)
        adverts = load_json("buildings/adverts.json")
        businesses = load_businesses(adverts)
        
        tl.timer("Loading: Training", nested=False)
        schools = load_schools()
        pytFlagProxyStore = shallowcopy(pytFlagProxyStore)
        pytRelayProxyStore = shallowcopy(pytRelayProxyStore)
        tl.timer("Loading: Training")
        
        # maps = xml_to_dict(content_path('db/map.xml'))
        calendar = Calendar(day=28, month=2, year=125)
        global_flags = Flags()
        chars_list_last_page_viewed = 0
        
        # import cPickle as pickle
        # tl.timer("Loading: Binary Tag Database")
        # # pickle.dump(tagdb.tagmap, open(config.gamedir + "/save.p", "wb"))
        # tagdb = TagDatabase()
        # tagdb.tagmap = pickle.load(open(config.gamedir + "/save.p", "rb"))
        # tagslog.info("loaded %d images from binary files" % tagdb.count_images())
        # tl.timer()
        
    python:
        # Loading characters:
        tagdb = TagDatabase()
        for tag in tags_dict.values():
            tagdb.tagmap[tag] = set()
        tl.timer("Loading: All Characters!")
        chars = load_characters("chars", Char)
        npcs = load_characters("new_npcs", NPC)
        # Trying to load crazy characters:
        crazy_chars = load_crazy_characters()
        chars.update(crazy_chars)
        rchars = load_random_characters()
        del crazy_chars
        tl.timer("Loading: All Characters!")
        devlog.info("Loaded %d images from filenames!" % tagdb.count_images())
        
        # Build shops:
        pytfall.init_shops()
        
        # Start auto-quests
        pytfall.world_quests.first_day()
        
        tl.timer("Loading: Mobs")
        mobs = load_mobs()
        
        tl.timer("Loading: Exploration", nested=False)
        # pytfall.forest_1 = Exploration()
        fg_areas = load_fg_areas()
        
        # ---------------------------------------
        # Temporary code
        tl.timer("Loading: Generating Random girls", nested=False)
        
        # Some random girls (if there are any):
        if rchars:
            rgirls = rchars.keys()
            shuffle(rgirls)
            for i in xrange(25):
                if rgirls:
                    rgirl = rgirls.pop()
                    new_random_girl = build_rc(id=rgirl)
                else:
                    rgirls = rchars.keys()
                    shuffle(rgirls)

            del rgirls
            del rgirl
            del new_random_girl
                
            create_arena_girls()

        tl.timer("Loading: GirlsMeets", nested=False)
        gm = GirlsMeets()
        
        tl.timer("Loading: Populating SlaveMarket", nested=False)
        pytfall.sm.populate_chars_list()
        tl.timer("Loading: Populating SlaveMarket")
        
    # Loading apartments/guilds:
    call load_resources
    
label dev_testing_menu:
    if config.developer:
        menu:
            "Debug Mode":
                $ initial_levelup(hero, 100, max_out_stats=True)
                
            "Content":
                menu:
                    "Test Intro":
                        call intro
                        call mc_setup
                    "MC Setup":
                        call mc_setup
                        $ neow = True
                    "Skip MC Setup":
                        $ pass
                    "Back":
                        jump dev_testing_menu
            "GFX":
                while 1:
                    menu:
                        "Webm":
                            call test_webm
                        "Chain UDD":
                            call testing_chain_udd
                        "Test Matrix":
                            call test_matrix
                        "Test Vortex":
                            call test_vortex
                        # "Quality Test":
                            # call screen testing_image_quality
                        "FilmStrip":
                            call screen testing_new_filmstrip
                        "Particle":
                            scene black
                            show expression ParticleBurst([Solid("#%06x"%renpy.random.randint(0, 0xFFFFFF), xysize=(5, 5)) for i in xrange(50)], mouse_sparkle_mode=True) as pb
                            pause
                            hide pb
                        "Test Robert Penners Easing":
                            call screen test_penners_easing
                        "Back":
                            jump dev_testing_menu
                        
                        
        python:
            if not hasattr(store, "neow"):
                renpy.music.stop()
                mc_pics = load_mc_images()
                picbase = choice(mc_pics.keys())
                hero.img_db = mc_pics[picbase]
                del mc_pics[picbase]
                af_pics = mc_pics
                del mc_pics
                hero.say = Character(hero.nickname, color=ivory, show_two_window=True, show_side_image=hero.show("portrait", resize=(120, 120)))
                hero.restore_ap()
                hero.log_stats()
    else:
        call mc_setup
    
    python:
        tl.timer("Loading: Arena!")
        pytfall.arena = Arena()
        
        for key in af_pics:
            f = ArenaFighter()
            f.name = key
            f.img_db = af_pics[key]
            f.init()
            pytfall.arena.ac[f.name] = f
        
        del af_pics
        
        pytfall.arena.ac.update(load_arena_fighters())
        pytfall.arena.setup_arena()
        pytfall.arena.update_matches()
        pytfall.arena.update_teams()
        pytfall.arena.find_opfor()
        pytfall.arena.update_dogfights()
        tl.timer("Loading: Arena!")
        
    # Call girls starting labels:
    $ all_chars = chars.values()
    while all_chars:
        $ popped_girl = all_chars.pop()
        $ girl_unique_label = "_".join(["start", popped_girl.id])
        if renpy.has_label(girl_unique_label):
            call expression girl_unique_label
    $ del all_chars
    if girl_unique_label in globals():
        $ del girl_unique_label
        
    if "char" in store.__dict__:
        $ del store.__dict__["char"]
    if "girl" in store.__dict__:
        $ del store.__dict__["girl"]
    if "testBrothel" in store.__dict__:
        $ del store.__dict__["testBrothel"]
    
    python:
        shop_items = [item for item in items.values() if (set(pytfall.shops) & set(item.locations))]
        all_auto_buy_items = [item for item in shop_items if item.usable and not item.jump_to_label]

        trait_selections = {"goodtraits": {}, "badtraits": {}}
        auto_buy_items = {k: [] for k in ("body", "restore", "food", "dress", "rest", "warrior", "scroll")}

        for item in all_auto_buy_items:

            for k in ("goodtraits", "badtraits"):
                if hasattr(item, k):
                    for t in getattr(item, k):
                        # same item may occur multiple times for different traits.
                        trait_selections[k].setdefault(t, []).append(item)

            if item.type != "permanent":

                if item.type == "armor" or item.slot == "weapon":
                    auto_buy_items["warrior"].append(item)

                else:
                    if item.slot == "body":
                        auto_buy_items["body"].append(item)

                    if item.type in ("restore", "food", "scroll", "dress"):
                        auto_buy_items[item.type].append(item)
                    else:
                        auto_buy_items["rest"].append(item)

        for k in trait_selections:
            for v in trait_selections[k].values():
                v = sorted(v, key=lambda i: i.price)

        for k in ("body", "restore", "food", "dress", "rest", "warrior", "scroll"):
            auto_buy_items[k] = [(i.price, i) for i in auto_buy_items[k]]
            auto_buy_items[k].sort()
    
    #  --------------------------------------
    # Put here to facilitate testing:
    if config.developer and renpy.has_label("testing"):
        call testing
    
    $ jsstor.finish()
    jump mainscreen
    
label after_load:
    stop music
    return
