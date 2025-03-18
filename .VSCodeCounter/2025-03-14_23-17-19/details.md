# Details

Date : 2025-03-14 23:17:19

Directory /Users/willgunter/projects/Gamefied-Study-Tool/backend

Total : 69 files,  5165 codes, 795 comments, 1303 blanks, all 7263 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [backend/app.py](/backend/app.py) | Python | 105 | 18 | 26 | 149 |
| [backend/completion\_tasks.py](/backend/completion_tasks.py) | Python | 185 | 6 | 40 | 231 |
| [backend/database/db\_handlers.py](/backend/database/db_handlers.py) | Python | 501 | 25 | 118 | 644 |
| [backend/database/document\_handlers.py](/backend/database/document_handlers.py) | Python | 37 | 5 | 12 | 54 |
| [backend/database/library\_handlers.py](/backend/database/library_handlers.py) | Python | 498 | 55 | 121 | 674 |
| [backend/database/models.py](/backend/database/models.py) | Python | 180 | 3 | 45 | 228 |
| [backend/database/upgrade\_db.py](/backend/database/upgrade_db.py) | Python | 46 | 1 | 14 | 61 |
| [backend/database/user\_handler.py](/backend/database/user_handler.py) | Python | 90 | 51 | 24 | 165 |
| [backend/email\_provider/email\_templates.py](/backend/email_provider/email_templates.py) | Python | 80 | 2 | 7 | 89 |
| [backend/email\_provider/resend\_api.py](/backend/email_provider/resend_api.py) | Python | 14 | 1 | 4 | 19 |
| [backend/functions.py](/backend/functions.py) | Python | 329 | 132 | 22 | 483 |
| [backend/images/library\_imager.py](/backend/images/library_imager.py) | Python | 33 | 22 | 11 | 66 |
| [backend/knowledge\_net/SystemPrompts/prompt\_utils.py](/backend/knowledge_net/SystemPrompts/prompt_utils.py) | Python | 100 | 0 | 27 | 127 |
| [backend/knowledge\_net/explore.py](/backend/knowledge_net/explore.py) | Python | 34 | 2 | 3 | 39 |
| [backend/knowledge\_net/graph\_calc.py](/backend/knowledge_net/graph_calc.py) | Python | 75 | 17 | 26 | 118 |
| [backend/knowledge\_net/library\_generator.py](/backend/knowledge_net/library_generator.py) | Python | 89 | 6 | 17 | 112 |
| [backend/knowledge\_net/math\_utils.py](/backend/knowledge_net/math_utils.py) | Python | 17 | 0 | 6 | 23 |
| [backend/message\_handler.py](/backend/message_handler.py) | Python | 94 | 1 | 21 | 116 |
| [backend/migrate\_db.py](/backend/migrate_db.py) | Python | 10 | 2 | 5 | 17 |
| [backend/migrations/alembic.ini](/backend/migrations/alembic.ini) | Ini | 38 | 0 | 13 | 51 |
| [backend/migrations/env.py](/backend/migrations/env.py) | Python | 66 | 17 | 31 | 114 |
| [backend/migrations/versions/036b751c460b\_.py](/backend/migrations/versions/036b751c460b_.py) | Python | 24 | 5 | 10 | 39 |
| [backend/migrations/versions/21f775927f5b\_.py](/backend/migrations/versions/21f775927f5b_.py) | Python | 19 | 5 | 11 | 35 |
| [backend/migrations/versions/250462cadd46\_.py](/backend/migrations/versions/250462cadd46_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/54a3f0868831\_.py](/backend/migrations/versions/54a3f0868831_.py) | Python | 23 | 5 | 13 | 41 |
| [backend/migrations/versions/63fb22cbe5ef\_.py](/backend/migrations/versions/63fb22cbe5ef_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/677b09341aea\_.py](/backend/migrations/versions/677b09341aea_.py) | Python | 40 | 5 | 8 | 53 |
| [backend/migrations/versions/6962e9d76135\_.py](/backend/migrations/versions/6962e9d76135_.py) | Python | 37 | 5 | 10 | 52 |
| [backend/migrations/versions/6f6d3dea7f24\_.py](/backend/migrations/versions/6f6d3dea7f24_.py) | Python | 35 | 25 | 20 | 80 |
| [backend/migrations/versions/7263ddcf4b57\_.py](/backend/migrations/versions/7263ddcf4b57_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/77791963377c\_.py](/backend/migrations/versions/77791963377c_.py) | Python | 72 | 5 | 18 | 95 |
| [backend/migrations/versions/7f981508ecb6\_.py](/backend/migrations/versions/7f981508ecb6_.py) | Python | 20 | 5 | 10 | 35 |
| [backend/migrations/versions/804348085f99\_.py](/backend/migrations/versions/804348085f99_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/816886ffb28f\_.py](/backend/migrations/versions/816886ffb28f_.py) | Python | 22 | 5 | 9 | 36 |
| [backend/migrations/versions/8750f891a884\_.py](/backend/migrations/versions/8750f891a884_.py) | Python | 32 | 5 | 13 | 50 |
| [backend/migrations/versions/87c5c12acbdf\_.py](/backend/migrations/versions/87c5c12acbdf_.py) | Python | 36 | 5 | 10 | 51 |
| [backend/migrations/versions/8a8d8b0220ac\_.py](/backend/migrations/versions/8a8d8b0220ac_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/8c2486640fd3\_.py](/backend/migrations/versions/8c2486640fd3_.py) | Python | 21 | 5 | 13 | 39 |
| [backend/migrations/versions/9402fc9cf2b2\_.py](/backend/migrations/versions/9402fc9cf2b2_.py) | Python | 51 | 5 | 9 | 65 |
| [backend/migrations/versions/9c7833a99288\_.py](/backend/migrations/versions/9c7833a99288_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/b181e191204f\_.py](/backend/migrations/versions/b181e191204f_.py) | Python | 112 | 5 | 9 | 126 |
| [backend/migrations/versions/b7f83ec6f8f2\_.py](/backend/migrations/versions/b7f83ec6f8f2_.py) | Python | 24 | 5 | 9 | 38 |
| [backend/migrations/versions/ba8819a34f40\_.py](/backend/migrations/versions/ba8819a34f40_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/c1a09d011674\_.py](/backend/migrations/versions/c1a09d011674_.py) | Python | 30 | 5 | 10 | 45 |
| [backend/migrations/versions/f0919ba3c71b\_.py](/backend/migrations/versions/f0919ba3c71b_.py) | Python | 26 | 5 | 12 | 43 |
| [backend/migrations/versions/f396a58e8fdd\_.py](/backend/migrations/versions/f396a58e8fdd_.py) | Python | 17 | 5 | 11 | 33 |
| [backend/migrations/versions/ffbba5ee324c\_check\_constrainst.py](/backend/migrations/versions/ffbba5ee324c_check_constrainst.py) | Python | 37 | 8 | 13 | 58 |
| [backend/openapi.py](/backend/openapi.py) | Python | 222 | 18 | 44 | 284 |
| [backend/rag.py](/backend/rag.py) | Python | 87 | 1 | 22 | 110 |
| [backend/requirements.txt](/backend/requirements.txt) | pip requirements | 51 | 0 | 1 | 52 |
| [backend/roles.py](/backend/roles.py) | Python | 16 | 1 | 9 | 26 |
| [backend/routes/admin\_routes.py](/backend/routes/admin_routes.py) | Python | 18 | 1 | 5 | 24 |
| [backend/routes/auth\_routes.py](/backend/routes/auth_routes.py) | Python | 107 | 47 | 27 | 181 |
| [backend/routes/chat\_routes.py](/backend/routes/chat_routes.py) | Python | 119 | 4 | 23 | 146 |
| [backend/routes/feedback\_routes.py](/backend/routes/feedback_routes.py) | Python | 54 | 2 | 15 | 71 |
| [backend/routes/graph\_routes.py](/backend/routes/graph_routes.py) | Python | 57 | 0 | 8 | 65 |
| [backend/routes/library\_routes.py](/backend/routes/library_routes.py) | Python | 282 | 58 | 80 | 420 |
| [backend/routes/profile\_routes.py](/backend/routes/profile_routes.py) | Python | 43 | 22 | 14 | 79 |
| [backend/routes/utility\_routes.py](/backend/routes/utility_routes.py) | Python | 30 | 1 | 9 | 40 |
| [backend/services/vision\_api.py](/backend/services/vision_api.py) | Python | 0 | 1 | 0 | 1 |
| [backend/stats.py](/backend/stats.py) | Python | 121 | 7 | 30 | 158 |
| [backend/system\_guide.py](/backend/system_guide.py) | Python | 113 | 3 | 19 | 135 |
| [backend/test.py](/backend/test.py) | Python | 3 | 9 | 2 | 14 |
| [backend/testEmbed.py](/backend/testEmbed.py) | Python | 185 | 76 | 59 | 320 |
| [backend/utils.py](/backend/utils.py) | Python | 41 | 10 | 11 | 62 |
| [backend/vector\_processing/embedding\_service.py](/backend/vector_processing/embedding_service.py) | Python | 88 | 8 | 14 | 110 |
| [backend/vector\_processing/file\_handler.py](/backend/vector_processing/file_handler.py) | Python | 40 | 3 | 6 | 49 |
| [backend/vector\_processing/file\_processing.py](/backend/vector_processing/file_processing.py) | Python | 25 | 3 | 8 | 36 |
| [backend/vector\_processing/retrieval.py](/backend/vector_processing/retrieval.py) | Python | 45 | 1 | 9 | 55 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)