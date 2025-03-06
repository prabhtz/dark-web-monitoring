import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface SearchBarProps {
  onSearch: (keywords: string[]) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [keywords, setKeywords] = useState("");

  const handleSearch = () => {
    const keywordArray = keywords.split(",").map((word) => word.trim());
    onSearch(keywordArray);
  };

  return (
    <div className="flex gap-4 p-4">
      <Input
        type="text"
        placeholder="Enter threat keywords (comma separated)..."
        value={keywords}
        onChange={(e) => setKeywords(e.target.value)}
      />
      <Button onClick={handleSearch} className="bg-blue-500 hover:bg-blue-600">
        Search
      </Button>
    </div>
  );
};

export default SearchBar;