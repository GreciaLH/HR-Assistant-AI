import React, { useState, useEffect } from 'react';
import Layout from '../../components/Layout';
import { getJobDescriptions, getResumes, createMatching, getMatchingsByJob } from '../../utils/api';

export default function Matching() {
  const [jobDescriptions, setJobDescriptions] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [selectedResumes, setSelectedResumes] = useState([]);
  const [matchings, setMatchings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [matchingLoading, setMatchingLoading] = useState(false);
  const [matchingResults, setMatchingResults] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [jobResponse, resumeResponse] = await Promise.all([
        getJobDescriptions(),
        getResumes()
      ]);
      setJobDescriptions(jobResponse.data);
      setResumes(resumeResponse.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const handleJobChange = (e) => {
    setSelectedJob(e.target.value);
    setMatchingResults(false);
  };

  const handleResumeToggle = (resumeId) => {
    setSelectedResumes(prev => {
      if (prev.includes(resumeId)) {
        return prev.filter(id => id !== resumeId);
      } else {
        return [...prev, resumeId];
      }
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedJob || selectedResumes.length === 0) {
      alert('Please select a job and at least one resume');
      return;
    }

    try {
      setMatchingLoading(true);
      await createMatching({
        job_description_id: parseInt(selectedJob),
        resume_ids: selectedResumes.map(id => parseInt(id))
      });
      
      const response = await getMatchingsByJob(parseInt(selectedJob));
      setMatchings(response.data);
      setMatchingResults(true);
      setMatchingLoading(false);
    } catch (error) {
      console.error('Error creating matching:', error);
      setMatchingLoading(false);
    }
  };

  return (
    <Layout>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg p-6">
        <div className="px-4 py-5 sm:px-6">
          <h1 className="text-3xl font-bold text-gray-900">Coincidencias</h1>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Encuentra coincidencias entre vacantes y currículums de candidatos
          </p>
        </div>

        {loading ? (
          <p className="mt-4 text-gray-500">Cargando datos...</p>
        ) : (
          <div className="mt-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="job" className="block text-sm font-medium text-gray-700">Seleccionar Vacante</label>
                <select
                  id="job"
                  value={selectedJob}
                  onChange={handleJobChange}
                  className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
                >
                  <option value="">Selecciona una vacante</option>
                  {jobDescriptions.map(job => (
                    <option key={job.id} value={job.id}>{job.title} - {job.company}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Seleccionar Currículums para Comparar</label>
                <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-2">
                  {resumes.length === 0 ? (
                    <p className="text-gray-500">No hay currículums disponibles. Por favor, sube currículums primero.</p>
                  ) : (
                    resumes.map(resume => (
                      <div key={resume.id} className="relative flex items-start">
                        <div className="flex items-center h-5">
                          <input
                            id={`resume-${resume.id}`}
                            type="checkbox"
                            checked={selectedResumes.includes(resume.id)}
                            onChange={() => handleResumeToggle(resume.id)}
                            className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          />
                        </div>
                        <div className="ml-3 text-sm">
                          <label htmlFor={`resume-${resume.id}`} className="font-medium text-gray-700">
                            {resume.candidate_name}
                          </label>
                          {resume.email && <p className="text-gray-500">{resume.email}</p>}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  disabled={!selectedJob || selectedResumes.length === 0 || matchingLoading}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  {matchingLoading ? 'Procesando...' : 'Comparar Currículums'}
                </button>
              </div>
            </form>
          </div>
        )}

        {matchingResults && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-800">Resultados de Coincidencias</h2>
            {matchings.length === 0 ? (
              <p className="mt-4 text-gray-500">No se encontraron resultados de coincidencias.</p>
            ) : (
              <div className="mt-4 overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                <table className="min-w-full divide-y divide-gray-300">
                  <thead className="bg-gray-50">
                    <tr>
                      <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Candidato</th>
                      <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Puntuación</th>
                      <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Comentarios</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 bg-white">
                    {matchings
                      .sort((a, b) => b.score - a.score)
                      .map(match => (
                        <tr key={match.id}>
                          <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">
                            {resumes.find(r => r.id === match.resume_id)?.candidate_name || 'Desconocido'}
                          </td>
                          <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              match.score >= 80 ? 'bg-green-100 text-green-800' :
                              match.score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {match.score.toFixed(1)}%
                            </span>
                          </td>
                          <td className="px-3 py-4 text-sm text-gray-500">
                            {match.comments}
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
}