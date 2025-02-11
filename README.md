# Gamefied-Study-Tool
Tool that allows users to input things like lecture recordings, lecture slides, professor notes, etc... and output Doulingo-like course based on those inputs.

IDEAS:

    ideas for grand plan / future:
        - create cheap vr cardboard cutouts of headsets where you can put your phone --> give to high schools possibly for free once you partner with them
            - not sure where to go from there, lots of places though
        - see google doc for more plans
        - say you came up with and built the knowledge graph algorithm on your resume

    ideas for name:
        - name something stone related (bc you are SOLIDIFYING your knowledge (hahahahahah ok im done))

    ideas for map themes (possibly):
        - name something stone related (bc you are SOLIDIFYING your knowledge (hahahahahah ok im done))
        - could have the background be a pond / stream or something
        - could be steps to a castle, which is a boss room
        - could be peddles in a pretty stream --> waterfall / dam boss room?
        - could be rocks in a forest --> tree house boss room
        - modern rocks in a modern sleek style? (like a modern house, but with the white squares that you step on but are surrounded with water) (ok this ones a stretch)
        - could be rocks in a grassy park (could have ppl / animals having a picnic or smth)
        - could be candy rock with a candy theme?
        - ...or some sort of rock food in a luncheon / dinner / breakfast theme
        - could be rocks on a farm --> barnhouse / farmhouse boss room
        - could be future / electronic rocks --> future place?
        - could be planets / asteroids in a solar system
        - could be small scale, some sort of things in a house, maybe theres a cat w/ yarn, or a dog, or couch w/ tv and ppl moving, etc...
        - could be lava rocks in a lava stream leading up to a volcano boss room
        - could be some sort of water rocks in a ocean
        - could be rocks in an island (or actual islands)
        - could be something in a crop field
        - possibly take inspiration from btd5 / btd6 / odessey

TODO list:
    
    general:
        - change theme / color / name
        - minor page reorganization (remove header and footer in game page + make page look at least a little better)
        - put image to text ocr thing on resume maybe

    - Create course (library) page:
        - add support for links / pdfs / other things and get rid of things like difficulty, tutor, etc... then actually start generating stuff to study

    Game page:
        - remove timer
        - remove likes / clouds / diamonds? 
            - investigate what they're used for and we can probably use them later
        - remove header / footer when user is playing a game
        - change from giving questions from lots and lots of "rooms" to questions from one specific room
            - almost done, but need to make library room names have underscores instead so it will redirect and it will 
        plan for textbook stuff:
        - see purple text in tablet (continue w/ gemini flash stuff)
            1) give whole textbook to gpt to "split up" (finding a regular nlp alternative would be awesome as well - TextTiling (semantic similarity) or BERT-Topic (topic changes) or BookNLP (best for academic / long-form texts))
            2) store embeddings in pinecone (every paragraph)
            3) generate questions per every subchapter / lecture given syllabus (stored in database)
            4) user can re-generate questions easily and for cheap (cheap for me at least cost for user tbd) bc embeddings are precomputed
            5) user should delete things hopefully
        - other idea: instead of giving whole textbook to gemini to figure out ideas, just have the user input a syllabus / toc of textbook so we can get the names off the bat, or have an option to specify yourself, or have it make its own based on the input material (this would be better for unorganized courses w/ no syllabus and it would be easy for users - could make specifying yourself the default and have this for paid content?)

    - Actual map page:
        - link clicking on the "play" button link to the actual game
        - decorate the map eventually
        - figure out a way to break up room names into sections either by user request or something else


COMPLETED:
    ✅ get frontend to work
    ✅ get backend to work
    ✅ get title from library to knowledge (practice) page and make sure you ask ChatGPT for best way to do it (data() vs mounted() vs actions vs computed)
    ✅ create a course, but all it displays is the name on a card. when you click on the card (course), you are taken to the previous knowledge graph screen, and it just says the course name. Nothing too fancy just yet
    ✅ make every room_name in a library associated with a stepping stone possibly
    ✅ going off of ^^^ basically finding something to fill list of stepping stones in db
    ✅ change room names text to a good color
    ✅ add a small pop-up menu when you click on it that currently displays nothing but will display the course name possibly and the play button
            and mastery of topics in the course as well (course name could be just the topics)

RESOURCES:
    - node components: https://vueflow.dev/