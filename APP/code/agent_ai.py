from langchain_aws import ChatBedrock
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

def RAG_llm(): 
    return ChatBedrock(
        credentials_profile_name="default", 
        model_id="amazon.nova-lite-v1:0", 
        model_kwargs={
            "temperature": 0.3, 
            "top_p": 0.9, 
            "max_new_tokens": 400
        }
    )

def get_response_from_ai_agents(query, allow_search, system_prompt):
    # ChatGroq removed; using Nova-Lite via Bedrock directly
    llm = RAG_llm()
    
    tools = [TavilySearch(max_results=2)] if allow_search else []
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )
    
    # Ensure query is passed as a message list
    state = {"messages": [("user", query)]}
    response = agent.invoke(state)
    
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    
    return ai_messages[-1] 
