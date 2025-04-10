// import OSINTSearch from "@/components/OSINTSearch";
// import DarkWebSearch from "@/components/DarkWebSearch";

// export default function Dashboard() {
//   return (
//     <div className="container mx-auto px-6 py-8">
//       <h1 className="text-3xl font-bold text-center mb-6">
//         Threat Intelligence Dashboard
//       </h1>

//       {/* OSINT Section */}
//       <OSINTSearch />

//       {/* Dark Web Section */}
//       <DarkWebSearch />
//     </div>
//   );
// }

import OSINTSearch from "@/components/OSINTSearch";
import DarkWebSearch from "@/components/DarkWebSearch";
import BlacklistSidebar from "@/components/BlacklistSidebar";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 px-6 py-8">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Threat Intelligence Dashboard
      </h1>

      <div className="flex flex-col-reverse lg:flex-row gap-6">
        {/* 🔍 Main Search Area */}
        <div className="flex-1 space-y-6">
          <OSINTSearch />
          <DarkWebSearch />
        </div>

        {/* ⚠️ Right Sidebar for Blacklisted IPs */}
        <div className="w-full lg:w-80">
          <BlacklistSidebar />
        </div>
      </div>
    </div>
  );
}
