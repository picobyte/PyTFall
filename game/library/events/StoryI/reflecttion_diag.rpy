init python:
    def eyewarp(x):
        return x**1.33
    eye_open = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=False, time_warp=eyewarp)
    eye_shut = ImageDissolve("content/gfx/masks/eye_blink.png", 1.5, ramplen=128, reverse=True, time_warp=eyewarp)
    
init:
    image carstein = ProportionalScale("content/events/StoryI/Eric Carstein.png", 1700, 500)
    $ ec_neutral = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_neutral.png")
    $ ec_sad = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_sad.png")
    $ ec_scared = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_scared.png")
    $ ec_happy = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_happy.png")
    $ ec_angry = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_angry.png")
    $ ec_d = Character("Carstein", color=white, what_color=white, show_two_window=True, show_side_image="content\events\StoryI\Carstein_d.png")
    image bag = ProportionalScale("content/items/quest/bag.png", 150, 150)
    image clocks = ProportionalScale("content/items/quest/cl2.png", 150, 150)
    image letter = ProportionalScale("content/items/quest/letter.png", 150, 150)
    image box = ProportionalScale("content/items/quest/box.png", 150, 150)
    
label intro_story_ad:
    stop world
    stop music
    scene black with dissolve
    play world "cemetery.ogg" fadein 2.0 loop
    show expression Text("City Cemetery", style="tisa_otm", align=(0.5, 0.33), size=40) as txt1:
        alpha 0
        linear 3.5 alpha 1.0
    pause 2.5
    hide txt1
    show bg cemetery with dissolve
    "You found the cemetery very soon with the help of locals. It does not look abandoned, but you are almost alone here."
    "..."
    "But after two hours of searching you found nothing."
    show bg story tombstone with dissolve
    show carstein at center with dissolve
    ec_sad "..."
    "On the very edge you see an old man standing next to a tombstone. Maybe he is the author of the letter? You come closer with caution."
    ec_happy "Well hello there youngster."
    "His voice is low and raspy."
    ec_happy "Not many people come to this place these days. Do you have some business with me?"
    $ cem = 0
    label cem_diag:
    menu:
        "Look at the tombstone next to him":
            "Nope, it's not your father. You can not make out the name, but the surname is 'Carstein'."
            jump cem_diag
        "Ask about the cemetery":
            ec_neutral  "Ah yes, you see, after the riot there were too many dead bodies to bury, so we started to burn them." 
            ec_neutral  "Over time it has become a tradition, and cemeteries are no longer used as before."
            ec_neutral "That's why not many people come here these days. <he glances at the tombstone nearby>"
            jump cem_diag
        "Ask what is he doing here":
            ec_happy "<he laughs softly> The same thing as you, I presume. Pay tribute to the fallen."
            jump cem_diag
        "Ask about your father's grave":
            ec_d "Oh, so you are looking for HIM. I'm afraid he is not here. I don't know where he is. Maybe nobody knows."
            $ cem = 1
            jump cem_diag
        "Leave" if cem == 1:
            "You turning around, going to leave this place. Obviously, the letter was someone's joke."
            ec_neutral "But if you looking for anyone else, we can help each other, [hero.name]."
    "You stop. Does he know you?"
    ec_neutral "Allow me to introduce myself, boy. I am Eric Carstein, retired militia officer."
    ec_neutral "I used to know your father. Now I'm just a tired old man, but I still have some connections with military."
    label cem_diag1:
    menu:
        "Ask about the letter":
            ec_neutral "So, you got a letter too? In fact, I have a similar letter telling me to meet you here today."
            ec_neutral "I don't know who sent them. Handwriting analysis showed complete nonsense."
            jump cem_diag1
        "Ask about the papers of your father":
            ec_d "<he doesn't look interested> Ah yes, he used to work on something. I don't know what it was, and I don't want to know too."
            ec_neutral "I already know enough to sleep bad at night. <he winks at you> Let's not worsen the situation."
            jump cem_diag1
        "Ask about your father":
            ec_neutral "We were friends from childhood. Always wanted to make a military career."
            ec_sad "And we both succeeded in killing people. I was on the battlefield, your father was in the laboratory."
            jump cem_diag1
        "Show him your letter":
            show letter at center with dissolve
            "You show him the letter you received two weeks ago. He carefully examines it for a minute or so."
            ec_neutral "It is the same handwriting, I'm sure of it. <he gazes at you> I don't know what is it about, but to be manipulated is never a good thing."
            hide letter with dissolve
    ec_neutral "I have a proposition. <he gives you a bag of coins> Here, consider it a payment for that letter of yours. Buy yourself a house. Find a job. Gather some money."
    ec_neutral "I believe we can be helpful to each other. If you help me to understand something, I will help you the best I can in return. We even can try to find your father, if you intend to follow the letter."
    $ hero.gold+= 500
    "Here we give a quest to buy a house and collect, let's say, 5000 gold and get to lvl 5." #quest
    ec_neutral "<he gives you address> This is where I live. Meet me there when you will be ready. Until then..."
    hide carstein with dissolve
    "He left. After a short while you go back to the city. At least that letter brought you some money."
    stop world fadeout 2.0
    scene black with dissolve
    
