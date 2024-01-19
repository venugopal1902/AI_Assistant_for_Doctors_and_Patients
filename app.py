import streamlit as st
from pathlib import Path
import google.generativeai as genai  
from api_key import api_key
st.set_page_config(page_title='VitalImage Analytics',page_icon=":robot:")

genai.configure(api_key=api_key)

generation_config = {'temperature':0.4,
                     "top_p":1,
                     "top_k":32,
                     "max_output_tokens":4096,}

# set the logo
safety_settings = [
{    
"category": "HARM_CATEGORY_HARASSMENT",
"threshold": "BLOCK_MEDIUM_AND_ABOVE" 
},
{"category":"HARM_CATEGORY_HATE_SPEECH",
"threshold" : "BLOCK_MEDIUM_AND_ABOVE",
},
{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT" ,
"threshold" :"BLOCK_MEDIUM_AND_ABOVE"
},
{"category":  "HARM_CATEGORY_DANGEROUS_CONTENT" ,
"threshold": "BLOCK_MEDIUM_AND_ABOVE"
}
]

system_prompt = """

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical diagnostic images for a reowned hospital. Your expertise is crucial in indentifying any anamalies, diseases, or health issues that may be present in  the images.

Your Responsibilities include:


1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including tests or treatements as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatmentl options or interventions.


Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined bases on provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions".
4. Your insights are invaluable in guiding clinical decisions. Please proceed with analysis , adhering to the structured approach outlined above.


Please provide me an output response with these 4 headings Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions, Important Notes.
"""

model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config = generation_config,
                              safety_settings = safety_settings)
st.title("Vital Image Analytics")

st.subheader("An Application that can help users to indentify medical images")

uploaded_file = st.file_uploader("Upload the medical image for analysis",type = ["png","jpg","jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=250,caption="Uploaded Medical Image")
submit_button = st.button("Generate the Analysis")
if submit_button:
    image_data = uploaded_file.getvalue()
    image_parts = [ 
        { 
            "mime_type": "image/png",
            "data": image_data

         } ,
    ]
    prompt_parts = [
        image_parts[0],
        system_prompt,
    ]
    response = model.generate_content(prompt_parts)
    if response:
        st.title("Here is the analysis based on your image")

        st.write(response.text)

