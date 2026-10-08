import streamlit as st
import json
import os
import random
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="Theaai Study Premium", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

# CSS para imitar la interfaz de la captura (Theaai) y arreglar los bugs visuales
st.markdown("""
<style>
    /* Ocultar elementos nativos de Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Configuración principal (Fondo blanco/gris muy claro) */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Ajustar el padding principal */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 6rem !important;
        max-width: 800px !important;
    }
    
    /* Top Bar (Nivel, Corona, etc) */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #E2E8F0;
        padding: 8px 15px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .top-bar-text {
        font-size: 0.9rem;
        font-weight: 600;
        color: #475569;
    }
    .top-bar-icons {
        font-size: 1.2rem;
    }

    /* Buscador o Caja superior blanca */
    .search-box {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        margin-bottom: 15px;
        color: #64748B;
        font-weight: 500;
        cursor: pointer;
    }
    
    /* Kit de Estudio (Carta Azul) */
    .kit-card {
        background: linear-gradient(135deg, #007AFF, #005CE6);
        border-radius: 20px;
        padding: 30px 20px;
        color: white;
        box-shadow: 0 10px 20px rgba(0, 122, 255, 0.25);
        position: relative;
        overflow: hidden;
        margin-bottom: 20px;
        min-height: 150px;
        display: flex;
        align-items: center;
    }
    .kit-card h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
        z-index: 2;
        position: relative;
        max-width: 80%;
    }
    .kit-card .icon-bg {
        position: absolute;
        right: 10px;
        bottom: -10px;
        font-size: 5rem;
        opacity: 0.2;
        z-index: 1;
    }

    /* Pregunta en Simulador */
    .question-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 20px;
        line-height: 1.4;
    }

    /* Estilo Moodle para Preguntas y Opciones */
    .moodle-box {
        background-color: #D6E0DD; /* Verde grisáceo exacto de Moodle */
        padding: 25px 25px 35px 25px; /* Amplio padding abajo para evitar solapamiento */
        border-radius: 8px 8px 0 0;
        border: 1px solid #BFCBC7;
        border-bottom: none;
        font-size: 1.15rem;
        font-weight: 500;
        color: #1A202C;
        margin-bottom: -1.5rem; /* Anula el gap por defecto de Streamlit */
    }
    
    div[data-testid="stRadio"] {
        background-color: #D6E0DD;
        padding: 0px 25px 25px 25px;
        border-radius: 0 0 8px 8px;
        border: 1px solid #BFCBC7;
        border-top: none;
        position: relative;
        z-index: 2;
        width: 100% !important;
        display: block !important;
    }
    
    div[data-testid="stRadio"] > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }
    
    div[role="radiogroup"] p {
        color: #212529 !important;
        font-weight: 400 !important;
        font-size: 1rem !important;
        margin-left: 5px;
    }
    
    /* Explicaciones */
    .explanation-box {
        background-color: white;
        border-left: 4px solid #10B981; /* Verde éxito */
        padding: 15px;
        border-radius: 0 15px 15px 0;
        margin-top: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        font-size: 0.95rem;
        color: #334155;
    }
    .explanation-box.error {
        border-left-color: #EF4444; /* Rojo error */
    }

    /* Flashcards */
    .flashcard {
        background-color: white;
        border-radius: 20px;
        padding: 40px 20px;
        min-height: 350px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border: 2px solid transparent;
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    .flashcard-flipped {
        border-color: #007AFF;
        background-color: #F8FAFC;
    }
    .flashcard h2 {
        color: #1E293B;
        font-size: 1.3rem;
        font-weight: 600;
    }

    /* Botones estilo Moodle (verde oscuro) */
    .stButton>button {
        border-radius: 6px !important;
        font-weight: normal !important;
        background-color: #0E271D !important;
        color: white !important;
        border: none !important;
        padding: 8px 24px !important;
    }

</style>
""", unsafe_allow_html=True)

