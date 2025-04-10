import { useQuery } from "@tanstack/react-query";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/blacklist";

export function useBlacklistData() {
  return useQuery({
    queryKey: ["blacklist"],
    queryFn: async () => {
      const response = await axios.get(API_URL);
      return response.data.results;
    },
    staleTime: 1000 * 60 * 5, // cache for 5 minutes
  });
}
