import OSINTSearch from "@/components/OSINTSearch";
import DarkWebSearch from "@/components/DarkWebSearch";

export default function SearchPage() {
  return (
    <div className="container mx-auto px-6 py-8">
      <OSINTSearch />
      <DarkWebSearch />
    </div>
  );
}
