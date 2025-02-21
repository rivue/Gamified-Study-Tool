# Gamefied-Study-Tool
Tool that allows users to input things like lecture recordings, lecture slides, professor notes, etc... and output Doulingo-like course based on those inputs.

IDEAS:

    ideas for grand plan / future:
        - create cheap vr cardboard cutouts of headsets where you can put your phone --> give to high schools possibly for free once you partner with them
            - not sure where to go from there, lots of places though
        - see google doc for more plans
        - say you came up with and built the knowledge graph algorithm on your resume
            - Built a custom text extraction pipeline using Optical Character Recognition to extract text from pdf textbooks with 97% accuracy
                (add image to text ocr thing on resume)
        - ADD RAG STUFF TO RESUME (INCLUDING GOOGLE VISION STUFF)
            - add gRPC stuff abt pinecone stuff
            - more advanced processing for Masters / PhD level topics (ask chatgpt, but mainly re-ranking, structured search, 
                and advanced reasonding-based prompt engineering to capture cross-section dependencies) 
            - investigate into late-chunking or late-interaction for vector embedding
            - also add multimodal and >1 file input for library / course creation

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
        - ability to "star" / "favorite" a course
        - fix low / moderate / high vulnerabilities for npm packages in frontend
        - redirects / url stuff (ex: 
            "/knowledge/:id/:anythingHereShouldRedirect"
            "/library/:id/:roomName/:anythingHereShouldRedirect"
            etc...
        )
        - make footer smaller
        - contact image on main sidebar?
        - significant ui rehaul ***
        - change gpt 40-mini to deepseek

    create course (library) page:
        - add support for links / pdfs / other things and get rid of things like difficulty, tutor, etc... then actually start generating stuff to study
        - after user submits something and is waiting, display a loading bar or wheel or something letting the user know that it is generating

    game page:
        - investigate into what clouds and diamonds in game screen were used for so I can probably use them later
        - remove time from db then remove all references to "timer", "end time" or "starting time" in gameStore.js
        - and possibly a hint button as well (3 hints per question?)
        - make it give more than 4 or 8 questions eventually
        - instead of having it flipped, just put the main contents on the page possibly? and ask them to use their applied knowledge?
        - fix the issue where anywhere on a card exits the lesson as opposed to just the red x
        - instead of multiple choice, have it where users can drag / drop for an answer slot:
            (deepseek recomendations):
            - Add haptic feedback on drop (vibration for correct/wrong).
            - Use gravity physics (e.g., answers "fall" into the slot with a bounce).
            - Animated rewards: Slot glows/explodes with confetti on correct answers.
        - once I add a second type of "game", make it "shuffle" the questions once it gets the
            8 or so least seen so that the questions seem random and they aren't just the same multiple choice every time
        - make the underscores ___ visible in the questions
        - "games":
            - one word free answer (make gpt come up with variations so people aren't pissed off w/ super close answers, ex:
                NCSU, ncsu, NC State, North Carolina State University, etc... or maybe use basic nlp to check?)
            - multiple options in a row: like with duolingo where you are given 10 or so options and you pick 4 or 5 and they have to be 
                in a specific order. this might be somewhat tricky to implement cus I have to implement drag-and-drop at the same time, so I might have to 
                think of a couple others in the mean time
            - matching pairs possibly, not sure how that would work
            - only two options as opposed to 4
            - play duolingo for inspiration
            - true / false
            - correct the statement / choose the correct portion of a paragrah / two students have different opinions make them choose the correct one
            - time attack mode option - questions might be a little easier possibly or not
            - image based questions - not sure how that would work how how we would ensure accuracy
            - drag-and-drop labels (label the x axis, y axis, identify what the mean is, etc...)
            - hotspot questions (click on X in this diagram)
            - sentence completion
            - category sorting (sort these into mammals, birds, and reptiles) - could be for easier questions
            - timeline creation - drag and drop events
            - venn diagram sorting - sort these things into squares, circles, or both
            - fill in the table (a periodic table w/ missing elements)
            - analogies: newton is to physics as darwin is to ___
            - debate mode: users choose a side in a debate and answer questions to support their argument
            - case studies: users analyze a real-world scenario and answer questions based on it
            - hypothesis testing: users propose a hypothesis and answer questions to test it
            - multi-step problem (would get to this later down the line)
            - creative writing (this would be hard w/o llms - maybe could use rlly advanced nlp to detect it? or ask chatgpt to give it things to look for)
            - compare and contrast two items
            - predict the outcome
            - error detection (users identify and correct errors in a passage, equation, or diagram)
            - ranking tasks: users rank tasks on order of importance, size, or chronology
            - mind mapping: users create a mind map by connecting related ideas
            - math / chemistry equation builder
            - historical role-playing: answer questions based on the perspective of a historical figure
            - build a circuit by connecting components
            - analyze a passage from a book and answer questions based on it
            - geography pinpoint: users click on a map to answer geography questions (where is paris)
            - physics simulation: users adjust variables in a simulation and answer questions about the outcome
            - users analyze a legal case and answer questions about the ruling or implications
            - users design a solution to an engineering problem (eg: build a bridge that can support 100kg)
            - users answer questions about the steps of the scientific method based on a given experiment

        - unlockable card grid:
            Pros:
                - Visual progression (users see their journey mapped out).
                - Creates curiosity ("What’s behind the locked card?").
                - Feels like a "level map" (common in games like Candy Crush).
            Cons:
                - Overwhelming if too many cards are visible upfront.
                - Risk of users feeling "stuck" if they can’t progress.
            Improvements:
                - Hide cards behind thematic obstacles (e.g., unlock a "forest path" by answering questions to "clear vines").
                - Let users choose their path (branching paths with optional challenges).
                - Add hidden power-ups in unlocked cards (e.g., skip a question, double points).

    uploading / retrieving submitted materials:
        plan for textbook stuff:
        - see purple text in tablet (continue w/ gemini flash stuff)
                - what to do if document generation fails?
                - add multiple file upload later
                - add delete file from library feature
                - user can change room name? possibly
                - make sure every thing is created successfully before adding anything to database possibly?
                - reorganize pinecone processing stuff maybe a bit (put pinecone stuff in a pinecone file?)
                - error handling. and lots of it.
                - make finished library redirect to library map
                - support links for more context possibly? (maybe it would be more of a room specific thing?)
                - fix weird website not working issue (I think it happens right after login)
                - remove image stuff for library and replace with plain color (user can choose color, maybe something out of 12 or something)
                - add times_seen variable in the library factoid database when a user "sees" the question so we can start giving the user the least seen 8 out of 20 questions each time or something
                - all the other routes and stuff (contact / submit feedback, terms & policies, buying subscription, settings)
            4) user can re-generate questions easily and for cheap (cheap for me at least cost for user tbd) bc embeddings are precomputed
            5) user should delete things hopefully
        - other idea: instead of giving whole textbook to gemini to figure out ideas, just have the user input a syllabus / toc of
         textbook so we can get the names off the bat, or have an option to specify yourself, 
        or have it make its own based on the input material (this would be better for unorganized courses w/ no 
        syllabus and it would be easy for users - could make specifying yourself the default and have this for paid content?)
        - optimize sectioning (e: citations should not be ignored as opposed to taking up lots of sections possibly)
            not completely sure how to do this yet
            - DEFINETELY invoke parallel processing somehow
            - INCREASE pinecone batch insert as well
            - not sure how to handle max context window - if its that long anyway - probably either just take the first 500 words or split it up
            or something
            - run basic nlp to determine if it is a question of substance or just citations / index / whatever
                - for citations for example, you could cite them in the problem.

    actual map page:
        - decorate the map eventually
        - figure out a way to break up room names into sections either by user request or something else
        - explore play button displaying mastery of topics in the course as well (course name could be just the topics for now)

