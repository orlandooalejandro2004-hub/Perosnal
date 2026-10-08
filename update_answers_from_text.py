import json
import re

def clean_text(t):
    # Remove special chars and convert to lower
    return re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]', '', t).lower()

def run():
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        preguntas = json.load(f)
        
    with open('correct_answers.txt', 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('###')]

    qa_pairs = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('**') and lines[i].endswith('**'):
            q = lines[i][2:-2].strip()
            if i + 1 < len(lines) and not lines[i+1].startswith('**'):
                a = lines[i+1].strip()
                qa_pairs.append((q, a))
                i += 2
            else:
                i += 1
        else:
            i += 1

    corrections = 0
    not_found = []

    for p in preguntas:
        p_q_clean = clean_text(p['pregunta'])
        
        # Find matching question in qa_pairs
        matched_a = None
        for (q, a) in qa_pairs:
            q_clean = clean_text(q)
            if q_clean in p_q_clean or p_q_clean in q_clean:
                matched_a = a
                break
                
        if matched_a:
            a_clean = clean_text(matched_a)
            # Find the best option
            best_idx = p['respuesta_correcta']
            for idx, opt in enumerate(p['opciones']):
                opt_clean = clean_text(opt)
                if a_clean in opt_clean or opt_clean in a_clean:
                    if best_idx != idx:
                        p['respuesta_correcta'] = idx
                        corrections += 1
                    break

    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(preguntas, f, indent=2, ensure_ascii=False)

    print(f"Hecho. Se procesaron {len(qa_pairs)} pares de Q&A.")
    print(f"Se corrigieron {corrections} respuestas.")

if __name__ == '__main__':
    run()
