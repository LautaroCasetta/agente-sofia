import os
import json
from datetime import datetime
import streamlit as st
from xhtml2pdf import pisa
import re
import emoji
import pytz

# Configuración de la página
PRIMARY_COLOR = "#4b83c0"
SECONDARY_COLOR = "#878889"
BACKGROUND_COLOR = "#ffffff"  # White background
ICOMEX_LOGO_PATH = "logos/ICOMEX_Logos sin fondo.png"
SOFIA_AVATAR_PATH = "logos/sofia_avatar.png"

# Function to load instructions
def load_instructions(topic):
    INSTRUCTIONS_FILES = {
        "Oportunidades de Inversión": "instructions_inversiones.txt",
        "Exportación de Servicios": "instructions_comercio_exterior.txt",
    }
    try:
        with open(INSTRUCTIONS_FILES[topic], "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        st.error(f"No se encontró el archivo de instrucciones para {topic}.")
        return None

# Clean message for PDF output
def clean_message(message_content):
    # Remove Markdown bold (**text** -> text)
    message_content = re.sub(r"\*\*(.*?)\*\*", r"\1", message_content)
    # Remove emojis
    message_content = emoji.replace_emoji(message_content, replace="")
    # Remove all "#" characters
    message_content = message_content.replace("#", "")
    # Replace line breaks with <br>
    message_content = message_content.replace("\n", "<br>")
    return message_content

# Generate PDF
def generate_pdf(html_content, output_path):
    with open(output_path, "w+b") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if pisa_status.err:
            return False, pisa_status.err
    return True, None

# Save conversation form
def save_conversation_form():
    with st.sidebar.form("guardar_conversacion"):
        st.write("Complete el formulario (se enviará esta conversación a su correo):")
        name = st.text_input("Nombre")
        last_name = st.text_input("Apellido")
        email = st.text_input("Correo electrónico")
        submitted = st.form_submit_button("Guardar y programar envío")

        if submitted:
            if name and last_name and email:
                # Filter messages
                filtered_messages = [
                    msg for msg in st.session_state.messages if msg["role"] != "system"
                ]
                # Create data to save
                conversation_data = {
                    "name": name,
                    "last_name": last_name,
                    "email": email,
                    "topic": st.session_state.selected_topic,
                    "messages": filtered_messages,
                }
                # Create folder if not exists
                folder = "./conversaciones/comercio_exterior" if st.session_state.selected_topic == "Exportación de Servicios" else "./conversaciones/inversiones"
                os.makedirs(folder, exist_ok=True)

                # Create file name with date and time
                argentina_time = datetime.now(pytz.timezone('America/Argentina/Buenos_Aires'))
                date_str = argentina_time.strftime("%Y%m%d%H%M")
                filename = f"{date_str}_{last_name.upper()}_{name.upper()}"
                json_filepath = os.path.join(folder, f"{filename}.json")
                pdf_filepath = os.path.join(folder, f"{filename}.pdf")

                # Save JSON file
                with open(json_filepath, "w", encoding="utf-8") as f:
                    json.dump(conversation_data, f, ensure_ascii=False, indent=4)

                # Create HTML content for PDF
                html_content = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            background-color: {BACKGROUND_COLOR};
                            margin: 0;
                            padding: 0;
                            font-size: 120%;
                        }}

                        .logos-container {{
                            width: 100%;
                            text-align: center;
                            margin: 20px 0;
                        }}
                        .logos-container table {{
                            margin: 0 auto; /* Center the table horizontally */
                            border-collapse: collapse;
                        }}
                        .logos-container img {{
                            height: 60px; /* Fixed height */
                            max-width: 150px; /* Restrict width to avoid stretching */
                            margin: 0 10px; /* Spacing between logos */
                            object-fit: contain; /* Maintain aspect ratio */
                        }}
    
                        .title-container h1 {{
                            color: {PRIMARY_COLOR};
                            font-size: 1.2rem; /* Tamaño de fuente más pequeño */
                            margin-top: 20px;
                            margin-bottom: 20px;
                            font-weight: bold;
                        }}
                       
                        .title-container {{
                            text-align: center;
                            color: {PRIMARY_COLOR};
                            font-size: 1.5rem;
                            margin-top: 20px;
                            margin-bottom: 20px;
                            font-weight: bold;
                        }}
                        .content {{
                            margin: 20px;
                        }}
                        .user {{
                            color: {SECONDARY_COLOR};
                            font-weight: bold;
                        }}
                        .assistant {{
                            color: {PRIMARY_COLOR};
                            font-weight: bold;
                        }}
                        .message {{
                            margin-bottom: 1em;
                        }}
                    </style>
                </head>
                <body>
                    <div class="logos-container">
                        <table>
                            <tr>
                                <td style="text-align: center; padding-left: 10px; padding-right: 10px;">
                                    <img src="{SOFIA_AVATAR_PATH}" alt="SofIA Logo">
                                    <img src="{ICOMEX_LOGO_PATH}" alt="ICOMEX Logo">
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="title-container">
                        <h1>{st.session_state.selected_topic}</h1>
                        <h1>Conversación de {name.title()} con SofIA</h1>
                    </div>
                    <div class="content">
                        <p><b>Nombre completo:</b> {name.title()} {last_name.title()}</p>
                        <p><b>Correo:</b> {email}</p>
                        <p><b>Fecha:</b> {argentina_time.strftime("%H:%M hs %d/%m/%Y")}</p>
                        <h2>Mensajes</h2>
                """
                for msg in filtered_messages:
                    role = name.title() if msg["role"] == "user" else "SofIA"
                    color_class = "user" if msg["role"] == "user" else "assistant"
                    html_content += f"<div class='message {color_class}'><b>{role}:</b> {clean_message(msg['content'])}</div>"

                html_content += "</div></body></html>"

                # Save PDF file
                success, error = generate_pdf(html_content, pdf_filepath)
                if success:
                    st.success("El envío de esta conversación se ha programado correctamente.")
                else:
                    st.error("La conversación no se ha guardado, por favor solicite ayuda al personal de I-COMEX.")

                st.session_state.show_form = False
            else:
                st.error("Por favor complete todos los campos.")