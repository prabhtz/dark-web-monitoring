import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";

interface SearchInputProps {
  onSearch: (searchQuery: string, searchType?: string) => void;
  searchType?: string;
  setSearchType?: (value: string) => void;
  loading: boolean;
  isDarkWeb?: boolean;
}

export default function SearchInput({
  onSearch,
  searchType,
  setSearchType,
  loading,
  isDarkWeb = false,
}: SearchInputProps) {
  const [localQuery, setLocalQuery] = useState("");

  const handleSearch = () => {
    if (localQuery.trim()) {
      onSearch(localQuery, searchType);
    }
  };

  return (
    <div className="flex gap-4 mb-4">
      {!isDarkWeb && setSearchType && (
        <Select value={searchType} onValueChange={setSearchType}>
          <SelectTrigger className="w-32">
            <SelectValue placeholder="Select Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="IP">IP</SelectItem>
            <SelectItem value="URL">URL</SelectItem>
            <SelectItem value="Email">Email</SelectItem>
            <SelectItem value="Hash">File Hash</SelectItem>
          </SelectContent>
        </Select>
      )}

      <Input
        placeholder={
          isDarkWeb ? "Enter dark web keyword..." : `Enter ${searchType}...`
        }
        value={localQuery}
        onChange={(e) => setLocalQuery(e.target.value)}
      />

      <Button onClick={handleSearch} disabled={loading || !localQuery.trim()}>
        {loading ? "Searching..." : "Search"}
      </Button>
    </div>
  );
}
