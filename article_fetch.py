import time

from langchain import PromptTemplate, LLMChain
from langchain.chains import StuffDocumentsChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader


def article_fetch(feed_list, logger):
    articles = []
    for feed in feed_list:
        for article in feed:
            prompt_template = """以下の記事の内容をですます調で要約してください:
                "{text}"
                簡潔な要約:
                """
            prompt = PromptTemplate.from_template(prompt_template)
            loader = WebBaseLoader(article['links'][0]['href'])
            docs = loader.load()
            llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k")
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
            logger.debug("Summarizing with ChatGPT🤖... [%s]" % article['title'])
            a = chain.run(docs)
            articles.append(a)
            # time.sleep(20)
    return articles
