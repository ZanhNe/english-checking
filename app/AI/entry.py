from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from app.AI.base_structure import FullGrammar, Reading
from app.AI.prompt_template import template_fix_grammar, template_fix_reading, template_check_grammar_general
import os

load_dotenv()

client_gemini = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
llm = ChatGoogleGenerativeAI(model='gemini-2.5-pro-exp-03-25', temperature=0, api_key=os.getenv('GEMINI_API_KEY'))


parser_grammar = SimpleJsonOutputParser(pydantic_object=FullGrammar)
parser_grammar_general = SimpleJsonOutputParser(pydantic_object=FullGrammar)

prompt_grammar = PromptTemplate(template=template_fix_grammar, input_variables=['sentence'], partial_variables={"format_instructions": parser_grammar.get_format_instructions()})
prompt_grammar_general = PromptTemplate(template=template_check_grammar_general, input_variables=['sentence'], partial_variables={'format_instructions': parser_grammar.get_format_instructions()})

chain_grammar = prompt_grammar | llm | parser_grammar
chain_grammar_general = prompt_grammar_general | llm | parser_grammar_general

parse_reading = SimpleJsonOutputParser(pydantic_object=Reading)
prompt_reading = PromptTemplate(template=template_fix_reading, input_variables=['Passage', 'Questions'], partial_variables={'format_instructions': parse_reading.get_format_instructions()})
chain_reading = prompt_reading | llm | parse_reading