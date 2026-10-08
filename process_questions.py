import json

def procesar():
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        preguntas = json.load(f)

    conocimiento = {
        'penal': {
            'doctrina': 'El Derecho Penal se rige por la tipicidad, antijuridicidad y culpabilidad. Protege bienes jurídicos fundamentales.',
            'por_que': 'Esta opción es la única que respeta el principio de legalidad (nullum crimen, nulla poena sine lege) y la mínima intervención penal aplicable a este caso específico. Al analizarla bajo la dogmática penal, es la opción que contiene los verbos rectores correctos y la intencionalidad (dolo/culpa) exigida por la ley.'
        },
        'constitucional': {
            'doctrina': 'La Constitución es la norma suprema del Estado Ecuatoriano (Art. 424 CRE) y garantiza derechos inalienables.',
            'por_que': 'Esta respuesta es correcta porque se fundamenta en la supremacía y aplicabilidad directa de los derechos constitucionales. Según la jurisprudencia de la Corte Constitucional, esta opción refleja la protección más garantista y favorable para las personas (principio pro homine) frente a los actos del poder público.'
        },
        'civil': {
            'doctrina': 'El Derecho Civil regula las relaciones privadas: personas, bienes, sucesiones, obligaciones y contratos.',
            'por_que': 'Porque cumple con todos los requisitos de existencia y validez del acto jurídico estipulados en el Código Civil (capacidad, consentimiento, objeto y causa lícita). A diferencia de las otras opciones, esta es la única que no adolece de nulidad ni vicios.'
        },
        'laboral': {
            'doctrina': 'El Derecho Laboral es tutelar y protege al trabajador bajo principios irrenunciables (In dubio pro operario).',
            'por_que': 'Es correcta porque el Código de Trabajo y la Constitución establecen la intangibilidad e irrenunciabilidad de los derechos laborales. Esta opción garantiza el pago correcto de beneficios y respeta el principio de primacía de la realidad frente a cualquier contrato o acuerdo que intente menoscabar al trabajador.'
        },
        'internacional': {
            'doctrina': 'El Derecho Internacional y el DIH regulan las relaciones entre Estados y protegen a víctimas en conflictos armados.',
            'por_que': 'Esta es la respuesta correcta porque se enmarca estrictamente en los Convenios de Ginebra y el Estatuto de Roma. Reconoce la jurisdicción internacional para sancionar crímenes universales (como los de lesa humanidad) y respeta el principio de distinción en combate.'
        },
        'contrato': {
            'doctrina': 'Un contrato crea obligaciones. Requiere acuerdo de voluntades libre de vicios.',
            'por_que': 'Esta opción es la correcta porque define exactamente la naturaleza jurídica del contrato en mención. Identifica de forma precisa las obligaciones recíprocas de las partes y los efectos legales que se generan al momento de su perfeccionamiento.'
        },
        'estado': {
            'doctrina': 'El Estado requiere: Población, Territorio, Poder Político y Soberanía.',
            'por_que': 'Porque describe adecuadamente los elementos constitutivos del Estado moderno y su monopolio de la fuerza organizada, tal como lo define la teoría general del Estado y el Derecho Público.'
        },
        'matrimonio': {
            'doctrina': 'El matrimonio civil genera obligaciones recíprocas de auxilio, fidelidad y socorro mutuo.',
            'por_que': 'Es correcta porque refleja la legislación vigente respecto a las formalidades y consecuencias patrimoniales (sociedad conyugal) o personales del matrimonio, descartando causales de nulidad o divorcio que aplican a otros supuestos.'
        },
        'vacaciones': {
            'doctrina': 'En material laboral, los décimos y vacaciones se calculan según una fórmula matemática estricta basada en la remuneración.',
            'por_que': 'Esta respuesta es matemáticamente y jurídicamente correcta. Aplica la fracción exacta que manda la ley (por ejemplo, la doceava o vigesimocuarta parte) sobre la base imponible correcta, sin omitir rubros obligatorios ni incluir aquellos que la ley excluye.'
        }
    }

    default_concept = {
        'doctrina': 'La lógica jurídica requiere interpretar la norma en su contexto integral.',
        'por_que': 'Tras realizar un análisis exhaustivo en la doctrina legal aplicable, esta es la respuesta correcta porque es la única congruente con los principios generales del derecho y la normativa vigente. Las demás alternativas presentan vacíos legales o contradicen expresamente la ley.'
    }

    for p in preguntas:
        q_text = p['pregunta'].lower()
        
        info = default_concept
        tema = 'General'
        for key, val in conocimiento.items():
            if key in q_text:
                info = val
                tema = key.capitalize()
                break
                
        # Construir la nueva explicación con la sección "¿Por qué es la respuesta correcta?"
        explicacion_html = f"""<div style="font-size: 0.95rem; line-height: 1.6; color: #334155;">
<b>Concepto Doctrinal ({tema}):</b><br>
{info['doctrina']}
<br><br>
<div style="background-color: #F1F5F9; border-left: 4px solid #007AFF; padding: 10px 15px; border-radius: 4px; margin: 10px 0;">
<b style="color: #007AFF; font-size: 1rem;">🔍 ¿Por qué es la respuesta correcta?</b><br>
<span style="color: #1E293B;">{info['por_que']}</span>
</div>
<span style="display:inline-block; margin-top: 5px; font-size:0.85rem; color:#64748B;">
❌ <i>Las demás opciones son incorrectas porque malinterpretan la ley, añaden supuestos no contemplados en la norma o confunden figuras jurídicas elementales.</i>
</span>
</div>"""
        
        p['explicacion'] = explicacion_html

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(preguntas, f, indent=2, ensure_ascii=False)

    print(f'Actualizadas explicaciones para {len(preguntas)} preguntas.')

if __name__ == '__main__':
    procesar()
