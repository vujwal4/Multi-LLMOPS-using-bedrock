from langchain_aws import ChatBedrock
from APP.config.settings import settings
import os
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
#os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
def RAG_llm(): 
    return ChatBedrock(
        #credentials_profile_name="default", 
        model_id="amazon.nova-lite-v1:0", 
        model_kwargs={
            "temperature": 0.3, 
            "top_p": 0.9, 
            "max_new_tokens": 400
        }
    )

def get_response_from_ai_agents(query, allow_search, system_prompt):

    llm = RAG_llm()

    tools = [TavilySearch(max_results=2)] if allow_search else []
    tools = [TavilySearch(api_key=settings.TAVILY_API_KEY, max_results=2)] if allow_search else []
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    user_message = query[-1] if query else ""

    state = {
        "messages": [
            ("system", system_prompt),
            ("user", user_message)
        ]
    }

    response = agent.invoke(state)

    messages = response.get("messages", [])

    ai_messages = [
        m.content
        for m in messages
        if isinstance(m, AIMessage)
    ]

    return ai_messages[-1] if ai_messages else "No response generated"
