import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const useThreatData = (query: { type: string; value: string }) => {
  return useQuery({
    queryKey: ["threatData", query.type, query.value],
    queryFn: async () => {
      if (!query.value) return [];
      const endpoint = query.type === "darkweb" ? "/darkweb" : "/osint";
      const { data } = await axios.get(`${API_BASE_URL}${endpoint}`, {
        params: { [query.type]: query.value },
      });
      return data.results;
    },
    enabled: !!query.value,
  });
};
