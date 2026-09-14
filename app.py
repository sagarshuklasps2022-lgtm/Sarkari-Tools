import io
from PIL import Image
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Sarkari Tools - Free Govt Exam Image & Sign Resizer",
    page_icon="🛠️",
    layout="wide",
)

# Website Header & Ad Space Placeholder
st.title("🛠️ Sarkari Tools")
st.markdown(
    "**100% Free Online Tools for Indian Government Job Aspirants** (GDS,"
    " SSC, UPSC, NDA, CDS, Agniveer, Banking & More)"
)
st.write("---")

# Preset Options with exact standard specs
exam_preset = st.selectbox(
    "Select Exam / Application Type:",
    [
        "India Post GDS (Photo: 30-100 KB, Sign: 20-100 KB)",
        "SSC / Banking (Photo: 20-50 KB, Sign: 10-20 KB)",
        "UPSC / NDA / CDS (Photo & Sign: 20-300 KB, 350x350 px)",
        "Indian Air Force Agniveer Vayu (Photo: 10-50 KB, Sign: 10-20 KB)",
        "Custom Size",
    ],
)

# Doc Type Selection
doc_type = st.radio(
    "Select Document Type:", ["Photo", "Signature / Thumb Impression"]
)

# Set Default Dimensions & Limits based on selection
if "India Post GDS" in exam_preset:
  if "Photograph" in doc_type:
    target_width, target_height = 320, 400
    min_kb, max_kb = 30, 100
  else:
    target_width, target_height = 300, 120
    min_kb, max_kb = 20, 100

elif "SSC / Banking" in exam_preset:
  if "Photograph" in doc_type:
    target_width, target_height = 200, 230
    min_kb, max_kb = 20, 50
  else:
    target_width, target_height = 140, 60
    min_kb, max_kb = 10, 20

elif "UPSC / NDA / CDS" in exam_preset:
  target_width, target_height = 350, 350
  min_kb, max_kb = 20, 300

elif "Indian Air Force" in exam_preset:
  if "Photograph" in doc_type:
    target_width, target_height = 200, 230
    min_kb, max_kb = 10, 50
  else:
    target_width, target_height = 140, 60
    min_kb, max_kb = 10, 20

else:  # Custom Size
  col_w, col_h = st.columns(2)
  with col_w:
    target_width = st.number_input("Target Width (Pixels)", value=200)
  with col_h:
    target_height = st.number_input("Target Height (Pixels)", value=230)

  col_min, col_max = st.columns(2)
  with col_min:
    min_kb = st.number_input("Minimum Size (KB)", value=20)
  with col_max:
    max_kb = st.number_input("Maximum Size (KB)", value=50)

# Display Target Specifications
st.info(
    f"📌 **Target Specifications:** Size: **{min_kb} KB – {max_kb} KB** |"
    f" Dimensions: **{target_width} x {target_height} pixels**"
)

# File Uploader
uploaded_file = st.file_uploader(
    "Upload your Image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"]
)


def process_image(image, width, height, min_size_kb, max_size_kb):
  if image.mode in ("RGBA", "P"):
    image = image.convert("RGB")

  resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

  output = io.BytesIO()
  quality = 95
  step = 5

  while quality > 5:
    output.seek(0)
    output.truncate(0)
    resized_image.save(output, format="JPEG", quality=quality, optimize=True)
    size_kb = output.tell() / 1024

    if min_size_kb <= size_kb <= max_size_kb:
      break
    elif size_kb > max_size_kb:
      quality -= step
    else:
      break

  return output.getvalue(), size_kb, resized_image


if uploaded_file is not None:
  original_image = Image.open(uploaded_file)

  col1, col2 = st.columns(2)
  with col1:
    st.image(
        original_image,
        caption="Original Uploaded Image",
        use_container_width=True,
    )

  if st.button("Resize, Crop & Compress"):
    with st.spinner("Processing your file..."):
      processed_bytes, final_size_kb, final_img = process_image(
          original_image, target_width, target_height, min_kb, max_kb
      )

    with col2:
      st.image(
          final_img,
          caption=f"Processed Image ({target_width}x{target_height}px)",
          use_container_width=True,
      )

    st.success(
        f"Successfully processed! Final file size: {final_size_kb:.2f} KB"
    )

    # Download Button
    st.download_button(
        label="Download Image",
        data=processed_bytes,
        file_name="sarkari_tools_optimized.jpg",
        mime="image/jpeg",
    )

st.write("---")
st.caption(
    "© 2026 Sarkari Tools. All tools are 100% free for everyone. Built with"
    " Python.""Createad by Sagar Shukla. For any queries, contact us at"
)
#for run this website use this command in terminal: streamlit run app.py
