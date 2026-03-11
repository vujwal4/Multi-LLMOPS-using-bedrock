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
