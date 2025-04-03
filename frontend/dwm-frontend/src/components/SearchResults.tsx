/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import { RiskBadge } from "./RiskBadge";

interface ThreatResult {
  source: string;
  risk_score: number;
  risk_category: string;
  data: {
    preview?: string;
    onion_links?: string[];
    [key: string]: any;
  };
}

interface SearchResultsProps {
  results: ThreatResult[];
  isDarkWeb?: boolean;
}

export default function SearchResults({
  results,
  isDarkWeb,
}: SearchResultsProps) {
  const [expandedRows, setExpandedRows] = useState<Record<number, boolean>>({});

  // Toggle Function for Expanding Rows
  const toggleRow = (index: number) => {
    setExpandedRows((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Source</TableHead>
          <TableHead>Risk Score</TableHead>
          <TableHead>Risk Level</TableHead>
          <TableHead>{isDarkWeb ? "Preview" : "Details"}</TableHead>
          {isDarkWeb && <TableHead>Onion Links</TableHead>}
        </TableRow>
      </TableHeader>
      <TableBody>
        {results?.map((result: ThreatResult, idx: number) => (
          <>
            {/* 🔹 Clickable Row */}
            <TableRow
              key={idx}
              onClick={() => toggleRow(idx)}
              className="cursor-pointer hover:bg-gray-100"
            >
              <TableCell>{result.source}</TableCell>

              {/* 🔹 Show Risk Score */}
              <TableCell>
                <span className="font-bold">{result.risk_score}</span>
              </TableCell>

              {/* 🔹 Show Risk Category with Color Coding */}
              <TableCell>
                <RiskBadge riskCategory={result.risk_category} />
              </TableCell>

              {/* 🔹 Clickable Text for Showing Details Instead of "N/A" */}
              <TableCell>
                {result.data && Object.keys(result.data).length > 0 ? (
                  <span className="text-blue-500 underline">
                    Click to view details
                  </span>
                ) : (
                  "N/A"
                )}
              </TableCell>

              {/* 🔹 Onion Links for Dark Web Search */}
              {isDarkWeb && (
                <TableCell>
                  {(result.data.onion_links ?? []).length > 0
                    ? (result.data.onion_links ?? []).map(
                        (link: string, i: number) => (
                          <a
                            key={i}
                            href={`http://${link}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 underline"
                          >
                            {link}
                          </a>
                        )
                      )
                    : "N/A"}
                </TableCell>
              )}
            </TableRow>

            {/* 🔹 Expandable Row for Full Details */}
            {expandedRows[idx] && result.data && (
              <TableRow>
                <TableCell
                  colSpan={isDarkWeb ? 5 : 4}
                  className="bg-gray-50 p-4"
                >
                  <pre className="whitespace-pre-wrap break-words text-sm max-h-40 overflow-auto p-2 bg-white border rounded">
                    {JSON.stringify(result.data, null, 2)}
                  </pre>
                </TableCell>
              </TableRow>
            )}
          </>
        ))}
      </TableBody>
    </Table>
  );
}
