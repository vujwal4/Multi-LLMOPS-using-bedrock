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
        #state_modifier=system_prompt
    )
    
    # Ensure query is passed as a message list
    state = {"messages": [("user", query)]}
    response = agent.invoke(state)
    
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    
    return ai_messages[-1] 
'''import botocore
from langchain_aws import ChatBedrock
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

def RAG_llm():
    # Increase read_timeout to handle agent search latency
    config = botocore.config.Config(
        read_timeout=120, 
        connect_timeout=120,
        retries={"max_attempts": 2}
    )
    
    return ChatBedrock(
        credentials_profile_name="default", 
        model_id="amazon.nova-lite-v1:0", 
        config=config, # Injects the increased timeout
        model_kwargs={
            "temperature": 0.3, 
            "top_p": 0.9, 
            "max_new_tokens": 400
        }
    )

def get_response_from_ai_agents(model_name, messages, allow_search, system_prompt):
    # model_name is passed from FastAPI, though logic below uses Bedrock
    llm = RAG_llm()
    
    # Ensure Tavily uses the API Key from your environment
    tools = [TavilySearch(max_results=2)] if allow_search else []
    
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt 
    )
    
    # Use the message list from the request
    state = {"messages": messages}
    response = agent.invoke(state)
    
    messages_out = response.get("messages")
    ai_messages = [m.content for m in messages_out if isinstance(m, AIMessage)]
    
    return ai_messages[-1] if ai_messages else "No response generated."
'''
