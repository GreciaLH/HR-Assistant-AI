import React from 'react';
import Layout from '../components/Layout';
import Link from 'next/link';

export default function Home() {
  return (
    <Layout>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
        <div className="px-4 py-5 sm:px-6">
          <h1 className="text-3xl font-bold text-gray-900">IA Recruiter</h1>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Herramienta impulsada por IA para encontrar coincidencias entre vacantes y currículums
          </p>
        </div>
        
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div className="bg-primary-50 overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg font-medium text-primary-800">Vacantes</h3>
              <p className="mt-2 text-sm text-gray-500">
                Gestiona descripciones de vacantes y extrae requisitos y habilidades clave.
              </p>
              <div className="mt-4">
                <Link href="/job-descriptions" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700">
                  Ver Vacantes
                </Link>
              </div>
            </div>
          </div>
          
          <div className="bg-primary-50 overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg font-medium text-primary-800">Currículums</h3>
              <p className="mt-2 text-sm text-gray-500">
                Sube y gestiona currículums de candidatos con extracción de datos impulsada por IA.
              </p>
              <div className="mt-4">
                <Link href="/resumes" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700">
                  Ver Currículums
                </Link>
              </div>
            </div>
          </div>
          
          <div className="bg-primary-50 overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg font-medium text-primary-800">Coincidencias</h3>
              <p className="mt-2 text-sm text-gray-500">
                Compara vacantes con currículums de candidatos y obtén clasificaciones impulsadas por IA.
              </p>
              <div className="mt-4">
                <Link href="/matching" className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700">
                  Iniciar Coincidencias
                </Link>
              </div>
            </div>
          </div>
        </div>
        
        <div className="mt-8 bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-800">Cómo Funciona</h2>
          <ol className="mt-4 space-y-4 text-gray-600">
            <li className="flex">
              <span className="flex-shrink-0 h-6 w-6 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-medium">1</span>
              <span className="ml-3">Sube o crea descripciones de vacantes para extraer requisitos y habilidades clave.</span>
            </li>
            <li className="flex">
              <span className="flex-shrink-0 h-6 w-6 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-medium">2</span>
              <span className="ml-3">Sube currículums de candidatos (PDF o DOCX) para extraer su experiencia, habilidades y educación.</span>
            </li>
            <li className="flex">
              <span className="flex-shrink-0 h-6 w-6 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-medium">3</span>
              <span className="ml-3">Utiliza la función de coincidencias para comparar descripciones de vacantes con currículums de candidatos.</span>
            </li>
            <li className="flex">
              <span className="flex-shrink-0 h-6 w-6 rounded-full bg-primary-600 text-white flex items-center justify-center text-sm font-medium">4</span>
              <span className="ml-3">Obtén clasificaciones, puntuaciones y análisis detallados impulsados por IA para cada candidato.</span>
            </li>
          </ol>
        </div>
      </div>
    </Layout>
  );
}