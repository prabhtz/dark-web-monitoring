interface RiskBadgeProps {
  riskCategory: string;
}

// Define color mapping based on risk level
const riskColors: Record<string, string> = {
  critical: "bg-red-600 text-white",
  high: "bg-orange-500 text-white",
  moderate: "bg-yellow-500 text-black",
  low: "bg-green-500 text-white",
  safe: "bg-gray-400 text-white",
};

export function RiskBadge({ riskCategory }: RiskBadgeProps) {
  return (
    <span
      className={`px-2 py-1 text-xs font-bold rounded ${
        riskColors[riskCategory.toLowerCase()] || "bg-gray-300 text-black"
      }`}
    >
      {riskCategory}
    </span>
  );
}
