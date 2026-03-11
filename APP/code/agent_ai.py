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

import logging

def get_response_from_ai_agents(query, allow_search, system_prompt):
    logger = logging.getLogger(__name__)

    try:
        llm = RAG_llm()
        logger.info("RAG_llm initialized successfully.")

        tools = [TavilySearch(max_results=2)] if allow_search else []
        logger.info(f"Tools configured: {tools}")

        agent = create_react_agent(
            model=llm,
            tools=tools,
            #state_modifier=system_prompt
        )
        logger.info("Agent created successfully.")

        # Ensure query is passed as a message list
        state = {"messages": [("user", query)]}
        logger.info(f"State initialized with query: {query}")

        response = agent.invoke(state)
        logger.info("Agent invocation completed successfully.")

        messages = response.get("messages")
        if not messages:
            logger.error("No messages found in the response.")
            raise ValueError("No messages found in the response.")

        ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
        if not ai_messages:
            logger.error("No AI messages found in the response.")
            raise ValueError("No AI messages found in the response.")

        return ai_messages[-1]

    except Exception as e:
        logger.error(f"Error during response generation: {e}")
        logger.exception("Stack trace of the error")
        raise HTTPException(
            status_code=500, 
            detail=str(CustomException("Failed to get AI response", error_detail=e))
        )
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
