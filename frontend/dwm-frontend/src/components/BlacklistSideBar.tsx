import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useBlacklistData } from "@/hooks/useBlacklistData";
import { RiskBadge } from "./RiskBadge";
import Loader from "@/components/ui/Loader";
import { Alert, AlertTitle } from "@/components/ui/alert";

// Define the BlacklistEntry type
interface BlacklistEntry {
  ip: string;
  risk_category: string;
  risk_score: number;
  data: {
    abuse_confidence_score: number;
    last_reported: string;
  };
}

export default function BlacklistSidebar() {
  const { data: blacklist = [], isLoading, isError } = useBlacklistData();

  return (
    <Card className="w-full lg:w-80 shadow-lg border-red-500">
      <CardHeader>
        <CardTitle className="text-red-600 text-lg">
          ⚠️ Top Malicious IPs from AbuseIPDB
        </CardTitle>
      </CardHeader>

      <CardContent className="max-h-[600px] overflow-y-auto space-y-4">
        {isLoading && <Loader className="text-center" />}

        {isError && (
          <Alert variant="destructive">
            <AlertTitle>Failed to load blacklist data</AlertTitle>
          </Alert>
        )}

        {!isLoading &&
          !isError &&
          blacklist.map((entry: BlacklistEntry, idx: number) => (
            <div key={idx} className="p-2 rounded border bg-gray-50 text-sm">
              <div className="font-bold text-gray-900">{entry.ip}</div>

              <div className="text-xs text-gray-600 flex gap-1 items-center">
                Risk: <RiskBadge riskCategory={entry.risk_category} />
                <span className="ml-1">({entry.risk_score})</span>
              </div>

              <div className="text-xs text-gray-500">
                Confidence Score from AbuseIPDB:{" "}
                {entry.data.abuse_confidence_score}%
              </div>

              <div className="text-xs text-gray-400">
                Last Reported:{" "}
                {new Date(entry.data.last_reported).toLocaleString()}
              </div>
            </div>
          ))}
      </CardContent>
    </Card>
  );
}
