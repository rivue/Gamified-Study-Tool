# library_routes.py

import random
from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin
from bleach import clean
from flask_executor import Executor
# from pdfminer.high_level import extract_text
import pytesseract
import pdf2image
import pytesseract
from PIL import Image
import pdfplumber
from PyPDF2 import PdfReader
import fitz
import re

import base64
from io import BytesIO
import time

from openapi import moderate
from utils import mask_email, get_client_ip
import database.library_handlers as lbh
import knowledge_net.library_generator as lgn
from images.library_imager import generate_images_task, save_image
from database.user_handler import increment_violations, is_within_limit, check_generation_allowed, mark_generation_done

def init_library_routes(app):

    executor = Executor(app)

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        # User checks
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            # ip = request.remote_addr
            ip = get_client_ip()
            # if not check_generation_allowed(ip, 'library'):
            #     return jsonify(status="error", message="Library generation limit reached."), 403

        # Topic checks
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400
        topic = clean(topic)
        if len(topic) > 200:
            return jsonify({"error": "Topic is too long. Maximum 200 characters allowed."}), 400
        if len(topic) < 1:
            return jsonify({"error": "No message."}), 400

        # Difficulty checks
        library_difficulty = request.json.get("libraryDifficulty")
        VALID_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not library_difficulty:
            library_difficulty = "Easy"
        else:
            library_difficulty = clean(library_difficulty)
            if library_difficulty not in VALID_DIFFICULTIES:
                library_difficulty = "Easy"

        # Guide checks
        guide = request.json.get("guide")
        VALID_GUIDES = ["Azalea", "Irona", "Bubbles", "Sterling"]
        if guide:
            guide = clean(guide)
        if not guide or guide not in VALID_GUIDES:
            guide = random.choice(VALID_GUIDES)

        # Language & language difficulty checks
        language = request.json.get("language")  # Add other supported languages
        if not language:
            language = "English"
        else:
            language = clean(language)

        language_difficulty = request.json.get("languageDifficulty")
        VALID_LANGUAGE_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not language_difficulty:
            language_difficulty = "Normal"
        else:
            language_difficulty = clean(language_difficulty)
            if language_difficulty not in VALID_LANGUAGE_DIFFICULTIES:
                language_difficulty = "Normal"
        # Extra context checks
        extra_context = request.json.get("extraContent")
        if extra_context:
            extra_context = clean(extra_context)
            if len(extra_context) > 200:
                return jsonify({"error": "Extra context is too long. Maximum 200 characters allowed."}), 400

        # Check for existing library
        # TODO VVV if not extra_context:
        #     existing_library = lbh.get_library_id(topic, library_difficulty, language, language_difficulty, guide)
        #     if existing_library:
        #         # Now check if first room exists
        #         existing_content = lbh.retrieve_library_room_contents(existing_library, topic)
        #         if existing_content:
        #             return jsonify(status="success", library_id=existing_library)
        #         else:
        #             try:
        #                 # Generate room content asynchronously
        #                 room_future = executor.submit(lgn.generate_libroom_content, user_id, topic, existing_library)
        #                 room_contents = room_future.result()
        #                 lbh.save_library_room_contents(existing_library, topic, room_contents)
        #                 return jsonify(status="success", library_id=existing_library)
        #             except Exception as e:
        #                 return jsonify(status="error", message=f"Failed to generate room content {e}"), 500

        if not user_id:
            mark_generation_done(ip, 'library')
        
        # Start moderation task
        # TODO vvv content_for_moderation = topic
        # if extra_context:
        #     content_for_moderation += extra_context
        # moderation_future = executor.submit(moderate, content_for_moderation)

        file_content = request.json.get("fileContent") # TODO moderation later
        if not file_content:
            return jsonify({"error": "No file provided"}), 400
        
        # 1) store embeddings in pinecone then get embeddings on a per room basis
        room_names = request.json.get("roomNames")
        if room_names:
            print(room_names)
        else:
            return jsonify({"error": f"Must specify room names for now, also we are in the process of breaking things"}), 400

        # Start library generation task (flask Gemini 1.5)
        # room_names_future = executor.submit(lgn.suggest_library_wing, user_id, topic, library_difficulty, language, language_difficulty, extra_context)

        # Start image generation task
        # img_url_future = executor.submit(generate_images_task, topic, library_difficulty, guide)
        
        # Generate first room content
        # room_future = executor.submit(lgn.generate_room_content, user_id, topic, library_difficulty, language, language_difficulty, extra_context, guide, file_content)

        # Wait for moderation result
        # TODO vvv violation, message = moderation_future.result()
        # if violation:
        #     if user_id:
        #         increment_violations(user_id)
        #     return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400

        # Create the library
        # room_names = room_names_future.result()
        # TODO library_response, status_code = lbh.create_library(user_id, topic, room_names, library_difficulty, language, language_difficulty, guide)
        # TODO add textbook / document embeddings to pinecone w/ library id fro library_response
        print("generate_library 1")
        
        # def extract_text_from_pdf(file_content):
            # try:
            #     # Handle data URL prefix if present
            #     if file_content.startswith('data:'):
            #         # Split header and data part
            #         parts = file_content.split(',', 1)
            #         header, data_part = parts[0], parts[1]
            #         # URL-decode the data part to handle percent-encoded characters
            #         data_part = unquote(data_part)
            #         file_content = data_part
                    
            #     # Remove any whitespace and newlines
            #     file_content = file_content.strip()
                
            #     # Add padding if needed
            #     padding_needed = len(file_content) % 4
            #     if padding_needed:
            #         file_content += '=' * (4 - padding_needed)
                
            #     # Validate ASCII-only characters
            #     try:
            #         file_content.encode('ascii')
            #     except UnicodeEncodeError as e:
            #         raise ValueError(f"Non-ASCII characters in base64 data: {str(e)}")
                
            #     try:
            #         # Decode base64
            #         pdf_bytes = base64.b64decode(file_content)
            #     except Exception as e:
            #         raise ValueError(f"Base64 decode failed: {str(e)}")
                
            #     # Create file stream and ensure it's properly positioned
            #     file_stream = io.BytesIO(pdf_bytes)
            #     file_stream.seek(0)  # Ensure we're at the start of the stream
                
            #     try:
            #         # Create PDF reader with strict=False to be more lenient with PDF format
            #         pdf_reader = PyPDF2.PdfReader(file_stream, strict=False)
                    
            #         # Extract text from all pages
            #         text_parts = []
            #         for page in pdf_reader.pages:
            #             try:
            #                 page_text = page.extract_text()
            #                 if page_text:
            #                     text_parts.append(page_text)
            #             except Exception as e:
            #                 print(f"Warning: Could not extract text from page: {str(e)}")
            #                 continue
                            
            #         # Join all text parts with newlines
            #         text = "\n\n".join(text_parts)
                    
            #         if not text.strip():
            #             raise ValueError("No text could be extracted from the PDF")
                        
            #         return text.strip()
                    
            #     except Exception as e:
            #         if "EOF marker not found" in str(e):
            #             # Try an alternative approach with a copy of the stream
            #             try:
            #                 file_stream = io.BytesIO(pdf_bytes)
            #                 pdf_reader = PyPDF2.PdfReader(file_stream)
            #                 text_parts = []
            #                 for page in pdf_reader.pages:
            #                     try:
            #                         text_parts.append(page.extract_text())
            #                     except:
            #                         continue
            #                 text = "\n\n".join(text_parts)
            #                 if text.strip():
            #                     return text.strip()
            #             except:
            #                 pass
                            
            #         raise ValueError(f"Could not process PDF: {str(e)}")
                    
            # except Exception as e:
            #     raise ValueError(f"Error processing PDF: {str(e)}")
            # pdf_bytes = base64.b64decode(file_content, validate=True)
            
           
            # Step 2: Convert bytes into a file-like object (BytesIO)
            # file_stream = BytesIO(pdf_bytes)
            
            # text = ""
            # with pdfplumber.open(file_stream) as pdf:
            #     for page in pdf.pages:
            #         text += page.extract_text() + "\n\n"
            # return text
            # fitz.open(stream=io.BytesIO(base64.b64decode(file_content, validate=True)), filetype="pdf")
            # all_text = ""
            # for page in fitz.pages():
            #     all_text += page.get_text("text")
            # return all_text

        # print("file content: " + file_content)
        
        def extract_text_from_scanned_pdf(file_content):
            # pages = convert_from_path(file_path)  # Convert each PDF page to an image
            # text = "\n\n".join([pytesseract.image_to_string(page) for page in pages])
            # return text
            try:
                # Step 1: Decode base64 string into bytes
                # print(file_content)
                # file_content = file_content.decode('utf-8') # or ascii?
                # file_content = file_content.decode('ascii')
                # handle event where file is bytes object?
                # encode object?
                file_content = file_content.strip()
                padding = 4 - (len(file_content) % 4)
                file_content += '=' * padding if padding != 4 else ''

                file_content_bytes = file_content.encode('utf-8')
                encoded_content = base64.b64encode(file_content_bytes) #, validate=True) # problem
                # encoded_content_str = encoded_content.decode('utf-8')
                decoded_content = base64.b64decode(encoded_content)

                pages = pdf2image.convert_from_bytes(decoded_content)
                total_text = ""

                # Process each page (image) with OCR
                for page in pages:
                    text = pytesseract.image_to_string(page)

                    # Print the OCR result for each page
                    if text:
                        print(text)
                    total_text += text

                # Write the extracted text to a file
                if total_text:
                    with open('./debug.txt', 'w', encoding='utf-8') as text_file:
                        text_file.write(total_text)
                else:
                    print("No text extracted from the PDF.")

                # print(encoded_content_str)
                # with open("./debug.pdf", "wb") as f: # good
                #     f.write(decoded_content)
                    # file_content_bytes = bad
                # with open('./debug.pdf', 'wb') as pdf_file:
                #     pdf_file.write(decoded_content)

                # with open('decoded_textbook.pdf', 'rb') as file:
                
                # Open and process the PDF
                # with BytesIO(decoded_content) as pdf_file:
                #     with pdfplumber.open(pdf_file) as pdf:
                #         for page_num, page in enumerate(pdf.pages):
                #             extracted_text = page.extract_text()  # Extract text from each page

                #             # Print out the extracted text for debugging
                #             if extracted_text:
                #                 print(f"Text from page {page_num + 1}:")
                #                 print(extracted_text)  # Print extracted text from each page
                #                 total_text += extracted_text  # Append the extracted text to the accumulator
                #             else:
                #                 print(f"No text extracted from page {page_num + 1}")  # Notify if no text is found

                # # After processing all pages, check if any text was accumulated
                # if total_text:
                #     # Print the entire extracted text (optional) for debugging
                #     print("Full extracted text from the PDF:")
                #     print(total_text)

                #     # Write the accumulated text to a file
                #     with open('./debug.txt', 'w', encoding='utf-8') as text_file:
                #         text_file.write(total_text)
                # else:
                #     print("No text was extracted from any page of the PDF.")
                
                # Step 2: Convert PDF pages into images
                # images = convert_from_bytes(pdf_bytes)
                # print(images)
                # print("^^^images")
                # Step 3: Extract text from images using OCR
                # extracted_text = "\n\n".join([pytesseract.image_to_string(img) for img in images])
                
                # extracted_text = extracted_text.encode("utf-8", "ignore").decode("utf-8")

                # extracted_text = unicodedata.normalize("NFKD", extracted_text)
                # extracted_text = extracted_text.encode("ascii", "ignore").decode("utf-8")
                # extracted_text = extracted_text.encode("ascii", "replace").decode("utf-8")

                return total_text
            except Exception as e:
                return f"Error extracting text: {str(e)}"

        def split_text_into_sections(text, min_sentences=5):
            sentences = re.split(r'(?<=[.!?])\s+', text)  # Split by punctuation
            sections = []
            temp_section = []

            for sentence in sentences:
                temp_section.append(sentence)
                if len(temp_section) >= min_sentences:
                    sections.append(" ".join(temp_section))
                    temp_section = []

            if temp_section:
                sections.append(" ".join(temp_section))  # Add leftover text

            return sections

        text = extract_text_from_scanned_pdf(file_content)  # Extract text from PDF
        print(text)
        # print(repr(text))
        # sections = split_text_into_sections(text)  # Chunk text into sections
        print("I did something")
        # print(sections[250])
        # print(sections[600])
        # print(sections[800])
        # print(sections[900])
        # print(len(sections[0]))
        # print(sections[0])
        # print(sections)
        return jsonify({"error": f"No error, we're in the process of breaking things for now😭😭😭"}), 400
        # 4️⃣ Embed & Store Sections in Pinecone
        # for section in sections:
            # pinecone_id = store_embedding(library_id, section)
        
        # if status_code == 201:
        library_id = library_response.get_json().get("library_id")
            # img_url = img_url_future.result()
            # print("saving image..")
            # save_image(library_id, img_url)
        # else:
            # raise Exception("Library creation failed")
        try:
            print("room future result")
            room_contents = room_future.result()
            print("room future result 2")
            lbh.save_library_room_contents(library_id, topic, room_contents)
            print("success")
            library = lbh.get_library(library_id, user_id, False)
            print("good")
            return jsonify(status="success", library_data=library.get_json())
        except Exception as e:
            return jsonify(status="error", message="Failed to generate room content"), 500


    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)

        if not library:
            return jsonify(status="error", message="Library not found"), 404

        # Check if the library has a default image and possibly trigger image generation
        response, status_code = lbh.has_default_image(library_id)
        if status_code != 200:
            return response

        # If there's a default image and the click count is divisible by 4, queue up image generation
        if response.json['has_default_image'] and library.get_json().get("clicks") % 4 == 0:
            executor.submit(generate_images_task, library_id)

        # Retrieve library data
        library_data = library.get_json()
        library_topic = library_data.get("library_topic")

        # Attempt to retrieve existing room contents
        room_data = lbh.retrieve_library_room_contents(library_id, library_topic)
        if not room_data:
            try:
                # If no content exists, generate the room content
                room_contents = lgn.generate_libroom_content(
                    user_id,
                    library_topic,
                    library_id
                )
                lbh.save_library_room_contents(library_id, library_topic, room_contents)
                room_data = room_contents
            except Exception as e:
                return jsonify(status="error", message="Failed to generate room content"), 500

        return jsonify(status="success", data=library_data, room_data=room_data)
        
    @app.route("/api/library/room", methods=["POST"])
    def generate_room():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")

        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        print("subtopic: " + subtopic)
        # Attempt to retrieve existing room contents
        existing_content = lbh.retrieve_library_room_contents(library_id, subtopic.replace("-", " "))
        if existing_content:
            return jsonify(status="success", data=existing_content)
        
        # If no content exists, generate new content
        if not user_id:
            ip = request.remote_addr # TODO ip stuff?
            # if not check_generation_allowed(ip, 'room'):
            #     return jsonify(status="error", message="Room generation limit reached."), 403
            
        print(f"userid: ${user_id}")
        if user_id:
            within_limit, message = is_within_limit(current_user)
            if not within_limit:
                return jsonify({"error": message}), 429
        elif not lbh.is_center_room(library_id, subtopic):
            return jsonify(status="error", message="Please login to continue."), 400

        try:
            generated_content = lgn.generate_libroom_content(user_id, subtopic, library_id)
            lbh.save_library_room_contents(library_id, subtopic, generated_content)
            existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
            if not user_id:
                mark_generation_done(ip, 'room')
            return jsonify(status="success", data=existing_content)
        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate content {e}"), 500
    
    @app.route('/api/library/available-generated-rooms', methods=['POST'])
    def get_available_generated_rooms():
        try:
            data = request.get_json()
            library_id = data.get('libraryId')
                
            if not library_id:
                return jsonify(status="error", message="No library ID provided"), 400

            # Call the separate DB logic function
            rooms = lbh.get_available_generated_rooms(library_id)
            print(rooms)
            # Success response
            return jsonify({
                "status": "success",
                "data": {
                    "rooms": rooms  # could be an empty list if none
                }
            }), 200

        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate content {e}"), 500


    @app.route("/api/library/end", methods=["POST"])
    def end_game():
        data = request.get_json()
        library_id = data.get('libraryId')
        score = data.get('score')
        time = data.get('time')
        completed_rooms = data.get('completed', []) 
        
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            return jsonify({'status': 'error', 'message': "Not logged in..."}), 401
        
        if library_id is None or score is None:
            return jsonify({'status': 'error', 'message': 'Missing libraryId or score'}), 400

        try:
            response, status = lbh.update_game_end(user_id, library_id, score, time, completed_rooms, True)
            return response, status
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
    @app.route("/api/libraries", methods=["GET"])
    def get_libraries():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        return lbh.get_libraries_info(user_id)
    
    @app.route("/api/library/like", methods=["POST"])
    def like_library():
        data = request.get_json()
        return lbh.like_library(data.get('libraryId'))
    
    @app.route('/api/scores', methods=['GET'])
    def fetch_scores():
        completions = lbh.get_top_scores_by_unique_users(limit=5)
        data = []
        for email, library_id, time in completions:
            data.append({
                "email": mask_email(email),
                "library_id": library_id,
                "time": time
            })
        return jsonify(data), 200


    @app.route('/api/scores/library/<int:library_id>', methods=['GET'])
    def fetch_scores_for_library(library_id):
        completions = lbh.get_library_top_scores_by_unique_users(library_id=library_id, limit=5)
        data = []
        for email, library_id, time in completions:
            data.append({
                "email": mask_email(email),
                "library_id": library_id,
                "time": time
            })
        return jsonify(data), 200