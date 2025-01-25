import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader





## sstreamlit APP
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader('Summarize URL')

groq_api_key="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"

st.write(f"Entered API Key: {groq_api_key}")  # Debugging step to check the input value



with st.sidebar:
    groq_api_key=st.text_input("Groq API key",value="",type="password")

generic_url=st.text_input("URL",label_visibility='collapsed')

if groq_api_key.strip():  # Ensure it's not an empty string
    llm = ChatGroq(model='Gemma-7b-It', groq_api_key=groq_api_key)
else:
    st.error("Groq API key is missing. Please enter a valid API key.")



prompt_i='''
Provide a summary of the flowing content in 300 words:content={text}
 '''
final_prompt=PromptTemplate(template=prompt_i,input_variables=['text'])

if st.button("summerize the content from YT or Website"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide information")
    elif not validators.url(generic_url):
        st.error("please enter a velid url it can may be a YT video url or website url")

    else:
        try:
            with st.spinner("Waiting..."):
                if 'youtube.com' in generic_url:
                    loader=YoutubeLoader.from_youtube_url(generic_url,add_video_info=True)
                else:
                     loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs=loader.load()
                chain=load_summarize_chain(llm,chain_type='stuff',prompt=prompt_i)
                output=chain.run(docs)
                st.success(output)

        except Exception as e:
            st.exception(f"Exception:{e}")
            
