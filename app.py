import streamlit as st
from agent import chat
from smartFeatures import get_daily_briefing, get_priority_summary
from storage import load_tasks

st.set_page_config(
    page_title="Task Management Agents",
    page_icon = "",
    layout="wide",
)
st.title(" PERSONAL TASK MANAGEMENT AGENT ")
st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Chat with Agent ")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Talk to agenet..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader(" TASK OVERVIEW ")

    tasks = load_tasks()
    pending = [t for t in tasks if t.status == "pending"]
    done = [t for t in tasks if t.status == "done"]

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Pending", len(pending))
    with col_b:
        st.metric("Complete", len(done))

    st.markdown("---")

    if st.button("> GET DAILY BRIEFING <"):
        with st.spinner("Generating daily briefing..."):
            briefing = get_daily_briefing()
        st.info(briefing)

    if st.button("> PRIORITY RANKING <"):
        summary = get_priority_summary()
        st.success(summary)

    st.markdown("---")
    st.subheader("-- ALL TASK --")

    if not tasks:
        st.write("[ No Task Yet ]")
    else:
        for task in tasks:
            if task.status == "done":
                st.success(f" FINISHED {task.title}")
            elif task.priority == "high":
                st.error(f"HIGH.PRIO [{task.title}] - Due: {task.due_date}")
            elif task.priority == "medium":
                st.warning(f"MEDIUM.PRIO [{task.title}] - Due: {task.due_date}")
            else:
                st.info(f"LOW.PRIO [{task.title}] - Due: {task.due_date}")
