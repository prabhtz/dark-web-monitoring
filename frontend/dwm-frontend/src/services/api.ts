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
export const fetchThreatData = async (keywords: string[] = []): Promise<Threat[]> => {
  const formattedKeywords = keywords.join(","); // Convert array to comma-separated string
  const response = await axios.get<ApiResponse>(`${API_BASE_URL}/scrape`, {
    params: { keywords: formattedKeywords },
    paramsSerializer: (params) => new URLSearchParams(params).toString(),
  });
  return response.data.scraped_data;
};