COMPLETED:
    ✅ get frontend to work
    ✅ get backend to work

    ✅ get title from library to knowledge (practice) page and make sure you ask ChatGPT for best way to do it (data() vs mounted() vs actions vs computed)
    ✅ create a course, but all it displays is the name on a card. when you click on the card (course), you are taken to the previous knowledge graph screen, and it just says the course name. Nothing too fancy just yet
    ✅ make every room_name in a library associated with a stepping stone possibly
    ✅ going off of ^^^ basically finding something to fill list of stepping stones in db
    ✅ change room names text to a good color
    ✅ add a small pop-up menu when you click on it that currently displays nothing but will display the course name possibly and the play button 
    ✅ link clicking on the "play" button link to the actual game
    ✅ USER HAS TO BE LOGGED IN TO GENERATE A LIBRARY
        - add both in frontend and backend
    ✅ change from giving questions from lots and lots of "rooms" to questions from one specific room
        - almost done, but need to make library room names have underscores instead so it will redirect and it will
    ✅ figure out how to make it so that it generates {inputed} number of rooms
    ✅ hide header / footer from game when user is playing a game
    ✅ remove timer, likes, clouds, and diamonds from game screen 
    ✅ add X button to exit out of game and navigate back to game / course map
    ✅ figured out why a room name of the name of the library kept generating and fixed it
    ✅ remove description and game image popup upon initial game page load
    ✅ page / route reorganization

    rag stuff:
    1) give whole textbook to gpt to "split up" ✅
    2) store embeddings in pinecone (every paragraph) ✅
        2.1) build a small ai rag chatbot to test out that everything I did so far works (it does) ✅
    3) generate questions per every subchapter / lecture given syllabus (stored in database) ✅
        3.1) integrate rag stuff with backend ✅
        3.3) enable modification of rooms based on user input of rooms ✅
        3.4) add rag retrieval to rooms ✅

RESOURCES:
    - node components: https://vueflow.dev/