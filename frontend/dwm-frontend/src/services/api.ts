import axios from "axios";

// Define API response types
export interface Threat {
  site: string;
  url: string;
  context: string;
}

export interface ApiResponse {
  keywords_used: string[];
  scraped_data: Threat[];
  total_links_found: number;
}

// Base URL of the FastAPI backend
const API_BASE_URL = "http://127.0.0.1:8000";

// Function to fetch threat data
export const fetchThreatData = async (keywords: string[]): Promise<Threat[]> => {
  const response = await axios.get<ApiResponse>(`${API_BASE_URL}/scrape`, {
    params: { keywords: keywords.length ? keywords : undefined },
  });
  return response.data.scraped_data;
};