import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
// import Dashboard from "./pages/Dashboard";
import Search from "./pages/Search";

const queryClient = new QueryClient();

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Search />
    </QueryClientProvider>
  );
};

export default App;
