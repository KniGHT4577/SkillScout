import { apiClient } from './client';

export const getOpportunities = async (params: any) => {
  const response = await apiClient.get('/opportunities/', { params });
  return response.data;
};

export const getBookmarks = async () => {
  const response = await apiClient.get('/bookmarks/');
  return response.data;
};

export const createBookmark = async (opportunity_id: number) => {
  const response = await apiClient.post('/bookmarks/', { opportunity_id });
  return response.data;
};

export const deleteBookmark = async (opportunity_id: number) => {
  const response = await apiClient.delete(`/bookmarks/${opportunity_id}`);
  return response.data;
};
