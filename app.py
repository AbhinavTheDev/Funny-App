# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
import stable_diffusion, ai21_studio

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Configure Streamlit page and state
st.set_page_config(page_title="AI21 Studio Tutorial", page_icon="🍩")

# Store the initial value of widgets in session state
if "imagine" not in st.session_state:
    st.session_state.imagine = ""

if "img_path" not in st.session_state:
    st.session_state.img_path = ""

if "query" not in st.session_state:
    st.session_state.query = ""

if "im_query" not in st.session_state:
    st.session_state.im_query = ""

if "prompt_generate" not in st.session_state:
    st.session_state.prompt_generate = ""

# yaha par yeh daala tha par kuch sahi nhi hua 
# if "file_path" not in st.session_state:
#    st.session_state.file_path = ""
    
if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "stable_diffusion_api_key" not in st.session_state:
    st.session_state.stable_diffusion_api_key = ""

if "ai21_api_key" not in st.session_state:
    st.session_state.ai21_api_key = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"

# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# For generating ideas
def generate_ideas():

    st.session_state.text_error = ""

    if st.session_state.cohere_api_key == "":
        st.session_state.text_error = "Missed API key."
        return


    st.session_state.text_error = ""

    if st.session_state.file_path == "" or st.session_state.query == "":
        st.session_state.text_error = "Missed a file or query."
        return


    st.session_state.prompt_generate = ""
    st.session_state.text_error = ""
    
# yaha par yeh daala tha par kuch sahi nhi hua 
   # st.session_state.file_path = ""

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            prompt = ai21_studio.generate(prompt=st.session_state.query, ai21_api_key=st.session_state.ai21_api_key)

            if prompt == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.prompt_generate = (prompt)
            
# yaha par yeh daala tha par kuch sahi nhi hua 
           # st.session_state.file_path = (file_path)

# For generating images
def imagine():

    st.session_state.text_error = ""

    if st.session_state.stable_diffusion_api_key == "":
        st.session_state.text_error = "Missed API key."
        return


    st.session_state.text_error = ""

    if st.session_state.im_query == "":
        st.session_state.text_error = "Missed a query."
        return

    st.session_state.imagine = ""
    st.session_state.img_path = ""
    st.session_state.text_error = ""

    with text_spinner_placeholder:
        with st.spinner("Please wait while we generate your image..."):
            im_path = stable_diffusion.imagine(prompt=st.session_state.im_query, stable_diffusion_api_key=st.session_state.stable_diffusion_api_key)

            if im_path == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.img_path = (im_path)

# Render Streamlit page
with st.sidebar:
    st.session_state.cohere_api_key = st.text_input('AI21 Studio API Key', )
    st.session_state.stable_diffusion_api_key = st.text_input('Stable Diffusion API Key', )

# title of the app
st.title("AI21 Studio + Stable Diffusion Tutorial")


st.markdown(
    "This is a demo of the AI21 Studio + Stable Diffusion Tutorial app."
)

# textarea
st.session_state.query = st.text_area(
    label="Generate engaging ideas for tweets",
    placeholder="Elon Musk wants to fight with Mu", height=100)


# button
st.button(
    label="Generate ideas",
    help="Click to genearate ideas",
    key="generate_prompt",
    type="primary",
    on_click=generate_ideas,
    )

# textarea
st.session_state.im_query = st.text_area(label="Cool description for tweets cover", placeholder="Elon Musk wants to fight with Mu", height=100)


# button
st.button(
    label="Generate image",
    help="Click to genearate image",
    key="generate_image",
    type="primary",
    on_click=imagine,
)

text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.prompt_generate:
    st.markdown("""---""")
    st.text_area(label="Cool ideas", value=st.session_state.prompt_generate,)
    
# yaha par yeh daala tha par kuch sahi nhi hua 
# if st.session_state.file_path:
  #  st.markdown("""---""")
 #   st.subheader("Engaging Ideas")
#    st.file(st.session_state.file_path, use_column_width=True, caption="Ideas generated by Ai21 studio", output_format="PNG")
    
if st.session_state.img_path:
    st.markdown("""---""")
    st.subheader("Cool image")
    st.image(st.session_state.img_path, use_column_width=True, caption="Image generated by Stable Diffusion", output_format="PNG")
