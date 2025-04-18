# Gamefied-Study-Tool
Tool that allows users to input things like lecture recordings, lecture slides, professor notes, etc... and output Doulingo-like course based on those inputs.

IDEAS:

    ideas for grand plan / future:
        - create a community discord server (configure the current one)
        - create cheap vr cardboard cutouts of headsets where you can put your phone --> give to high schools possibly for free once you partner with them
            - have to think specifically of who / what to target for MVP, etc... so as little time as possibly gets wasted building something that either 1) is outside of my domain of expertise or 2) other people might build (repeat of unclear jupyterhub research)
            - not sure where to go from there, lots of places though
        - see google doc for more plansyour resume
            - Built a custom text extraction pipeline using Optical Character Recognition to extract text from pdf textbooks with 97% accuracy
                (add image to text ocr thing on resume)

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
        - about page (?)
        - somewhere to link to X / discord (might be on an existing page, idk) (see mvp cleanup list)
        (currently all 4 were in BottomBar.vue) --> (BASICALLY MAKE BottomBar.vue SMALLER)

    general:
        - add two buttons right next to each other and right above "play"
            1) video button where a manim video is generated about the subject possibly
            2) other resources button where other youtube videos / articles are researched in relation to the topic (grab the resources based on content, not necessarily the name of the section)
        - add ability to see uploaded files in library and maybe even file preview
        - add ability to add friends to a course + leaderboard as well
        - make a constants file for discord links, twitter / x links, any backend urls, etc...
        - add tips for making a new stepping stone (i.e. make sure it aligns with what you put, etc... )
        - for short answer, 1) make it one word (for now) and most importantly 2) make sure the exact word is in the other side of the card
        - fix Aryan's problem with viewing it on his phone
        - look into adding a resizable area somewhere in your site (like how turbo learn has it) but like people can't change it
        - add ability to delete library (have to enter its name exactly)
        - add check for duplicate room name for the time being - maybe allow it later down the line?
        - when you mouse over the popup for the lesson that has the # of lessons / x button, it should not cause the button to hover
        - improve ui with libraries / courses in library creation screen
        - add ability to change color of image of courses
        - remove lesson ids, lesson names, password reset tokens and confirmation tokens from urls and communicate them somewhere else
            - make it like duolingo where doing the actual lesson is /learn or something
        - add page after you finish a game session, but make it have confetti or an animation or something
        - should email / pwd reset tokens be visible via the url or should they be more secret?
        - how long do email confirmation tokens last / how long do password reset tokens last / what do I do when they're done?
        - improve prompt / answer generation
        - fix propfind error thing
        - add google auth and / or PASSWORD RESET
        
        - add a slot for an image in each question for reference or description or something - like maybe an image of a bridge or trigonometry or something
        - migrate from pinecone-client to pinecone (not really a migration, just a typo I think, shouldn't take too long)
        - possibly fix weird ssl module warning thing when I run the backend
        - reduce bundle (currently @ 261 KiB, want to be ideally below 244)
        - add support for multiple file upload (possibly)
        - add other routes back in, eventually
        - remove library difficulty, mentor, language, etc... from db course structure, backend, frontend course creation screen
            - note: easy to get rid of in the frontend, but have to remove lots of stuff in backend w/ various function calls and stuff
        - include question prompt generation (e.g. make the answer choices very similar to what you think the user would think so the questions are a little more challenging, etc...)
        - add default background if you scroll to far (like in main page if you scroll too far down)
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

        - all the other routes and stuff (terms & policies, buying subscription)

    create course (library) page:
        - add support for links / pdfs / other things and get rid of things like difficulty, tutor, etc... then actually start generating stuff to study
        - after user submits something and is waiting, display a loading bar or wheel or something letting the user know that it is generating


    potential work for rod / calvin / caleb:
        - let units / sections / courses have spacings / duplicate values as others in db / weird characters / numbers, #($^@{"?}*), etc...
        - change from rag --> kag
            - very nlp involved + graph stuff, etc...

    game page:
        - break up error checking in frontend for unit creation
        - implement game "score" logic (if you get >80% #attemps:number of questions ratio) then you get more / less points or something, etc...
        - investigate into what clouds and diamonds in game screen were used for so I can probably use them later
        - remove time from db then remove all references to "timer", "end time" or "starting time" in gameStore.js
        - add possibly a hint button as well (3 hints per question?)
        - instead of having to flip the factoid card, just put the main contents on the question card possibly? and ask them to use their applied knowledge, or give it to them as hints or something
        - instead of multiple choice, have it where users can drag / drop for an answer slot:
            (deepseek recomendations):
            - Add haptic feedback on drop (vibration for correct/wrong).
        - once I add a second type of "game", make it "shuffle" the questions once it gets the
            8 or so least seen so that the questions seem random and they aren't just the same multiple choice every time
        - make the underscores ___ visible in the questions

        - "games":
            - compare and contrast two items / scenarios (list of items / cards and sort them into categories)
            - ***analogies (would be easy to implement): newton is to physics as darwin is to ___ <-- would be super similar to already existing ones
            - ranking tasks: users rank tasks on order of importance, size, or chronology
            - timeline creation - drag and drop events <-- maybe would be good after we get a couple others down
            - category sorting (sort these into mammals, birds, and reptiles) - could be for easier questions
                like sort the statements into whether they are true / false, etc...
            - true / false <-- rlly good
            - matching pairs possibly, not sure how that would work with longer questions
            - could vary option amount (2-7 options)
            - users could have to select multiple options (select 1-5 out of 6-8, etc...)
            
            - multiple options in a row: like with duolingo where you are given 10 or so options and you pick 4 or 5 and they have to be 
                in a specific order. this might be somewhat tricky to implement cus I have to implement drag-and-drop at the same time, so I might have to 
                think of a couple others in the mean time
            - play duolingo / kinnu for inspiration
            - (easy**) correct the statement / choose the correct portion of a paragrah / two students have different opinions make them choose the correct one
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
    ✅ make it so you have to be confirmed to access pages
    ✅ add ability to add multiple room names from Add New Stepping Stone part
    ✅ ADD SHAD-CN
    ✅ eventually add footer back (note: requires light mode, discord link, everything in contact page, terms page, copyright(?), and possibly twitter link if we decide to do that)




RESOURCES:
    - node components: https://vueflow.dev/
    - how to use openai functions: https://platform.openai.com/docs/guides/function-calling?example=get-weather
    - my google doc: https://docs.google.com/document/d/1MvOFHL8wQBdvFlOhxfWZcTMGbxHWUpuhCqqbmpGXRUA/edit?tab=t.oc5pfrbekfi2