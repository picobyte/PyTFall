label mc_setup_merchant:
    "Setting up main Merchant effects here!"
    return
    
label mc_setup_merchant_caravan:
    "Setting up main Merchant-Caravan effects here!"
    return
    
label mc_setup_merchant_mc_defender:
    "MC Caravan Defender Option Reporting!"
    return
    
label mc_setup_merchant_mc_defender_sword:
    "MC Caravan Defender Sword Option Reporting (Finally)!"
    return

label mc_setup_warrior:
    $ pass
    return
    
label mc_setup_warrior_warrior: # naturally, I dunno how to properly set base classes
    "Warrior class"
    return
    
label mc_setup_warrior_defender:
    "Defender class"
    return
    
label mc_setup_warrior_shooter:
    "Shooter class"
    return
    
label mc_setup_warrior_assassin:
    "Assassin class"
    return
    
label mc_setup_warrior_warrior_amazon: 
    $ hero.apply_trait("Amazon Blood")
    return
    
label mc_setup_warrior_warrior_amazon_training:
    $ hero.apply_trait("Amazon Training")
    return
    
label mc_setup_warrior_warrior_amazon_muscle:
    $ hero.apply_trait("Amazon Musculature")
    return
    
label mc_setup_warrior_warrior_amazon_yuri:
    $ hero.apply_trait("Yuri Expert")
    
label mc_setup_warrior_warrior_dragon:
    $ hero.apply_trait("Dragon Blood")
    return
    
label mc_setup_warrior_warrior_dragon_fire:
    $ hero.apply_trait("Fire Dragon Scales")
    return
    
label mc_setup_warrior_warrior_dragon_stone:
    $ hero.apply_trait("Stone Dragon Scales")
    return
    
label mc_setup_warrior_warrior_dragon_defiler:
    $ hero.apply_trait("Defiler Dragon Scales")
    return
    
label mc_setup_warrior_assassin_princess:
    $ hero.apply_trait("Royal Blood")
    return
    
label mc_setup_warrior_assassin_princess_knight:
    $ hero.apply_trait("Knightly Stance")
    return
    
label mc_setup_warrior_assassin_princess_fencer:
    $ hero.apply_trait("Sword Master")
    return
    
label mc_setup_warrior_assassin_princess_sister:
    $ hero.apply_trait("Sister Lover")
    # TODO for Xela: chars with half-sister trait should have +400 disposition instead of usual +200
    return
    
label mc_setup_warrior_assassin_drow:
    $ hero.apply_trait("Drow Blood")
    return
    
label mc_setup_warrior_assassin_drow_poison:
    $ hero.apply_trait("Poison Master")
    return
    
label mc_setup_warrior_assassin_drow_dagger:
    $ hero.apply_trait("Dagger Master")
    return
    
label mc_setup_warrior_assassin_drow_flex:
    $ hero.apply_trait("Flexible")
    return
    
label mc_setup_warrior_shooter_forest_elf:
    $ hero.apply_trait("Forest Elf Blood")
    return
    
label mc_setup_warrior_shooter_forest_elf_sniper:
    $ hero.apply_trait("Bow Master")
    return

label mc_setup_warrior_shooter_forest_elf_ranger:
    $ hero.apply_trait("Ranger")
    return
    
label mc_setup_warrior_shooter_forest_elf_features:
    $ hero.anal += 50
    $ hero.ANAL += 50
    $ hero.apply_trait("Elven Features")
    return
    
label mc_setup_warrior_shooter_summer_fay:
    $ hero.apply_trait("Fae Blood")
    return
    
label mc_setup_warrior_shooter_summer_fay_eternal:
    $ hero.apply_trait("Summer Eternality")
    return
    
label mc_setup_warrior_shooter_summer_fay_affinity:
    $ hero.attack_skills.append("Summer Arrow")
    $ hero.apply_trait("Summer Affinity")
    return
    
label mc_setup_warrior_shooter_summer_fay_beacon:
    $ hero.apply_trait("Life Beacon")
    return
    