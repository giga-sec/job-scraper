import streamlit as st
import subprocess
import pandas as pd
import plotly.express as px
import plotly.io as pio
import openai

pio.templates.default = "plotly_dark"  # You can choose from "plotly", "plotly_white", "ggplot2", "seaborn", etc.

def tableChart(dataframe):
  st.dataframe(dataframe, hide_index=True, width=300)

def barChart1to10(dataframe):
  ## Prepare data for Plotly chart
  df2_top10 = dataframe.head(10)
  job_skills = df2_top10['jobSkills'].tolist()[::-1]  #[::-1] is used to indirectly display charts top to bottom
  counts = df2_top10['count'].tolist()[::-1]  #[::-1] is used to indirectly display charts top to bottom
  ## Create a horizontal bar chart using Plotly
  # chart = Figure()
  # chart.add_trace(Bar(x=counts, y=job_skills, orientation='h'))
  chart = px.bar(
    df2_top10,
    x=counts,
    y=job_skills,
    title="<b>Top 1-10 Job Trend Skills</b>",
    template="plotly_white",
    text=counts,
    color_discrete_sequence=["#0083B8"],
  )
  ## Display the chart using Streamlit
  return chart

def barChart11to20(dataframe):
  ## Prepare data for Plotly chart
  df2_top20 = dataframe.iloc[11:20]
  job_skills = df2_top20['jobSkills'].tolist()[::-1]  #[::-1] is used to indirectly display charts top to bottom
  counts = df2_top20['count'].tolist()[::-1] # [::-1] is used to indirectly display charts top to bottom
  ## Create a horizontal bar chart using Plotly
  # chart = Figure()
  # chart.add_trace(Bar(x=counts, y=job_skills, orientation='h'))
  chart = px.bar(
    df2_top20,
    x=counts,
    y=job_skills,
    title="<b>Top 11-20 Job Trend Skills</b>",
    template="plotly_white",
    text=counts,
    color_discrete_sequence=["#0083B8"]
    # **{'yaxis': {'autorange': 'reversed'}}
  )
  ## Display the chart using Streamlit
  return chart
  




st.set_page_config(layout="wide")

# Start of Sidebar 
signal = "Skills not Analyzed"
with st.sidebar:
  # Add elements to the sidebar
  st.title("Sidebar Menu")
  st.write("This is some content in the sidebar")
  # You can add other widgets like buttons, sliders, etc. here

  # Initial state (skills hidden)
  show_skills = False

  # Get user input for job title
  job_title = st.text_input("Enter your job title:")
  

  is_disabled = True  # Initial state
  state = True
  # Button to enable/disable text area
  if (job_title != "") and (state == True):
      is_disabled = False
      st.write("Job Title:", job_title)
      subprocess.run(["python", "scrape.py", job_title])
      st.write("Scraped")

  ai_generate_skills = st.button("AI Generated")
  if ai_generate_skills:
    openai.api_key = ""
    prompt = f"""
            Give me strictly 100 skills needed for {job_title}
            No explanation.
            Separate skills with commas.
            One to Three Words only. Acronyms are allowed 
            Strictly separate acronym and definition
            Correct: Content Management System, CMS
            Incorrect: Content Management System (CMS)
             """
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=50,  # Adjust the maximum number of tokens generated
        n=1,  # Number of desired completions
        stop=None,  # Optional stop character
        temperature=0.3,  # Adjust the randomness of the generation
    )
    response = response.choices[0].text
    skills_list = st.text_area("Skills:", height=500, disabled=is_disabled, key="text_area", value=response)
  else:
    skills_list = st.text_area("Skills:", height=500, disabled=is_disabled, key="text_area")
  show_text_area = True  # Flag to control visibility

  
  if skills_list:
    subprocess.run(["python", "bigram_jobskills.py", job_title, skills_list])
    st.write("Skills Analyzed")
    signal = "Skills Analyzed Done"

# ^-- End of Sidebar


# Main Menu Section Below
def highlight_keyword(s):
  return ['background-color: yellow' if 'javascript' in str(v) else '' for v in s]



st.markdown("""# Cebu City Job-Skills Real Time Analysis
            """)


pio.templates.default = "plotly_dark"  # You can choose from "plotly", "plotly_white", "ggplot2", "seaborn", etc.
tabs = st.tabs(["Table Chart", "Bar Chart"])



if signal == "Skills Analyzed Done":
  df2 = pd.read_csv(f"csv\\jobSkills_{job_title}.csv")
  # Display content based on selected tab
  if df2.empty:
    print("Empty Values")
  else:
    with tabs[0]:
      tableChart(df2)

    with tabs[1]:
      chartLeft = ""
      chartRight = ""
      selectedpoints1 = ""
      selectedpoints2 = ""
      left, right = st.columns(2)
      with left:
        chartLeft = barChart1to10(df2)
        st.plotly_chart(chartLeft, use_container_width=True)
        # selected_points1 = plotly_events(chartLeft, click_event=True, hover_event=False, select_event=False)
      with right:
        chartRight = barChart11to20(df2)
        st.plotly_chart(chartRight, use_container_width=True)
        # selected_points2 = plotly_events(chartRight, click_event=True, hover_event=False, select_event=False)

    narrow_search_job_desc = st.text_input("Search Bar Job Description: ")
    df = pd.read_csv(f"csv\\original_{job_title}.csv")
    if narrow_search_job_desc:
      df = df[df['description'].str.contains(narrow_search_job_desc, case=False, na=False)]
      st.write(f"There's ..number.. jobs found that contains {narrow_search_job_desc} as a skill found in description")
    st.dataframe(df, hide_index=True, width=1500, height=200)


    # selected_points = plotly_events(chartLeft, click_event=True, hover_event=False, select_event=False)

    # Display click event data
    # if selected_points1 or selected_points2:
    #     st.write('You clicked on point:', selected_points1)
    # else:
    #     st.write('Click on a point in the plot.')
