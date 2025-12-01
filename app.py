import streamlit as st
import ollama

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("What's on your mind?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
       
        for response in ollama.chat(model='llama2', messages=[
            {'role': m["role"], 'content': m["content"]} 
            for m in st.session_state.messages
        ]):
            full_response += response['message']['content']
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
   
    st.session_state.messages.append({"role": "assistant", "content": full_response})
