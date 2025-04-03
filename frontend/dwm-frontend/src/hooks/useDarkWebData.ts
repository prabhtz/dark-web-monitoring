/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/darkweb";

export function useDarkWebData() {
  const [data, setData] = useState<any[]>([]);
  const [isError, setError] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = async (query: string) => {
    if (!query) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.get(API_BASE_URL, {
        params: { keyword: query },
      });
      setData(response.data.results);
    } catch (error) {
      setError(true);
      console.error("Error fetching Dark Web data:", error);
    }
    setIsLoading(false);
  };

  return { data, isLoading, fetchData, isError };
}
