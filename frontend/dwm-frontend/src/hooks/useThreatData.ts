import { useQuery } from "@tanstack/react-query";
import { fetchThreatData, Threat } from "../services/api";

export const useThreatData = (keywords: string[]) => {
  return useQuery<Threat[], Error>({
    queryKey: ["threatData", keywords],
    queryFn: () => fetchThreatData(keywords),
    enabled: !!keywords.length, // Only fetch if keywords are provided
    retry: 2, // Retry twice on failure
  });
};