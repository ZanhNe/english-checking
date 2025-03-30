from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.globals import set_llm_cache
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
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

sapling_api = "LQ0K5L3Q6WPEQ4ICJ3NWEOASFVGFV25I"

mail = Mail()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)

migrate = Migrate(db=db)

eleven_client = ElevenLabs(api_key=os.getenv('ELEVENLAB_API_KEY'))


cors = CORS(resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# set_llm_cache(None)

llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro-exp-03-25', temperature=0.2, top_k=40, top_p=0.8, api_key=os.getenv('GEMINI_API_KEY'))

template_fix_reading = """
    You are an advanced AI specialized in linguistic analysis and reading comprehension. Your task is to analyze the following passage carefully, extract key details, and generate precise answers to comprehension questions. Be meticulous in ensuring accuracy, logical reasoning, and textual alignment when providing responses.
    Input:

    Reading Passage: {Passage}
    Question Type (Multiple-choice / True-False / Fill-in-the-blank / Short Answer)
    Questions: {Questions}


    Expected Answer Format: Returns the answer as a JSON object with keys like 'question' for The question of answer key, 'answer' for Answer (A, B, C, D or True/False, or a sentences, or word in the blank, etc.), 'explanation' for provide a short explanation of how the answer was derived from the passage. For each question + answer + explanation, there will be a corresponding JSON object element as above. Always returns a list even if there is at least one element

    Output Instructions:

    Comprehensive Analysis: Break down the passage into key themes, main ideas, and supporting details.
    Evidence-based Answering: Each answer must be strictly based on the passage. Do not rely on external knowledge.
    Explain Your Reasoning: For each answer, provide a short explanation of how the answer was derived from the passage.
    Accuracy & Clarity: Ensure the answer is concise, unambiguous, and aligned with the question format.

    Example Execution:

    Reading Passage:

    "The Amazon Rainforest, often referred to as the ‘lungs of the Earth,’ produces 20% of the world's oxygen. It is home to millions of species and plays a crucial role in regulating global climate patterns. However, deforestation has significantly threatened this ecosystem, leading to biodiversity loss and climate disruptions."

    Questions & Answers:

    Q1: What percentage of the world's oxygen does the Amazon Rainforest produce?

    A) 10%
    B) 15%
    C) 20%
    D) 25%

    Question: What percentage of the world's oxygen does the Amazon Rainforest produce?
    Answer: C.
    Explanation: The passage explicitly states that "The Amazon Rainforest produces 20% of the world's oxygen."

    Question: The Amazon Rainforest has no impact on climate regulation. (True/False)
    Answer: False
    Explanation: The passage mentions that the Amazon "plays a crucial role in regulating global climate patterns," indicating its significant impact on climate regulation.
    
    Question: The Amazon Rainforest is often called the ‘______ of the Earth.’
    Answer: lungs
    Explanation: The passage directly states that the Amazon is referred to as "the lungs of the Earth."
"""

template_fix_grammar = """
Bạn là một chuyên gia dạy tiếng Anh và là chuyên gia ngôn ngữ học, nhiệm vụ của bạn là giúp học viên trung bình/yếu cải thiện kỹ năng Writing.  
Nhiệm vụ của bạn là phân tích kỹ lưỡng câu sau đây, chỉ ra tất cả các lỗi về ngữ pháp (bao gồm lỗi về thì, sự đồng nhất chủ ngữ – động từ, lỗi đại từ, lỗi giới từ, v.v.) và đưa ra gợi ý sửa lỗi cho từng lỗi cụ thể.  

Yêu cầu:
1. **Kiểm tra và phân tích**:
   - Phân tích chính xác từng lỗi trong câu. Nếu câu đúng, hãy xác nhận rõ ràng rằng câu không có lỗi.
   - Nếu phát hiện lỗi, hãy liệt kê hết tất cả các từ/cụm từ bị sai.

2. **Đưa ra gợi ý sửa lỗi**:
   - Với mỗi lỗi, không cần phải sửa lại toàn bộ câu, chỉ đưa ra đề xuất sửa lỗi cho phần cụ thể bị sai.
   - Nếu có lỗi liên quan đến nhiều yếu tố (ví dụ: lỗi về thì và lỗi về cấu trúc câu), hãy giải thích theo cách cụ thể nhưng vẫn dễ hiểu đối với học viên trung bình/yếu, có thể kèm theo kiến thức liên quan.

3. **Định dạng kết quả**:
   - Trả về một object JSON với các key sau:
       - `"is_correct"`: Boolean xác định rằng câu ban đầu có đúng hoàn toàn hay không.
       - `"grammar_check_details"`: Một danh sách các object, mỗi object ứng với một lỗi cụ thể, với các key:
           - `"keyword"`: Danh sách các từ hoặc cụm từ bị sai.
           - `"error"`: Mô tả cụ thể lỗi sai và có thể kèm theo kiến thức liên quan nếu cần.
           - `"suggestion"`: Đề xuất sửa lỗi cho phần bị sai (chỉ sửa phần lỗi, không phải toàn bộ câu).
       - `"correct_sentence"`: Nếu câu sai, đưa ra câu đã được sửa lỗi hoàn chỉnh; nếu câu đúng, trả về câu gốc.

4. **Lưu ý quan trọng**:
   - Không được tự ý cho rằng câu đúng hoặc sai nếu không kiểm chứng chính xác.
   - Phải đảm bảo liệt kê đầy đủ tất cả các lỗi phát hiện được trong câu.
   - Đảm bảo kết quả luôn trả về dưới dạng một object JSON đầy đủ theo cấu trúc đã chỉ định.
   - Phân tích dựa trên {sentence} được cung cấp.

Ví dụ:

Input mẫu: 
INPUT: "Yesterday, I go to the bookstore because I want buy some new book."
OUTPUT:
{{
  "is_correct": false,
  "grammar_check_details": [
    {{
      "keyword": ["go"],
      "error": "Lỗi chia động từ: Với chủ ngữ 'I' thì cần sử dụng 'went' hoặc 'go' phù hợp với thì quá khứ.",
      "suggestion": "I went"
    }},
    {{
      "keyword": ["want buy"],
      "error": "Lỗi cách dùng động từ: Cần thêm giới từ 'to' sau 'want' để thành 'want to buy'.",
      "suggestion": "want to buy"
    }},
    {{
      "keyword": ["new book"],
      "error": "Lỗi về số ít/số nhiều: 'book' cần ở dạng số nhiều nếu nói về nhiều cuốn sách, hoặc nên sử dụng 'a new book' nếu chỉ là một cuốn.",
      "suggestion": "a new book"
    }}
  ],
  "correct_sentence": "Yesterday, I went to the bookstore because I wanted to buy a new book."
}}

"""


template_check_grammar_general = """
Bạn là một chuyên gia dạy tiếng Anh, nhiệm vụ của bạn là giúp học viên khá/giỏi cải thiện kỹ năng Writing. 
Cho một đoạn văn mà học viên đã viết, bạn cần thực hiện các bước sau:

1. **Sửa lỗi**:
   - Kiểm tra toàn bộ đoạn văn và xác định tất cả các lỗi ngữ pháp, từ vựng, và cách dùng câu.
   - Nếu một câu có lỗi lớn, hãy viết lại toàn bộ câu sao cho tự nhiên và đúng ngữ pháp.
   - Nếu câu chỉ có lỗi nhỏ, hãy giữ nguyên cấu trúc chính và chỉ sửa những lỗi cần thiết.
   - Lưu ý: Không được bỏ sót lỗi nào trong đoạn văn. Mỗi từ hoặc cụm từ sai cần được nhận diện.

2. **Giải thích lỗi**:
   - Với mỗi câu bị sửa, gom lại tất cả các lỗi xảy ra trong câu đó thành một lời giải thích chung chung (không đi vào chi tiết từng lỗi quá mức) nhưng vẫn liệt kê hết các từ/cụm từ bị lỗi.
   - Giải thích này cần chỉ ra loại lỗi chính (ví dụ: lỗi chia động từ, sử dụng từ không phù hợp, lỗi cấu trúc, v.v.) và cách sửa đã áp dụng.

3. **Định dạng kết quả**:
   - Trả về một Object JSON với các key sau:
     - `"is_correct"`: Boolean xác định xem đoạn văn ban đầu có đúng hoàn toàn hay không.
     - `"grammar_check_details"`: Một mảng các object, mỗi object ứng với một câu bị sửa, bao gồm:
         - `"keyword"`: Danh sách các từ hoặc cụm từ bị sai (liệt kê hết tất cả các lỗi được phát hiện trong câu đó).
         - `"error"`: Mô tả chung về lỗi sai của câu đó (không cần phân tích chi tiết từng lỗi, nhưng phải nêu ra lỗi chính của câu).
         - `"suggestion"`: Đề xuất sửa lại toàn bộ câu, tức là câu đã được sửa hoàn chỉnh.
     - `"correct_sentence"`: Chuỗi văn bản là đoạn văn đã được sửa lại, với tất cả các câu được chỉnh sửa đúng ngữ pháp và tự nhiên.

4. **Hướng dẫn bổ sung**:
   - Đảm bảo rằng bạn kiểm tra và sửa toàn bộ đoạn văn, không chỉ sửa một số lỗi rồi dừng lại.
   - Giải thích lỗi theo cách phù hợp với người học khá/giỏi: súc tích, tổng hợp các lỗi trong một câu mà không đi quá sâu vào chi tiết từng lỗi nhỏ.
   - Phân tích và sửa dựa trên biến {sentence} được cung cấp.

Ví dụ:

Input mẫu:
INPUT = "She go to school everyday because she like study English. She want improve her skills, so she practice a lot."
OUTPUT:
{{
  is_correct: false,
  grammar_check_details: [
    {{
      keyword: ["go", "everyday", "like study"],
      error: "Câu có lỗi về chia động từ, cách sử dụng trạng từ và danh động từ.",
      suggestion: "She goes to school every day because she enjoys studying English."
    }},
    {{
      keyword: ["want", "practice"],
      error: "Câu có lỗi về chia động từ cho chủ ngữ số ít.",
      suggestion: "She wants to improve her skills, so she practices a lot."
    }}
  ],
  correct_sentence: "She goes to school every day because she enjoys studying English. She wants to improve her skills, so she practices a lot."
}}

Chú ý:
    Đảm bảo liệt kê đầy đủ các từ hoặc cụm từ sai trong phần "keyword" cho mỗi câu.

    Giải thích lỗi trong "error" là tổng hợp lỗi chính của câu đó, không cần đi vào chi tiết từng từ nhưng phải đủ để học viên hiểu được điểm cần cải thiện.

    "suggestion" phải là câu đã được chỉnh sửa hoàn chỉnh và tự nhiên.


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


class Reading(BaseModel):
    question: str = Field(description='The question of answer key')
    answer: str = Field(description='Answer (A, B, C, D or True/False, or a sentences, or word in the blank, etc.)')
    explaination: str = Field(description='provide a short explanation of how the answer was derived from the passage.')


class Speaking(BaseModel):
    user_speaking: str = Field(description='Câu nói của người dùng')
    ai_speaking: str = Field(description='Câu nói của AI (là bạn)')

class Grammar(BaseModel):
    keyword: list = Field(description='Các từ bị sai trong ngữ pháp, có từ nào sai thì đưa vào đây')
    error: str = Field(description='Lỗi ngữ pháp cụ thể, có lỗi gì thì đưa vào đây bằng Tiếng Việt giải thích, và có thể đề xuất thêm phần kiến thức liên quan đến lỗi này')
    suggestion: str = Field(description='Đề xuất lại sửa lỗi, chỉ sửa từng chỗ chứ không nguyên câu')

class FullGrammar(BaseModel):
    is_correct: bool = Field(description='Nếu câu đúng, thì trả ra True, câu sai thì trả ra False')
    grammar_check_details: list[Grammar] = Field(description='Chứa danh sách những phần kiểm tra grammar')
    correct_sentence: str = Field(description='Câu đã được sửa')

parse_reading = SimpleJsonOutputParser(pydantic_object=Reading)
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



parser_grammar = SimpleJsonOutputParser(pydantic_object=FullGrammar)
parser_grammar_general = SimpleJsonOutputParser(pydantic_object=FullGrammar)

prompt_grammar = PromptTemplate(template=template_fix_grammar, input_variables=['sentence'], partial_variables={"format_instructions": parser_grammar.get_format_instructions()})
prompt_grammar_general = PromptTemplate(template=template_check_grammar_general, input_variables=['sentence'], partial_variables={'format_instructions': parser_grammar.get_format_instructions()})

prompt_reading = PromptTemplate(template=template_fix_reading, input_variables=['Passage', 'Questions'], partial_variables={'format_instructions': parse_reading.get_format_instructions()})
chain_grammar = prompt_grammar | llm | parser_grammar
chain_grammar_general = prompt_grammar_general | llm | parser_grammar_general

chain_reading = prompt_reading | llm | parse_reading

# chain_speaking = prompt_speaking | llm | parser_speaking
