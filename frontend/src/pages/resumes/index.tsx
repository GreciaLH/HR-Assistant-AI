import React, { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import { getResumes, uploadResume, deleteResume } from '../../utils/api';
import { useDropzone } from 'react-dropzone';

export default function Resumes() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    onDrop: acceptedFiles => {
      handleFileUpload(acceptedFiles[0]);
    }
  });

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      setLoading(true);
      const response = await getResumes();
      setResumes(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching resumes:', error);
      setLoading(false);
    }
  };

  const handleFileUpload = async (file) => {
    try {
      setUploading(true);
      const data = new FormData();
      data.append('file', file);
      // El backend extraerá automáticamente el nombre del candidato y otros datos del archivo

      await uploadResume(data);
      fetchResumes();
      setUploading(false);
    } catch (error) {
      console.error('Error uploading resume:', error);
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteResume(id);
      fetchResumes();
    } catch (error) {
      console.error('Error deleting resume:', error);
    }
  };

  return (
    <Layout>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
        <div className="px-4 py-5 sm:px-6">
          <h1 className="text-3xl font-bold text-gray-900">Currículums</h1>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
          Subir y gestionar currículums de candidatos
          </p>
        </div>

        <div className="mt-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Cargar currículum (PDF o DOCX)</label>
            <div 
              {...getRootProps()} 
              className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md cursor-pointer hover:bg-gray-50"
            >
              <div className="space-y-1 text-center">
                <svg
                  className="mx-auto h-12 w-12 text-gray-400"
                  stroke="currentColor"
                  fill="none"
                  viewBox="0 0 48 48"
                  aria-hidden="true"
                >
                  <path
                    d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                    strokeWidth={2}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <div className="flex text-sm text-gray-600">
                  <input {...getInputProps()} />
                  <p>Arrastre y suelte un archivo aquí o haga clic para seleccionar un archivo</p>
                </div>
                <p className="text-xs text-gray-500">PDF o DOCX hasta 10MB</p>
                <p className="text-xs text-gray-500 font-medium">Toda la información del candidato se extraerá automáticamente del archivo.</p>
              </div>
            </div>
          </div>
          {uploading && <p className="mt-2 text-sm text-gray-500">Subiendo archivo...</p>}
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-semibold text-gray-800">CVs subidos</h2>
          {loading ? (
            <p className="mt-4 text-gray-500">Cargando currículums...</p>
          ) : resumes.length === 0 ? (
            <p className="mt-4 text-gray-500">No hay currículums encontrados. Sube uno arriba..</p>
          ) : (
            <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
              {resumes.map((resume) => (
                <div key={resume.id} className="border border-gray-200 rounded-md p-4">
                  <div className="flex justify-between">
                    <h3 className="text-lg font-medium text-primary-800">{resume.candidate_name}</h3>
                    <button
                      onClick={() => handleDelete(resume.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Eliminar
                    </button>
                  </div>
                  {resume.email && <p className="text-sm text-gray-600">Email: {resume.email}</p>}
                  {resume.phone && <p className="text-sm text-gray-600">Teléfono: {resume.phone}</p>}
                  <div className="mt-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Currículum subido
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}