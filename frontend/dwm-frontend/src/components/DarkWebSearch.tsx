import SearchInput from "./SearchInput";
import SearchResults from "./SearchResults";
import { useDarkWebData } from "../hooks/useDarkWebData";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Loader from "@/components/ui/Loader";
import { Alert, AlertTitle } from "@/components/ui/alert";

export default function DarkWebSearch() {
  const { data, isLoading, isError, fetchData } = useDarkWebData();

  const handleSearch = (searchQuery: string) => {
    fetchData(searchQuery); // ✅ Explicitly trigger fetch
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>🌑 Dark Web Threat Search</CardTitle>
      </CardHeader>
      <CardContent>
        <SearchInput
          onSearch={handleSearch} // ✅ Pass handleSearch function
          loading={isLoading}
          isDarkWeb
        />

        {isLoading && <Loader className="mt-4" />}

        {isError && (
          <Alert variant="destructive" className="mt-4">
            <AlertTitle>Error fetching Dark Web data</AlertTitle>
          </Alert>
        )}

        {data.length > 0 && <SearchResults results={data} isDarkWeb />}
      </CardContent>
    </Card>
  );
}
