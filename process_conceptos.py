import json

def procesar():
    with open('conceptos.json', 'r', encoding='utf-8') as f:
        conceptos = json.load(f)

    # Añadimos contexto e importancia (el por qué) a cada tarjeta
    conocimiento_conceptos = {
        'Estado': 'Porque es la base de la organización política y jurídica moderna. Sin Estado no hay soberanía ni imperio de la ley.',
        'Derecho': 'Porque establece el marco de convivencia pacífica, regulando el comportamiento social bajo amenaza de sanción coactiva.',
        'Constitución': 'Porque es la carta magna que subordina a todas las demás leyes, asegurando que el poder público no viole los derechos ciudadanos.',
        'Delito': 'Porque permite distinguir una simple infracción de una conducta grave que atenta contra bienes jurídicos fundamentales de la sociedad.',
        'Contrato': 'Porque brinda seguridad jurídica a las transacciones diarias, garantizando que los acuerdos voluntarios se cumplan o se indemnicen.',
        'Laboral': 'Porque protege la parte más débil de la relación de producción (el trabajador), equilibrando las fuerzas frente al capital.',
        'Internacional': 'Porque regula la coexistencia pacífica entre naciones soberanas y sanciona crímenes universales más allá de las fronteras.',
        'Matrimonio': 'Porque es el núcleo tradicional de la familia y genera un régimen de obligaciones personales y patrimoniales ineludibles.',
        'Sucesión': 'Porque garantiza la continuidad patrimonial y previene conflictos sobre la propiedad de los bienes tras la muerte de una persona.'
    }
    
    default_por_que = "Porque su comprensión es vital para aplicar correctamente la ley en casos prácticos y evitar errores de interpretación jurídica."

    for c in conceptos:
        termino = c.get('termino', '').lower()
        
        por_que = default_por_que
        for key, val in conocimiento_conceptos.items():
            if key.lower() in termino:
                por_que = val
                break
                
        c['por_que'] = por_que

    with open('conceptos.json', 'w', encoding='utf-8') as f:
        json.dump(conceptos, f, indent=2, ensure_ascii=False)
        
    print(f"Actualizadas {len(conceptos)} tarjetas con el 'Por qué'.")

if __name__ == '__main__':
    procesar()
