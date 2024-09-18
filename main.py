import streamlit as st
from skimage import io
from PIL import Image # Necessary for handling image file conversions
import numpy as np
import matplotlib.pyplot as plt

# Name
st.title("Picture Compressor in Streamlit")

# Description
st.write(" Download your picture which you want to compress")



# Step 1: DOwnload picture 
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width = True)

    image_np = np.array(image)
    if image_np.ndim ==3:
     single_channel = image_np[:,:,0]
    else:
       single_channel= image_np
    # Displaying the single channel image
    single_channel_image = Image.fromarray(single_channel)
    st.image(single_channel_image, caption= "Single Chanel Image", use_column_width=True)

    #Step 2: set k value
    top_k = st.slider("Set the scale of compression")
    factor = max(1,top_k)

#Step 3: Decrease resolution of the picture 
    U, sing_values, V = np.linalg.svd(single_channel)
    tranc_U = U[:, :top_k]
    sigma = np.zeros(shape=single_channel.shape)
    np.fill_diagonal(sigma, sing_values)
    tranc_sigma = sigma[:top_k, :top_k]
    tranc_V = V[:top_k, :]
    new_image = tranc_U@tranc_sigma@tranc_V

    fig, ax = plt.subplots(1, 2, figsize=(15, 10))

    ax[0].imshow(single_channel, cmap="grey")
    ax[0].set_title("Orifginal Single Channel")
    ax[1].imshow(new_image, cmap="grey")
    ax[1].set_title("Picture with decresed resolution")
    st.pyplot(fig)



#Step4: Demonstrate pic with lower resolution