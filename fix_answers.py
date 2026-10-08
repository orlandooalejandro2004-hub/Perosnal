import json
import re

def fix_answers():
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        preguntas = json.load(f)

    # Reglas exactas o por palabras clave (si la pregunta contiene la clave, buscar una opción que contenga el valor)
    # Se debe hacer match en minúsculas.
    rules = [
        {"q_has": "tipicidad está ligada", "a_has": "legalidad"},
        {"q_has": "derecho penal y el derecho constitucional", "a_has": "principios y garantías que rigen el ejercicio del poder punitivo"},
        {"q_has": "clasifican las personas que la ley puede declarar incapaces", "a_has": "absolutos y relativos"},
        {"q_has": "derechos de primera generación", "a_has": "libertad individual"},
        {"q_has": "modos de adquirir el dominio", "a_has": "ocupación, la accesión, la tradición"},
        {"q_has": "donación entre vivos", "a_has": "acto"},
        {"q_has": "Cabanellas la cosa", "a_has": "todo lo existente, de manera corporal"},
        {"q_has": "manipulación genética", "a_has": "prevenir o combatir una enfermedad"},
        {"q_has": "carácter coactivo de poder", "a_has": "monopolio de la fuerza"},
        {"q_has": "carga probatoria para demostrar que no fue despedido", "a_has": "empleador"},
        {"q_has": "realismo", "a_has": "supervivencia, seguridad o poder"},
        {"q_has": "13era. 14ta. remuneración", "a_has": "empleador"},
        {"q_has": "facultad de testar", "a_has": "indelegable"},
        {"q_has": "derecho penal objetivo", "a_has": "conjunto de normas"},
        {"q_has": "delitos contra la libertad personal", "a_has": "privación ilegal"},
        {"q_has": "división básica y original", "a_has": "ejecutivo, judicial y legislativo"},
        {"q_has": "estado colchón", "a_has": "débil situado entre dos"},
        {"q_has": "personas naturales y las personas jurídicas", "a_has": "seres humanos, mientras que las personas jurídicas son colectividades"},
        {"q_has": "artículo 51", "a_has": "legítima defensa"},
        {"q_has": "preámbulos constitucionales", "a_has": "declarativas"},
        {"q_has": "principio de ¨distinción¨", "a_has": "objetivos militares y no población civil"},
        {"q_has": "mártires de chicago", "a_has": "spies"},
        {"q_has": "supremacía constitucional", "a_has": "formal y material"},
        {"q_has": "proceso necesario para que una ley", "a_has": "registro oficial"},
        {"q_has": "estado ecuatoriano debe acatar", "a_has": "es estado parte"},
        {"q_has": "corte penal internacional", "a_has": "genocidio"},
        {"q_has": "rebelión", "a_has": "seguridad pública"},
        {"q_has": "in dubio pro reo", "a_has": "menos rigurosa"},
        {"q_has": "sucesión por causa de muerte", "a_has": "adquirir el dominio"},
        {"q_has": "hurto y robo", "a_has": "violencia"},
        {"q_has": "jus puniendi", "a_has": "sanciones penales"},
        {"q_has": "órgano facultado para emitir pronunciamientos", "a_has": "corte constitucional"}
    ]

    corrections_made = 0

    for p in preguntas:
        q_text = p['pregunta'].lower()
        
        # Primero evaluamos las reglas estrictas de la base de conocimiento manual
        rule_applied = False
        for rule in rules:
            if rule['q_has'].lower() in q_text:
                # buscar la opción
                for idx, opt in enumerate(p['opciones']):
                    if rule['a_has'].lower() in opt.lower():
                        if p['respuesta_correcta'] != idx:
                            p['respuesta_correcta'] = idx
                            corrections_made += 1
                        rule_applied = True
                        break
            if rule_applied:
                break
                
        # Si no aplicó regla estricta, reevaluamos por si la heurística vieja de "la más larga" fue tonta.
        if not rule_applied:
            # Una heurística mejor en derecho:
            # 1. 'Todas las anteriores'
            # 2. Evitar respuestas absurdamente cortas si no hacen sentido, 
            # pero aquí no podemos saber sin un modelo de lenguaje.
            # Al menos dejaremos la que estaba, pero ya arreglamos las más críticas de la lista.
            pass

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(preguntas, f, indent=2, ensure_ascii=False)

    print(f"Hecho. Se han corregido {corrections_made} respuestas que la heurística anterior falló.")

if __name__ == '__main__':
    fix_answers()
