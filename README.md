# Gamefied-Study-Tool
Tool that allows users to input things like lecture recordings, lecture slides, professor notes, etc... and output Doulingo-like course based on those inputs.

IDEAS:

    ideas for grand plan / future:
        - create a community discord server (configure the current one)
        - create cheap vr cardboard cutouts of headsets where you can put your phone --> give to high schools possibly for free once you partner with them
            - have to think specifically of who / what to target for MVP, etc... so as little time as possibly gets wasted building something that either 1) is outside of my domain of expertise or 2) other people might build (repeat of unclear jupyterhub research)
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
        - possibly take inspiration from btd5 or btd6 / odessey

TODO list:

    MVP CLEANUP LIST:
        - add OTHER PAGES

    OTHER PAGES:
        - terms and policies page
        - somewhere to link to X / discord (might be on an existing page, idk) (see mvp cleanup list)
        - about page
        (currently all 4 were in BottomBar.vue) --> (BASICALLY MAKE BottomBar.vue SMALLER)

    general:
        - implement some sort of const file with routes (ex: PASSWORD_RESET_URL = "...", etc...)
        - improve prompt / answer generation
        - fix propfind error thing
        - add google auth and / or PASSWORD RESET
        - add ability to add multiple room names from Add New Stepping Stone part
        - add a slot for an image in each question for reference or description or something - like maybe an image of a bridge or trigonometry or something
        - migrate from pinecone-client to pinecone (not really a migration, just a typo I think, shouldn't take too long)
        - possibly fix weird ssl module warning thing when I run the backend
        - reduce bundle (currently @ 261 KiB, want to be ideally below 244)
        - ACCOUNT FOR MOBILE SCREEN SIZES!!
        - ADD SHAD-CN
        - add support for multiple file upload (possibly)
        - add other routes back in, eventually
        - remove library difficulty, mentor, language, etc... from db course structure, backend, frontend course creation screen
            - note: easy to get rid of in the frontend, but have to remove lots of stuff in backend w/ various function calls and stuff
        - include question prompt generation (e.g. make the answer choices very similar to what you think the user would think, etc...)
        - add default background if you scroll to far (like in main page if you scroll too far down)
        - eventually add footer back (note: requires light mode, discord link, donate link (or we could just not do that), everything in contact page, terms page, copyright(?), and possibly twitter link if we decide to do that)
        - change theme / color / name
        - ability to "star" / "favorite" a course
        - make footer smaller and look better
        - contact image on main sidebar?
        - add about route back in (could be something about how I want to help students study, or I could just not add it back in)
        - significant ui rehaul *** --> kinnu, duolingo, saved instagram design reels etc..
            - copy openais font?
        
        - change gpt 4o-mini to deepseek (deepseek once I test reliable function calling or parsing) or other model for cost
        - eventually look into custom api / llm specifically designed for education or review or whatever
        - *possibly* add a slider to each course based on how lenient the course creator wants the fuzzy string matcher to be (for misspelled words)
        - improve completion screen a bit
        - add support for .txt files for the create library thing
        - clean up minor ui thing with learning nodes (when you click on the popup to play the games, for some reason it still highlights the node)
        - modify section splitting logic (5 sentences --> 1k characters or 200 words max or whatever.)
        - only fetch most 30 recent factoids, or summary of factoids or something when doing room generation
        - one word short answer (make gpt come up with variations so people aren't pissed off w/ super close answers, ex:
        NCSU, ncsu, NC State, North Carolina State University, etc... or maybe use basic nlp to check?)
        - all the other routes and stuff (contact / submit feedback, terms & policies, buying subscription, settings)

    create course (library) page:
        - add support for links / pdfs / other things and get rid of things like difficulty, tutor, etc... then actually start generating stuff to study
        - after user submits something and is waiting, display a loading bar or wheel or something letting the user know that it is generating

    game page:
        - implement game "score" logic (if you get >80% #attemps:number of questions ratio) then you get more / less points or something, etc..)
        - investigate into what clouds and diamonds in game screen were used for so I can probably use them later
        - remove time from db then remove all references to "timer", "end time" or "starting time" in gameStore.js
        - add possibly a hint button as well (3 hints per question?)
        - instead of having to flip the factoid card, just put the main contents on the question card possibly? and ask them to use their applied knowledge, or give it to them as hints or something
        - instead of multiple choice, have it where users can drag / drop for an answer slot:
            (deepseek recomendations):
            - Add haptic feedback on drop (vibration for correct/wrong).
            - Use gravity physics (e.g., answers "fall" into the slot with a bounce).
            - Animated rewards: Slot glows/explodes with confetti on correct answers.
        - once I add a second type of "game", make it "shuffle" the questions once it gets the
            8 or so least seen so that the questions seem random and they aren't just the same multiple choice every time
        - make the underscores ___ visible in the questions
        - "games":
            - compare and contrast two items / scenarios (list of items / cards and sort them into categories)
            - analogies: newton is to physics as darwin is to ___ <-- would be super similar to already existing ones
            - ranking tasks: users rank tasks on order of importance, size, or chronology
            - timeline creation - drag and drop events <-- maybe would be good after we get a couple others down
            - category sorting (sort these into mammals, birds, and reptiles) - could be for easier questions
                like sort the statements into whether they are true / false, etc...
            - true / false <-- rlly good
            - sentence completion <-- kind of similar to one word answer? maybe you type it in the sentence or something?
                maybe it can be more drag / drop later?
            - matching pairs possibly, not sure how that would work with longer questions
            - could vary option amount (2-7 options)
            - users could have to select multiple options (select 1-5 out of 5-8, etc...)
            
            - multiple options in a row: like with duolingo where you are given 10 or so options and you pick 4 or 5 and they have to be 
                in a specific order. this might be somewhat tricky to implement cus I have to implement drag-and-drop at the same time, so I might have to 
                think of a couple others in the mean time
            - play duolingo / kinnu for inspiration
            - correct the statement / choose the correct portion of a paragrah / two students have different opinions make them choose the correct one
            - time attack mode option - questions might be a little easier possibly or not
            - image based questions - not sure how that would work how how we would ensure accuracy
            - drag-and-drop labels (label the x axis, y axis, identify what the mean is, etc...)
            - hotspot questions (click on X in this diagram)
            - venn diagram sorting - sort these things into squares, circles, or both
            - fill in the table (a periodic table w/ missing elements)
            - debate mode: users choose a side in a debate and answer questions to support their argument
            - case studies: users analyze a real-world scenario and answer questions based on it
            - hypothesis testing: users propose a hypothesis and answer questions to test it
            - multi-step problem (would get to this later down the line)
            - predict the outcome
            - creative writing (this would be hard w/o llms - maybe could use rlly advanced nlp to detect it? or ask chatgpt to give it things to look for)
            - error detection (users identify and correct errors in a passage, equation, or diagram)
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
                - support links for more context possibly? (maybe it would be more of a room specific thing?)
                - fix weird website not working issue (I think it happens right after login)
                - remove image stuff for library and replace with plain color (user can choose color, maybe something out of 12 or something)
                - add times_seen variable in the library factoid database when a user "sees" the question so we can start giving the user the least seen 8 out of 20 questions each time or something
            4) user can re-generate questions easily and for cheap (cheap for me at least cost for user tbd) bc embeddings are precomputed
            5) user should delete things hopefully
        - other idea: instead of giving whole textbook to gemini to figure out ideas, just have the user input a syllabus / toc of
         textbook so we can get the names off the bat, or have an option to specify yourself,
            - search for GenerateLibraryRoomNames
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
    ✅ gray out the explore button until someone adds at least one room name
    ✅ switch "room names" to "lectures" in create library page
    ✅ add ability to create rooms / "lectures" once you create a library, and mention that in the "add rooms" page (ex: "*lectures can be added within the library*")
    ✅ fix the issue where anywhere on a card exits the lesson as opposed to just the red x
    ✅ maybe do something that caps length of vector embedding response, like chops off anything after 1k tokens / characters or something (limited response to 10 questions)
    
    rag stuff:
    1) give whole textbook to gpt to "split up" ✅
    2) store embeddings in pinecone (every paragraph) ✅
        2.1) build a small ai rag chatbot to test out that everything I did so far works (it does) ✅
    3) generate questions per every subchapter / lecture given syllabus (stored in database) ✅
        3.1) integrate rag stuff with backend ✅
        3.3) enable modification of rooms based on user input of rooms ✅
        3.4) add rag retrieval to rooms ✅

    MVP CLEANUP LIST:
    ✅ redirects / url stuff + 404 page (ex: 
            "/knowledge/:id/:anythingHereShouldRedirect"
            "/library/:id/:roomName/:anythingHereShouldRedirect"
            etc...
        )
    ✅ fix low / moderate / high vulnerabilities for npm packages in frontend (down to 8 from 26 so yay)
            - anything in dev dependencies are probably fine (vue-cli-... or vue/component...)
            TODO USE npm audit --only=prod for this, 0 vulnerabilities = good
    ✅ make sure "Knowledge Map", "Lessons", and other dashboard things either actually link somewhere or are handled properly
    ✅ loading bars / wheels possibly (at least look into) (for course creation and for other stuff as well)
        ✅ added loading component to every frontend route, no matter if valid or invalid, in case routes take too long to fetch,
        which covers cases where you have to fetch from api
    ✅ weird redirect for when user is logged in and try to navigate to a library which doesn't exist or no permissions (102 in main.js) ex: /lessons/234234
            fix w/ a loading state or something, prob pretty easy
    ✅ create email

    ✅ ideas for name:
        - name something stone related for the actual lessons (bc you are SOLIDIFYING your knowledge (hahahahahah ok im done))
        - rivue (ReInvent VirtUal Education --> go public w/ the acronym when I start the cardboard thing)
    ✅ implement "feedback" tab (note: requires email oath, and email domain and possibly twitter and stuff as well)
    ✅ change CORS(origins="*") to the actual frontend url in app.py
    ✅ add auto deploy for github ci/cd
    ✅ add light / dark mode switcher to settings (it already exists)
    ✅ ascendence --> rivue (everywhere on the site and in the file system)
            - pretty much done, and modify email_templates
    ✅ go through TODOs (again once emails are taken care of)
    ✅ figure out prod building and gcp and possibly nginx / rabbit / zeromq or whatever  
    ✅ error handling, and lots of it (how to handle failed document generation, other errors, etc...)
    ✅ error handling for not finding any context when loading stone names in library?
    ✅ put x / discord links in main page, probably along with something like "join us" or "hear our updates" or something
    ✅ continue with adding X / Discord link to main page (LibraryCreator.vue)


RESOURCES:
    - node components: https://vueflow.dev/
    - how to use openai functions: https://platform.openai.com/docs/guides/function-calling?example=get-weather
    - my google doc: https://docs.google.com/document/d/1MvOFHL8wQBdvFlOhxfWZcTMGbxHWUpuhCqqbmpGXRUA/edit?tab=t.oc5pfrbekfi2