def cargar_datos():
    dir_path = os.path.dirname(__file__)
    try:
        with open(os.path.join(dir_path, 'preguntas.json'), 'r', encoding='utf-8') as f:
            preguntas = json.load(f)
    except Exception:
        preguntas = []
        
    try:
        with open(os.path.join(dir_path, 'conceptos.json'), 'r', encoding='utf-8') as f:
            conceptos = json.load(f)
    except Exception:
        conceptos = []
        
    return preguntas, conceptos

def main():
    preguntas, conceptos = cargar_datos()
    
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Prueba"
        
    st.markdown('<div class="top-bar"><span class="top-bar-text">Nivel 1: 0%</span><span class="top-bar-icons">✨ 👑</span></div>', unsafe_allow_html=True)
    
    # Navegación Superior
    cols = st.columns(4)
    if cols[0].button("🏠 Home", use_container_width=True): st.session_state.current_tab = "Home"
    if cols[1].button("🎴 Tarjetas", use_container_width=True): st.session_state.current_tab = "Tarjetas"
    if cols[2].button("📝 Prueba", use_container_width=True): st.session_state.current_tab = "Prueba"
    if cols[3].button("🎲 Aleatorio", use_container_width=True): st.session_state.current_tab = "Aleatorio"
    
    st.write("---")

    if st.session_state.current_tab == "Home":
        st.markdown('<div class="search-box">✨ Crea un kit de estudio ➔</div>', unsafe_allow_html=True)
        st.markdown('<div class="search-box">🔍 Buscar...</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex; justify-content:flex-end; margin-bottom:10px;">
            <span style="background:#E2E8F0; padding:5px 10px; border-radius:10px; font-size:0.8rem; color:#475569;">☷ Sin agrupar ˅</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="kit-card">
            <h3>Cuestionario de Derecho Completo</h3>
            <span class="icon-bg">⚖️</span>
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Contiene {len(preguntas)} preguntas tipo examen y {len(conceptos)} flashcards conceptuales.")



    elif st.session_state.current_tab == "Prueba":
        if not preguntas:
            st.error("No hay preguntas cargadas en preguntas.json")
            return
            
        if 'p_sim' not in st.session_state:
            st.session_state.p_sim = preguntas.copy()
            # Opcional: random.shuffle(st.session_state.p_sim)
            st.session_state.pregunta_actual = 0
            st.session_state.respondido = False
            
        idx = st.session_state.pregunta_actual
        p_sim = st.session_state.p_sim
        
        if idx >= len(p_sim):
            st.success("¡Has completado toda la prueba!")
            if st.button("Volver a empezar"):
                st.session_state.pregunta_actual = 0
                st.session_state.respondido = False
                st.rerun()
        else:
            p = p_sim[idx]
            
            st.markdown(f'''
            <div class="moodle-box">
                {p["pregunta"]}
            </div>
            ''', unsafe_allow_html=True)
            
            opcion_elegida = st.radio(" ", options=range(len(p['opciones'])), format_func=lambda i: f"{chr(97+i)}.   {re.sub(r'^[a-dA-D]\.\s*', '', p['opciones'][i].strip())}", label_visibility="collapsed", index=None, key=f"radio_{idx}")

            if opcion_elegida is not None:
                st.session_state.respondido = True
                es_correcta = (opcion_elegida == p['respuesta_correcta'])
                
                if es_correcta:
                    st.success("✅ ¡Excelente!")
                    components.html('<script>navigator.vibrate(100);</script><audio autoplay><source src="https://actions.google.com/sounds/v1/ui/bell_ding.ogg" type="audio/ogg"></audio>', height=0)
                else:
                    st.error("❌ Respuesta Incorrecta")
                    components.html('<script>navigator.vibrate([100, 50, 100]);</script><audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>', height=0)
                    
                explicacion = p.get('explicacion', "Revisa los apuntes legales correspondientes a este tema.")
                
                clase_css = "explanation-box" if es_correcta else "explanation-box error"
                st.markdown(f'''
                <div class="{clase_css}">
                    {explicacion}
                </div>
                ''', unsafe_allow_html=True)
                
                if not es_correcta:
                    st.markdown(f'''
                    <div class="explanation-box" style="margin-top:10px; border-left-color:#007AFF; background-color:#F0F7FF;">
                        <b>La respuesta correcta era:</b> {p['opciones'][p['respuesta_correcta']]}
                    </div>
                    ''', unsafe_allow_html=True)

                st.write("") # Espacio
                colA, colB, colC = st.columns([1,1,1])
                if colC.button("Siguiente página", use_container_width=True):
                    st.session_state.pregunta_actual += 1
                    st.session_state.respondido = False
                    st.rerun()

    elif st.session_state.current_tab == "Aleatorio":
        if not preguntas:
            st.error("No hay preguntas cargadas en preguntas.json")
            return
            
        if not st.session_state.get('aleatorio_configurado', False):
            st.markdown('<div class="question-title">Configuración de Práctica</div>', unsafe_allow_html=True)
            
            st.markdown("<p style='color:#475569; font-size:0.95rem; margin-bottom:10px;'>Crea una sesión de estudio personalizada según tus necesidades.</p>", unsafe_allow_html=True)
            
            num_q = st.number_input("¿Cuántas preguntas quieres estudiar?", min_value=1, max_value=len(preguntas), value=min(50, len(preguntas)))
            modo = st.radio("Modo de selección:", ["De manera aleatoria", "Seguida (orden original)"])
            
            start_idx = 1
            if modo == "Seguida (orden original)":
                start_idx = st.number_input(f"¿Desde qué pregunta empezar? (1 a {len(preguntas)})", min_value=1, max_value=len(preguntas), value=1)
                # Ajustamos num_q si se pasa del límite al elegir seguida
                if start_idx - 1 + num_q > len(preguntas):
                    num_q = len(preguntas) - start_idx + 1
                    st.warning(f"Solo hay {num_q} preguntas disponibles desde esa posición.")
            
            if st.button("Empezar a Estudiar", use_container_width=True):
                if modo == "De manera aleatoria":
                    st.session_state.p_aleatorio = random.sample(preguntas, num_q)
                else:
                    st.session_state.p_aleatorio = preguntas[start_idx-1 : start_idx-1 + num_q]
                
                st.session_state.aleatorio_actual = 0
                st.session_state.aleatorio_respondido = False
                st.session_state.aleatorio_configurado = True
                st.rerun()
        else:
            idx = st.session_state.aleatorio_actual
            p_sim = st.session_state.p_aleatorio
            
            if idx >= len(p_sim):
                st.success("¡Has completado esta sesión de estudio!")
                if st.button("Configurar nueva sesión"):
                    st.session_state.aleatorio_configurado = False
                    st.rerun()
            else:
                p = p_sim[idx]
                
                st.markdown(f'''
                <div class="moodle-box">
                    {p["pregunta"]}
                </div>
                ''', unsafe_allow_html=True)
                
                opcion_elegida = st.radio(" ", options=range(len(p['opciones'])), format_func=lambda i: f"{chr(97+i)}.   {re.sub(r'^[a-dA-D]\.\s*', '', p['opciones'][i].strip())}", label_visibility="collapsed", index=None, key=f"radio_al_{idx}")

                if opcion_elegida is not None:
                    st.session_state.aleatorio_respondido = True
                    es_correcta = (opcion_elegida == p['respuesta_correcta'])
                    
                    if es_correcta:
                        st.success("✅ ¡Excelente!")
                        components.html('<script>navigator.vibrate(100);</script><audio autoplay><source src="https://actions.google.com/sounds/v1/ui/bell_ding.ogg" type="audio/ogg"></audio>', height=0)
                    else:
                        st.error("❌ Respuesta Incorrecta")
                        components.html('<script>navigator.vibrate([100, 50, 100]);</script><audio autoplay><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>', height=0)
                        
                    explicacion = p.get('explicacion', "Revisa los apuntes legales correspondientes a este tema.")
                    
                    clase_css = "explanation-box" if es_correcta else "explanation-box error"
                    st.markdown(f'''
                    <div class="{clase_css}">
                        {explicacion}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    if not es_correcta:
                        st.markdown(f'''
                        <div class="explanation-box" style="margin-top:10px; border-left-color:#007AFF; background-color:#F0F7FF;">
                            <b>La respuesta correcta era:</b> {p['opciones'][p['respuesta_correcta']]}
                        </div>
                        ''', unsafe_allow_html=True)

                    st.write("") # Espacio
                    colA, colB, colC = st.columns([1,1,1])
                    if colC.button("Siguiente página", use_container_width=True):
                        st.session_state.aleatorio_actual += 1
                        st.session_state.aleatorio_respondido = False
                        st.rerun()
                        
                st.write("---")
                if st.button("Terminar sesión tempranamente", key=f"end_early_{idx}"):
                    st.session_state.aleatorio_configurado = False
                    st.rerun()

    elif st.session_state.current_tab == "Tarjetas":
        if not conceptos:
            st.error("No hay conceptos cargados en conceptos.json")
            return
            
        if 'flashcard_idx' not in st.session_state:
            st.session_state.flashcard_idx = 0
            st.session_state.volteada = False
            
        f_idx = st.session_state.flashcard_idx
        c_flash = conceptos[f_idx]
        
        st.markdown("<p style='text-align:center; color:#64748B;'>Piensa en el concepto y toca Voltear Carta para verificar tu conocimiento.</p>", unsafe_allow_html=True)

        if not st.session_state.volteada:
            st.markdown(f'''
            <div class="flashcard">
                <span style="color:#007AFF; font-size:0.9rem; font-weight:bold; margin-bottom:15px; text-transform:uppercase;">Concepto Jurídico</span>
                <h2>{c_flash["termino"]}</h2>
            </div>
            ''', unsafe_allow_html=True)
        else:
            por_que_html = f"""<div style="background:#E0F2FE; border-left:4px solid #0EA5E9; padding:15px; border-radius:10px; margin-top:15px; font-size:0.95rem; color:#0369A1; text-align:left;">
<b style="color:#0284C7;">🔍 ¿Por qué es importante?</b><br>
{c_flash.get('por_que', 'Concepto base para el análisis jurídico.')}
</div>"""
            
            st.markdown(f'''
            <div class="flashcard flashcard-flipped">
                <span style="font-size:0.9rem; color:#64748B; margin-bottom:15px; text-transform:uppercase; letter-spacing:1px;">{c_flash["termino"]}</span>
                <div style="background:#F1F5F9; padding:20px; border-radius:15px; margin-top:10px; font-size:1.05rem; color:#1E293B; text-align:left; line-height:1.5;">
                    💡 <b>Definición:</b> {c_flash["definicion"]}
                </div>
                {por_que_html}
            </div>
            ''', unsafe_allow_html=True)
            
        cA, cB, cC = st.columns([1, 2, 1])
        if cA.button("⬅️", use_container_width=True, disabled=(f_idx == 0)):
            st.session_state.flashcard_idx -= 1
            st.session_state.volteada = False
            st.rerun()
            
        if cB.button("🔄 Voltear Carta", use_container_width=True):
            st.session_state.volteada = not st.session_state.volteada
            st.rerun()
            
        if cC.button("➡️", use_container_width=True, disabled=(f_idx == len(conceptos)-1)):
            st.session_state.flashcard_idx += 1
            st.session_state.volteada = False
            st.rerun()
            
        st.markdown(f"<p style='text-align:center; color:#94A3B8; font-size:0.8rem; margin-top:10px;'>{f_idx + 1} / {len(conceptos)}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
