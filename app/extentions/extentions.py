from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from app.models.models import db, User, Role
from flask_migrate import Migrate
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_SECRET_API_KEY')
)



mail = Mail()
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
migrate = Migrate(db=db)

eleven_client = ElevenLabs(api_key=os.getenv('ELEVENLAB_API_KEY'))


cors = CORS(resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=os.getenv('GEMINI_API_KEY'))

template_fix_grammar = """
    Bạn là một chuyên gia ngôn ngữ học chuyên phân tích ngữ pháp tiếng Anh. 
    Nhiệm vụ của bạn là phân tích câu sau đây, chỉ ra tất cả các lỗi về ngữ pháp (bao gồm lỗi về thì, sự đồng nhất chủ ngữ – động từ, lỗi đại từ, v.v.) và đưa ra gợi ý sửa lỗi.
    Chỉ ra lỗi sai ngữ pháp của câu, và trả ra kết quả dưới dạng JSON với các key như 'keyword' chỉ ra các từ vựng bị sai ngữ pháp, 'error' chỉ rõ lỗi sai cụ thể và có thể đề xuất thêm phần kiến thức liên quan đến lỗi, 'suggestion' đề xuất lại sửa lỗi chỗ bị sai, chứ không cần nguyên câu
    Nên nhớ là rà soát toàn bộ lỗi trong câu chứ không xem qua một cách đơn giản
    Luôn trả ra list object mặc dù chỉ có 1 object
    Phân tích dựa trên {sentence}
"""

human_template_speaking = """
    Bạn hãy đối thoại với người dùng một cách tự nhiên giống như 2 người bạn.
    Nói chuyện bằng ngôn ngữ tiếng anh.

    Tuyệt đối không nói các vấn đề khác, chỉ giao tiếp đơn thuần thôi, nếu như người dùng có hỏi những cái ngoài phạm vi của speaking thì kêu không hỗ trợ
    
    Câu nói người dùng: {sentence_speaking}

"""

prompt_speaking = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name='history'),
    ('human', human_template_speaking),
])


class Speaking(BaseModel):
    user_speaking: str = Field(description='Câu nói của người dùng')
    ai_speaking: str = Field(description='Câu nói của AI (là bạn)')

class Grammar(BaseModel):
    keyword: list = Field(description='Các từ bị sai trong ngữ pháp, có từ nào sai thì đưa vào đây')
    error: str = Field(description='Lỗi ngữ pháp cụ thể, có lỗi gì thì đưa vào đây bằng Tiếng Việt giải thích, và có thể đề xuất thêm phần kiến thức liên quan đến lỗi này')
    suggestion: str = Field(description='Đề xuất lại sửa lỗi, chỉ sửa từng chỗ chứ không nguyên câu')


parser_speaking = SimpleJsonOutputParser(pydantic_object=Speaking)

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain_speaking = RunnableWithMessageHistory(
    prompt_speaking | llm,
    get_session_history=get_by_session_id,
    input_messages_key='sentence_speaking',
    history_messages_key='history',
)



parser_grammar = SimpleJsonOutputParser(pydantic_object=Grammar)
prompt_grammar = PromptTemplate(template=template_fix_grammar, input_variables=['sentence'], partial_variables={"format_instructions": parser_grammar.get_format_instructions()})

chain_grammar = prompt_grammar | llm | parser_grammar
# chain_speaking = prompt_speaking | llm | parser_speaking
