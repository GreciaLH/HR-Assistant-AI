import React, { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import { getJobDescriptions, createJobDescription, deleteJobDescription } from '../../utils/api';

export default function JobDescriptions() {
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    description: ''
  });

  useEffect(() => {
    fetchJobDescriptions();
  }, []);

  const fetchJobDescriptions = async () => {
    try {
      setLoading(true);
      const response = await getJobDescriptions();
      setJobDescriptions(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching job descriptions:', error);
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createJobDescription(formData);
      setFormData({
        title: '',
        company: '',
        location: '',
        description: ''
      });
      fetchJobDescriptions();
    } catch (error) {
      console.error('Error creating job description:', error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteJobDescription(id);
      fetchJobDescriptions();
    } catch (error) {
      console.error('Error deleting job description:', error);
    }
  };

  return (
    <Layout>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
        <div className="px-4 py-5 sm:px-6">
          <h1 className="text-3xl font-bold text-gray-900">Vacantes</h1>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Crear y gestionar descripciones de vacantes
          </p>
        </div>

        <div className="mt-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">Título del Puesto</label>
              <input
                type="text"
                name="title"
                id="title"
                value={formData.title}
                onChange={handleInputChange}
                required
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label htmlFor="company" className="block text-sm font-medium text-gray-700">Empresa</label>
              <input
                type="text"
                name="company"
                id="company"
                value={formData.company}
                onChange={handleInputChange}
                required
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">Ubicación</label>
              <input
                type="text"
                name="location"
                id="location"
                value={formData.location}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">Descripción</label>
              <textarea
                name="description"
                id="description"
                rows={4}
                value={formData.description}
                onChange={handleInputChange}
                required
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
              >
                Crear Vacante
              </button>
            </div>
          </form>
        </div>

        <div className="mt-8">
          <h2 className="text-xl font-semibold text-gray-800">Vacantes Existentes</h2>
          {loading ? (
            <p className="mt-4 text-gray-500">Cargando vacantes...</p>
          ) : jobDescriptions.length === 0 ? (
            <p className="mt-4 text-gray-500">No se encontraron vacantes. Crea una arriba.</p>
          ) : (
            <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
              {jobDescriptions.map((job) => (
                <div key={job.id} className="border border-gray-200 rounded-md p-4">
                  <div className="flex justify-between">
                    <h3 className="text-lg font-medium text-primary-800">{job.title}</h3>
                    <button
                      onClick={() => handleDelete(job.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Eliminar
                    </button>
                  </div>
                  <p className="text-sm text-gray-600">{job.company} • {job.location}</p>
                  <p className="mt-2 text-sm text-gray-500 line-clamp-3">{job.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}