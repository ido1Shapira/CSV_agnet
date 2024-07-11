from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

system_prompt = """
    You MUST think step by step by answering the query.

    For the following query, if it requires drawing a table, reply as follows:
    {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

    If the query requires creating a bar chart, reply as follows:
    {"bar": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

    If the query requires creating a line chart, reply as follows:
    {"line": {"columns": ["A", "B", "C", ...], "data": [25, 24, 10, ...]}}

    There can only be two types of chart, "bar" and "line".

    If it is just asking a question that requires neither, reply as follows:
    {"answer": "answer"}
    Example:
    {"answer": "The title with the highest rating is 'Gilead'"}

    If you do not know the answer, reply as follows:
    {"answer": "I do not know."}
    
    If you need to simplify the query, reply as follows:
    {"answer": "I do not clearly understand your query please simplify your query."}

    Return all output as a string.

    All strings in "columns" list and data list, should be in double quotes,

    For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}
    
    Below is the query.
    Query:
"""


def get_prompt(query: str) -> str:
    return system_prompt + query


simple_system_prompt = "You are very powerful assistant named Ido Shapira"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", simple_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ]
)
