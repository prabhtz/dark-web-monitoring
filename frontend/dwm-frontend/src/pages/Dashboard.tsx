import { useState } from "react";
import { useThreatData } from "../hooks/useThreatData";
import SearchBar from "../components/SearchBar";
import ThreatTable from "../components/ThreatTable";
import Loader from "@/components/ui/Loader";
import { Alert, AlertTitle } from "@/components/ui/alert";

const Dashboard: React.FC = () => {
  const [keywords, setKeywords] = useState<string[]>([]);
  const { data, isLoading, isError } = useThreatData(keywords);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold text-center mb-6">Threat Intelligence Dashboard</h1>
      <SearchBar onSearch={setKeywords} />

      {isLoading && <Loader className="mt-6 text-center" />}

      {isError && (
        <Alert variant="destructive" className="mt-6">
          <AlertTitle>Error fetching data</AlertTitle>
        </Alert>
      )}

      {data && data.length > 0 && <ThreatTable data={data} />}
    </div>
  );
};

export default Dashboard;