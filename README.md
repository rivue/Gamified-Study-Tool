# Gamefied-Study-Tool
Tool that allows users to input things like lecture recordings, lecture slides, professor notes, etc... and output Doulingo-like course based on those inputs.


Note: use npm audit --only=prod for this, 0 vulnerabilities = good

IDEAS:

    cleanup / maintenence (files to break apart):
        - remove library difficulty, mentor, language, etc... from db course structure, backend, frontend course creation screen
        - note: easy to get rid of in the frontend, but have to remove lots of stuff in backend w/ various function calls and stuff
        - get rid of other stuff I'm not using / don't plan on using like stuff in User model with ai tutor, etc...
        - break up different files to make them smaller and more modular:
        - library_routes
        - library_handlers
            - break into library level and section / unit level
            - or other things like settings or something because this file is 1k lines long
        - Learning Path 
            - specifically settings and add node buttons
        - etc... (keep working on this list)
        - Blueprints maybe

    ideas for grand plan / future:
        - Brain-Computer Interface (BCI) Integrations
            For researchers with EEG headsets: detect attention lapses or cognitive overload and adapt content pacing in real time.

        - Wearable Haptic Feedback
            Study flashcards on your smartwatch; correct answers give a gentle vibration “ping,” wrong ones a soft double-tap—learn on the go without looking at a screen.

        - Voice-First Study Mode
            Hands-free “audio textbooks”: speak your answers, get immediate verbal feedback, and use simple voice commands (“Next question,” “Explain that again”).
        - Mentor Matching Engine
            Based on your goals, invite advanced peers or volunteer mentors (e.g. alumni, grad students) for scheduled office-hour chats—AI helps coordinate agendas and follow-ups.
        - Automated Mind-Map Composer
            Feed in your scattered notes or highlights; the AI weaves them into a dynamic mind-map with draggable nodes, auto-grouped by theme, and “chain reactions” that show how mastering one idea unlocks another.
        - Embedded “Anywhere” Widgets
            -Drop a small embed on any website (Wikipedia article, corporate wiki, Slack channel) that launches a context-aware mini-lesson or flashcard deck tied to that page’s topic.
        -Plugin Marketplace & Open SDK
            Let third-party devs create specialized modules—math equation solvers, language pronunciation bots, domain-specific mini-games—and distribute them through an “App Store” for your platform.
            -Enterprise & University LMS Connectors
            One-click import of campus syllabi, grade-book sync, auto-provisioned cohorts based on student enrollment lists.
        - create a community discord server (configure the current one)

        - create cheap vr cardboard cutouts of headsets where you can put your phone --> give to high schools possibly for free once you partner with them and possibly include neural monitoring hard ware so we can take in their brain data and do something with it

           - AR Annotations & Pop-Ups
                Point your phone at a page of a textbook (or whiteboard) and see AI-generated overlays—diagrams that float in 3D, step-by-step solution hints, pronunciation guides for foreign-language vocab, and interactive “hotspots” you can tap for mini-quizzes
            - Virtual Lab Simulations
                launch fully simulated physics, chemistry, or biology experiments in the browser or VR headset. Mix chemicals, wire circuits, dissect virtual frogs—all with real-time AI guidance and safety feedback.
            - have to think specifically of who / what to target for MVP, etc... so as little time as possible gets wasted building something that either 1) is outside of my domain of expertise or 2) other people might build (repeat of unclear jupyterhub research)
            - not sure where to go from there, lots of places though
        - see google doc for more plans for resume (or just repomix this whole codebase into gpt / grok / gemini / claude, etc..)
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

    LAUNCH LIST: goal: July 6th then start working on social media posts


        last / harder:
        - ⭐️ obfuscate / minimize prod code
        - ⭐️ for LibraryCreator, outline the rules clearly somewhere, like in an i-card next to "create a course to explore" 
        or just put in text "rules for creating courses" or something
            - also, make room / course / unit / section consistent in frontend
        - ⭐️ vvvmaybe ask for feedback before doing vvv
            - also make sure it works well(ish) for mobile
        - ⭐️ add google auth
        - ⭐️ Terms of use / Policy Page legal agreement thing - ask gpt if I actually need, maybe ask jake how to do but maybe not
            - ⭐️ There are probably websites and stuff for this --> do this before Stripe
        - ⭐️ Stripe implementation
            - have to think abt what different payment levels mean / how I want to do it
        - ⭐️ ⭐️ ⭐️ (might take at least a couple weeks) UI redesign / rehaul *** --> kinnu, duolingo, saved instagram design reels etc...) --> ask nc state entreprenuership ppl for tips while i'm designing
            - Note: 1) try to see what horizontal --> vertical learning path looks like, and possibly make a vertical bar on the side for settings, i-card, files list, adding a new stepping stone, etc... but maybe keep lesson name and current unit name at the top?
            - COPY QUIZLET???
            - change popups --> toast, possibly with bar that displays when it will leave
            - note: maybe change top navbar to be a constant hovering side menu on the side / bottom of the screen maybe similar to duolingo and possibly replace "my library", "settings", etc.. with actual icons
                - maybe move name of library to top left corner, then add a box for the actual map, with buttons / settings / leaderboard outside of the bo
                    box or on the bottom / lining the right / left edge or something
                - potential new menu: "my libraries" "browse libraries" (would link from search?) "notifications" (like error messages or who joined a library or something), create / + (or maybe it would be a tab at the top next to search)
                - menu for library would have members list, settings for course owner, potentially a list of files to see, potentially a screen to see library statistics like # likes, # people, etc... 
                -  settings button would enable course owners to remove people, change visibility settings I think? or check different boxes for question types, or see users or something
                - users could add a note for each unit / library or something
                - instead of making path a long rectangle shape, make it follow the curve of the nodes
                - ⭐️ explore adding "scroll to current" on map page (last unlocked node)
                - also, maybe change it to vertical
                - ⭐️ add ability to leave libraries (later)
                - ⭐️ move dropdown menu to left + make dropdown menu permanant, replace w/ profile picture --> hover menu for to see profile settings or something
                - for course creation, make a "advanced settings" toggle for t/f, mcq, other questions, max users, etc... maybe other stuff as well
                - ⭐️ all the other routes and stuff (terms & policies, buying subscription, can't think of others?)
                - ⭐️ add i-card for all users, maybe description about the library along with a preview of the files used in the library and maybe also users who are members of the library or something 
                    - make description visible right below library card I think, maybe i card has more detail information, maybe when it was created or current owner or something
                    - also displays number of members of the library
                    - should I replace the proposed "i-card" with some icon that links to library details like discord has with their profile page where I would put files, members, and everything else in the menu, or should I keep it as is?
                    - (maybe?) ⭐️ add ability to see uploaded files in library (list of their names) and maybe even file preview (would require nosql db or something maybe)
                        - should I limit file size for this? like can only display files < 50 MB or something?

            - add ui ability to "join" private libraries / public libraries that you didn't create maybe in like a seperate page or list or maybe I could add a box for putting in library codes or something
            - ⭐️ after user submits something and is waiting, display a loading bar or wheel or different rotating facts (maybe relevant to the library?) letting the user know that it is generating
            - also note: ask gemini / grok / gpt / claude for some ui design tips like adding a menu bar, or ui tips / tricks / helpful websites / youtube videos, etc...
            use this maybe: https://www.shadcn-vue.com/docs/components/stepper.html
            - note: for main page, add two / 3 simple boxes, class you want, school, and possibly professor, and it gives you classes close to you like quizlet / rate my professor along with option for creating your own
                maybe it shows private ones with a "lock" icon and prompts you to enter a password. this way it would be like more of a network, which would differentiate us from a copy paste ai study tool (turbolearn) / NotebookLM
        
        glitches / 
            - why do different pages flicker on the screen when I am on a page and I hit refresh?
            - why is public generating a code on library creation? 
            - current streak in lesson complete displays current streak not current streak + 1 (maybe just refetch it?)
            - improve question generation eventually, like make all answers similar length, use similar answer choices, utilize SAT / ACT / MCAT style questions, maybe tailor the answer style for each course, like MCAT = premed, SAT / ACT = SAT / ACT prep, college style = college final exam style / quiz, etc...
            - when creating library for first time, maybe move join_library call to right below or IN save_library_room_states so theres no duplicate call to add users to library room states - might have to move db.session.commit logic though
            - on user login, make sure streak resets if last streak is more then a day ago or something like that
            - why does the "add unit" button extend the course length a little bit --> it shouldn't for now
            - play popup menu currently displays below unit name --> it should not be that way
            - make a back button in leaderboard that goes back to the library.

        hard probably (goal: 2 high level bullet points / wk):
        - ⭐️ remove alert message in library creator (not hard but have to remember)
        - ⭐️ add username (backfill username w/ 1st part of email before @ symbol - maybe let people change later)
            - for this section, make sure you modify explore page owner_id and library leaderboard
            - also, add a "back" button to library even if its literally a router.push call
        - ✅ ⭐️ Finish sections + units
            - ⭐️ Add ability to add sections to specific units (later --> come back to, reminder to make it account for 1-n number of sections no matter how that looks. add new stepping stones button is commented out for now)
            - When a user adds a section, make sure its added for all users, like add it to section_user_state and stuff
            - Make sure to account for duplicate section names, and make sure section names can have under scores, /&}}#@<, etc... and check for duplicate names for that unit or something
            - come_back_to
            - why is this empty? --> rag_context:
            - enable db.rollback for section generation
            - make sure to add a way to add sections in a library not just on empty units
                - make sure current section_id and unit_id is communicated to section generation call
            - make sure + section buttons are styled the same for middle ones and ones on the end
            - make sure either positions are correctly accounted for or we drop the ability to add multiple sections
            - when you come back do positions and ^^^ above
        - ✅ ⭐️ (would like to implement visibility of different courses first or at least a many:one for non-owners in library model)
            - ⭐️ Delete sections requires entering the name of the unit / course just for accidental reasons)
            - ⭐️ Delete Units (requires entering the name of the unit / course just for accidental reasons)
            - ⭐️ Delete courses / libraries (whatever they're called) (requires entering the name of the unit / course just for accidental reasons)
               - ⭐️ Remember to delete from both DB and pinecone as well, as well as respective child / parent courses / units / sections / libraries, roomNameState, LibraryFavorites, question, question_choice, LibraryMembership, etc...
        - ⭐️ (NOTE: do AFTER deleting sections / units / courses and adding sections) ability to leave a library
            - in explore courses page, add a "leave library" next to the "go to Course" button when a user joins the course

        medium (chip away at when tired / mentally exhausted from hard ones):
        - ⭐️ add staging / pre-production environment that isn't localhost
            - also figure out if 1) what I do to migrate the database is safe (swapping uri string and running flask db ugprade) and 2) how I should do it if it is not ideal
        
        easy (same as medium):
        - ⭐️ eventually fix Aryan's problem with viewing it on his phone - some samsung variation?

    OTHER PAGES:
        - terms and policies page
        - about page (?)
        - somewhere to link to X / discord (might be on an existing page, idk) (see mvp cleanup list)
        (currently all 4 were in BottomBar.vue) --> (BASICALLY MAKE BottomBar.vue SMALLER)

    general:
    study tool additions / ideas:
        - instead of having one opanai function, have a parent function which rolls how many and what type of game will be rolled ('true_false': 4, 'multiple_choice': 6, 'image': 2, etc... and then a suite of small agents which are each responsible for one (1) type of game (ex: true_false agent, multiple choice agent, image agent (might have to break up further maybe idk), etc..)) --> do all this so I can put "suite of agents" on my resume
        - is there a tool to like visualize all the different calls / paths something takes in a given api call or function call or something?
            - (important distinction: NOT debugging)
        - research into ibm granite / aws bedrock, or other alternatives to AI rag / kag for accuracy or something
        - when errors popup, prompt the user subtly with a contact form and discord (tell them we're constantly on Discord and check the contact form every hour or something)

        - voice mode based on textbook w/ knowledge bars of things you've covered so far and possibly quick lessons to make sure you know your stuff (insipired by gpt voice mode)
        - trending courses tab?
        - ⭐️ add leaderboard / game point tracking system (could be reworked later)once user base grows a bit (on every course, do all time and monthly)
            - ⭐️ implement some game "score" logic (if you get >80% #attemps:number of questions ratio) then you get more / less points or something, etc...
            - would need num_points for each user in a library - maybe in library membership data structure?
        - ⭐️ ask for feedback / look at how people are joining public / private libraries / give users a school variable / track users joining libraries across different timezones to see if I should add descripitions or not
        - ⭐️ for various buttons / other things, when you hover over them, make them display what they do / their names (edit button, toggles edit mode, etc...)
        - ⭐️ replace chevron / double chevron with arrows (copy openai / grok / claude, etc...)
        - ⭐️ add some other types of games / questions (ex: true / false, very detailed / specific questions, sorting, compare / contrast, analogies, image based stuff (not sure how to implement) 6 options choose 1-6, etc... see list below)
        - ⭐️ In creating a new library, add checkboxes for different types of modes (fill-in-the-blank, t/f, mcq, etc…)
            - maybe add it in settings for owner as well (enable / disable for future lesson content generation)
        - integrate with teacher / school list from rate my professors 
            - would probably be pretty easy: https://classic.yarnpkg.com/en/package/ratemyprofessor-api
            - https://github.com/tisuela/ratemyprof-api
        - ability to verify by school email which helps with filtering results? 
        - (later) add support for links / pdfs / other things and get rid of things like difficulty, tutor, etc... then actually start generating stuff to study
        - (later) add support for multiple file upload as well
        - add logic for multiple flame emojis w/ streaks of 1, 5, 10, 25, 50, 100
            - or make it adopt to a curve like exponential games or like xp in skyblock something more broken like --> (1, 3, 6, 8, 18, 36, 42, 69, 120, 210, etc...)
                - but offer rewards at even perks (5, 10, 15, 25, 50) to make it even more enticing?
            - could be for a smaller one: https://lottiefiles.com/free-animation/fire-flame-4De5RVVPag
            - slightly bigger one: https://lottiefiles.com/free-animation/fire-IuJfcIXKF1
            - maybe for 50 or 100, this whisks accross the little hover menu?: https://lottiefiles.com/free-animation/dancing-fire-CtzldMIEf9
            - maybe for smaller one like 5-10: https://lottiefiles.com/free-animation/fire-TLLDXwQuCQ
            - do this a little later
        - small idea for later (maybe): when you mouse over the unit name in learning path, it hovers a little bit, highlights white or --text-color, and displays above any names it is over
        - massive reorg / cleaning - get rid of unused functions / db models, commands / db calls / api calls / frontend components and rearrange existing ones using files structures / Blueprints that make sense
        - big idea: for multiplayer, make a way for people to join a "call" like discord, but with like a host maybe, so they have mini-games just like jack in the box where you have a host judge, or maybe the other players or ai judges the players responses. the games would be very high in retrieval so players really burn in the studying, like playeres could be given a prompt from something from their studying or notes or courses like "photosynthesis" and the user would have to construct a concept map using bubbles and lines and would name them accordingly to see how deeply they can remember a topic, then everyone would rate and compare responses. the level deeper then that would be if people would describe each bubble word in a sentance / essay form, obviously there could be more retrieval based games but this is just a start
        - big idea #2 (slightly smaller): add an ability for users to click a button and the website / app generates / can print out a "study guide" for tests and stuff, and the user can choose what size it is, like 2 page front and back, 1 page, 1 page 12"x18", 1 5"x3" index card, etc...
        - Front page: 1-2 boxes, "what are you here to study" then a text input box that slides through different classes, maybe filter by location and have a second optional box for professor name and third for school name. Displays a list or libraries along with a butt9n thay says "create"

        -User retention: streak and cram mode
        Complete a lesson daily to keep stream. 24 hrs after u complete a lesson, the next one unlocks. Maybe some external reward like irl merch or snth
        Cram node is basically creative mode, can't do rewards but can skip around to any lesson
        -Possible idea: adding the ability to schedule group study sessions within each library, maybe a ventral calendar for all the meetings, and maybe add the ability to pull things from canvas and moodle?
        Good- idk
        Bad- location in an app might be dangerous especially for public libraries, not an original feature, might get people off the app?
        - ⭐️ cram mode or something at the bottom - basically goes through review mode, but of all of them, effectively giving them the review, but without the need to break their streak
        - ability for user to change language
        - add toggle for users to set a home 'timezone' (dropdown menu) and add for it to automatically 
            switch
        - look into flask Blueprints
        - ⭐️ Syllabus to section / unit converter / parser thing
        - look in to using vueFlow for the nodes --> maybe one day I make it super interactive and colorful with people dragging and creating ornate graphs for their friends or something, or maybe not
        - when users first sign up, give them a medium / long survey to make them think long and hard about their study habits / why they want to get high grades, then when they hit the paywall, they are more likely to join
                - free users get like 10 free uploads / month, and can only join libraries up to like 5 sections or up to 5 libraries or something
                - first paid tier get unlimited uploads / month, but only have like 2 large textbooks uploaded / month
                - second paid tier get 10 textbook uploads / month maybe
        - have a notifications / dashboard page - errors for generating libraries / units / sections (like for content moderation errors, etc...) and notifications about someone liked your course or someone joined your course or something, etc... (maybe maybe not on this one - I just want a place to tell users without them having to wait 30 minutes for their course to load)
        - use the ai to generate a course
            - tell it to generate reasonable courses that are like 2-3 times a week or every day or something.
            - below the section name, it could tell what resources it used to create the course in smaller / gray text
        - Skill Trees & Talent Builds
            Visualize your mastery like a character in an RPG—choose to specialize (“speed-reader” vs. “deep-diver”) and unlock branching benefits (fast flash-review vs. deeper case studies).
        - Hypothesis Playground
            Sketch out your own mini-experiments or thought experiments, and the AI simulates outcomes (e.g. “What if temperature doubles in reaction X?”), giving you rapid feedback on plausibility.
        - Total Accessibility Suite
            Real-time audio narration, sign-language avatar translations, dyslexia-friendly fonts, high-contrast themes, and language-learner mode with instant look-up pop-ups.
        - Mindfulness & Mental Fitness
            Short, AI-led breathing exercises or “cognitive resets” before tough modules to reduce anxiety and boost retention.
        - Sentiment & Engagement Signals
            Analyze discussion-board posts, free-form answers and chat logs to surface concepts that trigger frustration, confusion, or boredom—and then automatically generate supportive hint-videos or alternative explanations.
        - “Predict & Prescribe” Engine
            Using aggregated, anonymized data, forecast which upcoming topics will trip up learners like you—and auto-prepare targeted readiness modules (“heads-up: many students struggle with substitution integrals next week!”).
        - Real-Time Study “Rooms”
            Join or host live co-study sessions: everyone works on the same module side-by-side, can chat or voice-call, swap spontaneous quizzes, and “ping” each other for help.

        - Peer-Graded Projects & Code Review
            For subjects like programming or writing, submit a project, get assigned 2–3 peers to review and grade, then earn badges for quality feedback.

        - Challenge Tournaments & Hackathons
            Weekly themed challenges (e.g. “Graph Theory Weekend”) where students compete individually or in teams to solve increasingly tough problems—complete with real-time leaderboards and “tournament brackets.”
        - Dynamic Difficulty Tuning
            As soon as the AI detects you’re breezing through one concept, it injects a harder “speed-run” sub-quiz or a real-world problem to keep you challenged. If you falter, it auto-spawns bite-sized remediation (“micro-lessons”) until mastery.
        - tailor the prompt / library to that specific class (ex: thermodynamics = engineering style problems, chemist = real life examples, etc...)
        - add a knowledge graph / knowledge map as one of the option on the vertical left side bar thing
        - shared milestones as opposed to just single user milestones / leaderboards
        - ability for voice enabled options for narration / settings and stuff
        - study groups / peer quizzes - not sure how to approach this one
        - ideas for multi-modal content: draggable vectors for physics, audio summaries / transcrips for learning on the go
        - button at the bottom of the page for daily review and maybe another one for review most missed questions (here is where we implement spaced repitition scheduling)
        - generate a lot of different questions and if a student gets a lot of the correct, move on to the next one or like skip ones that the student finds easy or something
        - ⭐️ ⭐️ do a quiz or something at the end of a user completing a stepping stone for the first time (all 3 or whatever lessons, not just one)
                reinforce the quiz with questions from tests from that school's test bank, and could get users to take pictures of their tests or something to popularize test banks in general
        - remove azure thing
        - ability to rename libraries
        - give estimations based on file input size (ex: 500kb --> 10 minutes, etc... make them highly conservative,)
            - we could also section it off, like load part of it at a time, or load it in the background 
                while the user it playing an already unlocked game or something
        - make a better loading screen / bar / wheel while the courses are being created
            - make it like not able to navigate away or something idk
            - maybe even tell users not to navigate away from the page or something
            - for improving textbook loading, maybe make textbook take a long time, but load users with similar sections / libraries while it still loads - like just direct them to actual section games of public libraries while they wait, or do a survey or something while they wait like who it is for or something
        - improve prompt generation a great fold (make sure as many of the quesitons relate to the section name as possible)
        - eventually combine library_question model with library_factoid model (why are they seperate to begin with?)
        - get student verification on Mobbin pro (UI library)
        - add ability to reset password for users who are logged in
        - change the name of all functions in library_handlers to use get, update, create, delete only
        - maybe ask users how knowledgeable they are with a unit / course / section before they start?
            not sure how many extra questions I would need to generate for this to work though...
        - clean up unneeded db model variables from db
        - there could be a button on the game screen that says “review most missed questions” or some equivalent
        - there could also be “boss missions” mixed in either at the end of units or mixed in randomly with more difficult questions or cumulative review or something
        other thing:
        - possibly change outline of course, like maybe make it wrap around to the right, then do a u-turn and wrap around to the left, with the user scrolling up / down
        ...instead of left / right
        - fix the fact that refresh is triggering /api/<whatever> three different times
        - add two buttons right next to each other and right above "play"
            1) video button where a manim video is generated about the subject possibly
            2) other resources button where other youtube videos / articles are researched in relation to the topic (grab the resources based on content, not necessarily the name of the section)

        - make a constants file for discord links, twitter / x links, any backend urls, etc...
            - make it available for both frontend and backend like for api routes
            - max_number of libraries
            - image links, like fireicon, discord logo, etc... ="../../assets/images/fireicon.png
        - for short answer, 1) make it one word (for now) and most importantly 2) make sure the exact word is in the other side of the card
        - look into adding a resizable area somewhere in your site (like how turbo learn has it) but like people can't change it
        - ??? remove lesson ids, lesson names, password reset tokens and confirmation tokens from urls and communicate them somewhere else
            - make it like duolingo where doing the actual lesson is /learn or something
        - should email / pwd reset tokens be visible via the url or should they be more secret?
        - how long do email confirmation tokens last / how long do password reset tokens last / what do I do when they're done?
        - improve prompt / answer generation
        - fix propfind error thing
        - (maybe later to make sure it works) add a slot for an image in each question for reference or description or something - like maybe an image of a bridge or trigonometry or something
        - migrate from pinecone-client to pinecone (not really a migration, just a typo I think, shouldn't take too long)
        - possibly fix weird ssl module warning thing when I run the backend
        - reduce bundle (currently @ 261 KiB, want to be ideally below 244)
        - add other routes back in, eventually
        - include question prompt generation (e.g. make the answer choices very similar to what you think the user would think so the questions are a little more challenging, etc...)
        - change theme / color / name
        - make footer even smaller and look better
        - contact image on main sidebar?
        - add about route back in (could be something about how I want to help students study, or I could just not add it back in)
        - change gpt 4o-mini to deepseek (deepseek once I test reliable function calling or parsing) or other model for cost
        - eventually look into custom api / llm specifically designed for education or review or whatever
        - *possibly* add a slider to each course based on how lenient the course creator wants the fuzzy string matcher to be (for misspelled words)
        - only fetch most 30 recent factoids, or summary of factoids or something when doing room generation

    game page:
        - break up error checking in frontend for unit creation
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

RESOURCES:
    - node components: https://vueflow.dev/
    - how to use openai functions: https://platform.openai.com/docs/guides/function-calling?example=get-weather
    - my google doc: https://docs.google.com/document/d/1MvOFHL8wQBdvFlOhxfWZcTMGbxHWUpuhCqqbmpGXRUA/edit?tab=t.oc5pfrbekfi2