import { useState } from "react";
import SearchInput from "./SearchInput";
import SearchResults from "./SearchResults";
import { useOSINTData } from "../hooks/useOSINTData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Loader from "@/components/ui/Loader";
import { Alert, AlertTitle } from "@/components/ui/alert";

export default function OSINTSearch() {
  const [searchType, setSearchType] = useState("IP");
  const { data, isLoading, isError, fetchData } = useOSINTData();

  const handleSearch = (searchQuery: string, type?: string) => {
    setSearchType(type || "IP");
    fetchData(searchQuery, type || "IP"); // ✅ Explicitly trigger fetch
  };

  return (
    <Card className="mb-8">
      <CardHeader>
        <CardTitle>🔍 OSINT Threat Intelligence Search</CardTitle>
      </CardHeader>
      <CardContent>
        <SearchInput
          onSearch={handleSearch} // ✅ Pass handleSearch function
          searchType={searchType}
          setSearchType={setSearchType}
          loading={isLoading}
        />

        {isLoading && <Loader className="mt-4" />}

        {isError && (
          <Alert variant="destructive" className="mt-4">
            <AlertTitle>Error fetching OSINT data</AlertTitle>
          </Alert>
        )}

        {data.length > 0 && <SearchResults results={data} />}
      </CardContent>
    </Card>
  );
}
