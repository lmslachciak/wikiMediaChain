from dotenv import load_dotenv
from WikimediaCommonsSearchTool import WikimediaCommonsSearchTool 


if __name__ == "__main__":
    load_dotenv(override=True)

    # instance creation
    commons_tool = WikimediaCommonsSearchTool()

    # test search
    search_term = "locomotive steam engine"
    results = commons_tool.run({"query": search_term, "limit": 100})
    print(results)

    # integration with LLM
    from langchain.agents import initialize_agent, AgentType
    from langchain_openai import ChatOpenAI # lub inny model LLM

    llm = ChatOpenAI()
    tools = [commons_tool]

    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    agent.run("Can you find some images of Polish steam locomotives on Wikimedia Commons?")