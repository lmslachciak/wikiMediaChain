import logging
from dotenv import load_dotenv
from WikimediaCommonsSearchTool import WikimediaCommonsSearchTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Wikimedia Commons search tool...")
    load_dotenv(override=True)

    try:
        # Instance creation
        commons_tool = WikimediaCommonsSearchTool()

        # Test search
        search_term = "locomotive steam engine"
        logger.info(f"Performing test search with term: '{search_term}'")
        results = commons_tool.run({"query": search_term, "limit": 100})
        print(results)

        # Integration with LLM
        from langchain.agents import initialize_agent, AgentType
        from langchain_openai import ChatOpenAI      

        llm = ChatOpenAI(
            model="gpt-4o")
        tools = [commons_tool]

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True
        )

        user_query = input("Enter your search query for Wikimedia Commons: ")
        agent.run(f"Can you find some images of {user_query} on Wikimedia Commons? Provide me a list of URLs")
    except Exception as e:
        logger.error(f"An error occurred: {e}")