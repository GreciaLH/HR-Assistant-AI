import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Job Descriptions
export const getJobDescriptions = () => api.get('/job-descriptions');
export const getJobDescription = (id: number) => api.get(`/job-descriptions/${id}`);
export const createJobDescription = (data: any) => api.post('/job-descriptions', data);
export const updateJobDescription = (id: number, data: any) => api.put(`/job-descriptions/${id}`, data);
export const deleteJobDescription = (id: number) => api.delete(`/job-descriptions/${id}`);

// Resumes
export const getResumes = () => api.get('/resumes');
export const getResume = (id: number) => api.get(`/resumes/${id}`);
export const uploadResume = (formData: FormData) => {
  return api.post('/resumes', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
export const deleteResume = (id: number) => api.delete(`/resumes/${id}`);

// Matching
export const createMatching = (data: { job_description_id: number; resume_ids: number[] }) => 
  api.post('/matching', data);
export const getMatchingsByJob = (jobId: number) => api.get(`/matching/job/${jobId}`);
export const getMatchingsByResume = (resumeId: number) => api.get(`/matching/resume/${resumeId}`);
export const getMatching = (id: number) => api.get(`/matching/${id}`);

export default api;