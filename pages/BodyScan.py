import streamlit as st
from utils.utitlity import load_css, predictShape
from PIL import Image
import numpy as np
import cv2
from constants import updateResult

@st.experimental_dialog("Want to proceed further ?")
def confirmaton(test_img):
    """
    This Python function takes an image as input, saves it, predicts its shape, writes the result to a
    file, and then switches to a different page if "Yes" is clicked or reruns if "No" is clicked.
    
    :param test_img: The `test_img` parameter is of type `Image`, which likely represents an image
    object that is being passed to the `confirmaton` function for further processing
    :type test_img: Image
    """
    cols = st.columns(6)
    if cols[0].button("Yes"):
        with st.status("Processing"):
            shape = predictShape(test_img)
            updateResult(shape)
        st.switch_page("pages/Result.py")
    if cols[1].button("No"):
        st.experimental_rerun()

def app(page="bodyScan"):
    st.set_page_config(page_icon="assests/MyStle-logo.png",
                       page_title="Mystyle", layout="wide", initial_sidebar_state="collapsed")
    load_css(f"style/{page}.css")

    with st.container():
        st.html("""<div id = 'main-container'></div>""")
        with st.container(border=False):
            st.html("""<div id = 'head-container'></div>""")
            cols = st.columns(2, gap="large", vertical_alignment="center")
            with cols[0]:
                sub_cols = st.columns(
                    [0.3, 1, 1, 1, 1], vertical_alignment='center')
                sub_cols[1].image("assests/MyStyle.png", width=250)
            with cols[1]:
                sub = st.columns([1, 1, 1, 0.5, 4, 1],
                                 vertical_alignment="center")
                sub[3].image("assests/search.png", width=20)
                sub[4].text_input(
                    "", label_visibility="collapsed", placeholder="search")

        with st.container(border=False, height=900):
            st.html("""<div id = 'inner-container'></div>""")
            st.html('''<h2 style="padding-left:50px">Scan the body :-</h2>''')
            cols = st.columns([1, 0.4, 0.5, 4, 1])
            cols[2].subheader("Select")
            selection = None
            with cols[3]:
                selection = st.selectbox(
                    "Use", ['Camera', 'Upload from the device'], label_visibility="collapsed", index=None)
                if selection:
                    process_image=None
                    if selection == "Camera":
                        cols=st.columns([20,200])
                        img = Image.open("assests/camera.png").resize((100, 100))
                        cols[0].image(img)
                        cam_img = st.camera_input(
                            "", label_visibility="collapsed")
                        if cam_img:
                            process_image=Image.open(cam_img)
                    elif selection == "Upload from the device":
                        st.markdown("#### Upload")
                        img = st.file_uploader("file", label_visibility="collapsed", type=[
                                               "png", "jpeg", "jpg","webp"])
                        if img:
                            img = Image.open(img).resize((400, 400))
                            st.image(img)
                            process_image=img
                        else:
                            st.header("")
                            st.header("")
                            cols=st.columns(3)
                            img = Image.open(r"assests/upload.png").resize((300, 300))
                            cols[1].image(img)
                            
                    if process_image and st.button("Examine", use_container_width=True, type="primary"):
                        test_image = cv2.cvtColor(np.array(process_image), cv2.COLOR_RGB2BGR)
                        confirmaton(test_image)

            if not selection:
                st.header("")
                st.header("")
                cols=st.columns([1.5,1,1,1,1])
                img = Image.open("assests/camera.png").resize((300, 300))
                cols[1].image(img)
                img = Image.open("assests/cross.png").resize((300, 300))
                cols[2].image(img)
                img = Image.open(r"assests/upload.png").resize((300, 300))
                cols[3].image(img)
        st.header("")


if __name__ == "__main__":
    app()