label intro_story_hj:
    stop music
    stop world
    scene black with dissolve
    play world "Town5.ogg" fadein 2.0 loop
    show bg story cab with dissolve
    show carstein at center with dissolve
    "You managed to settle a bit for the last days. You came to Carstein as he asked and told that you are ready."
    ec_neutral "Good, very good. During this time I learned something new about our... case."
    "You sit on a luxury sofa. It's very comfortable and most likely worth more than your house."
    label last_carst:
    menu:
        "Ask about your father's grave":
            ec_happy "Ah, you see, nobody knows where is he. At least no one alive in the city. <he grins slightly>"
            jump last_carst
        "Ask about the letter":
            ec_neutral "Nothing new here. It's the same paper, the same inks, the same handwriting."
            ec_neutral "But letters are identical to each other. Yet the force pressing the paper is different, so it shouldn't be written by a machine."
            ec_sad "<sigh> ...Or at least my connections think so."
            jump last_carst
        "Ask about new clues":
            ec_neutral "Yes, yes. <he looks at you> Do you know what happened in 3596?"
            $ a = 0
            $ b = 0
            $ c = 0
            label last_carst1:
            menu:
                "My father died" if a == 0:
                    $ a = 1
                    ec_sad "Yes, indeed. A tragedy, but just one of many. There are witnesses of his death, but no one saw what happened to his body after."
                    jump last_carst1
                "The city was wiped out" if b == 0:
                    $ b = 1
                    ec_neutral "Close, but not truth. We lost a quarter of the city. Mainly the slave army was affected, because we managed to gather rebels in one place."
                    jump last_carst1
                "Slaves rebellion" if c == 0:
                    $ c = 1
                    ec_neutral "Indeed, but they happened almost every year back then. Although it was a big one, perhaps the biggest one."
                    ec_sad "<you are alone in the room, but he lowers his voice anyway> They say someone helped them. Someone gave them weapons and magic to fight back."
                    ec_sad "But in the end they were manipulated by someone. The riot was a consequence, not a cause."
                    jump last_carst1
                "Enough with history" if a == 1 or b == 1 or c == 1:
                    ec_happy "<he makes a short laugh> As you say, young man. After all, if you want to know the official history, you can go to the library."
                    ec_neutral "Unfortunately, the red flash that vaporized the army of slaves also destroyed most of the clues. The official story for the most part consists of assumptions and propaganda."
                    ec_neutral "And the user of the weapon lost his mind, so he is useless to us..."
    ec_happy "However, I have an idea where we should start looking."
    ec_neutral "The weapon used during the riot was found in ruins not very far from the city. They say an itinerant historian came to the city and told us where to find it."
    ec_neutral "<sigh> And everything he said was true. The riot ended with a single flash. The city has grown and become rich."
    ec_neutral "And he never told us about the consequences for one who used it. So technically, he did not lie in anything."
    ec_sad "<he frowns> Very convenient. But there is more. Nobody remembers how he looked. Initially I had hoped to find him, and questioned eyewitnesses for many years."
    ec_neutral "So now I want you to send an expedition to the ruins he mentioned. This is the best clue I have. The information about its location is classified, so most likely nobody was there after Terumi."
    ec_neutral "See if you can find something. Anything."
    "You get up to leave."
    ec_sad "...And be careful. Do not tell anyone about our conversation."
    # And so we give a quest to find ruins deep in SE. When the group will return, MC will know that ruins were sealed by impenetrable stone wall.
    # At the wall there is the same symbol you saw at Sakura's equipment.
    scene black with dissolve
    stop music fadeout 2.0