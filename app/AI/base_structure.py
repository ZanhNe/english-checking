from pydantic import BaseModel, Field

class Reading(BaseModel):
    question: str = Field(description='The question of answer key')
    answer: str = Field(description='Answer (A, B, C, D or True/False, or a sentences, or word in the blank, etc.)')
    explanation: str = Field(description='provide a short explanation of how the answer was derived from the passage.')
    segments: str = Field(description='the specific paragraph(s) or segment(s) (e.g., "Paragraph 2", "Segment 2.3") from which the evidence was extracted.')


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

config_reading_gemini={
        'temperature': 0,
        'response_mime_type': 'application/json',
        'response_schema': list[Reading],
}