import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import engine
from sqlalchemy import text
import json

def view_resume_details():
    with engine.connect() as connection:
        # Ejecutar consulta SQL para obtener todos los currículums
        result = connection.execute(text("SELECT * FROM resumes"))
        
        # Mostrar resultados detallados
        print("\n=== DETALLES COMPLETOS DE CURRÍCULUMS ===\n")
        
        resumes = result.fetchall()
        if not resumes:
            print("No hay currículums guardados en la base de datos.")
            return
            
        for row in resumes:
            print(f"{'='*50}")
            print(f"ID: {row.id}")
            print(f"Nombre del Candidato: {row.candidate_name}")
            print(f"Email: {row.email}")
            print(f"Teléfono: {row.phone}")
            print(f"Ruta del Archivo: {row.file_path}")
            
            # Mostrar habilidades
            print("\nHABILIDADES:")
            if row.skills:
                try:
                    skills = json.loads(row.skills)
                    if isinstance(skills, list) and skills:
                        for skill in skills:
                            print(f"  • {skill}")
                    else:
                        print("  No se encontraron habilidades estructuradas")
                except json.JSONDecodeError:
                    print(f"  Error al decodificar JSON: {row.skills}")
            else:
                print("  No hay información de habilidades")
            
            # Mostrar experiencia
            print("\nEXPERIENCIA:")
            if row.experience:
                try:
                    experience = json.loads(row.experience)
                    if isinstance(experience, list) and experience:
                        for exp in experience:
                            print(f"  • {exp.get('title', 'Sin título')} en {exp.get('company', 'Sin empresa')}")
                            if 'duration' in exp:
                                print(f"    Duración: {exp['duration']}")
                            if 'description' in exp:
                                print(f"    Descripción: {exp['description']}")
                    else:
                        print("  No se encontró experiencia estructurada")
                except json.JSONDecodeError:
                    print(f"  Error al decodificar JSON: {row.experience}")
            else:
                print("  No hay información de experiencia")
            
            # Mostrar educación
            print("\nEDUCACIÓN:")
            if row.education:
                try:
                    education = json.loads(row.education)
                    if isinstance(education, list) and education:
                        for edu in education:
                            print(f"  • {edu.get('degree', 'Sin grado')} en {edu.get('institution', 'Sin institución')}")
                            if 'year' in edu:
                                print(f"    Año: {edu['year']}")
                    else:
                        print("  No se encontró educación estructurada")
                except json.JSONDecodeError:
                    print(f"  Error al decodificar JSON: {row.education}")
            else:
                print("  No hay información de educación")
            
            # Mostrar contenido (primeros 200 caracteres)
            print("\nEXTRACTO DEL CONTENIDO:")
            if row.content:
                print(f"  {row.content[:200]}..." if len(row.content) > 200 else f"  {row.content}")
            else:
                print("  No hay contenido extraído")
                
            print(f"\nFecha de creación: {row.created_at}")
            print(f"Última actualización: {row.updated_at}")
            print(f"{'='*50}\n")

if __name__ == "__main__":
    view_resume_details()