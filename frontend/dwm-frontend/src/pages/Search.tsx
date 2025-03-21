/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableHeader,
  TableRow,
  TableHead,
  TableBody,
  TableCell,
} from "@/components/ui/table";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
} from "@/components/ui/tooltip";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export default function SearchPage() {
  const [osintQuery, setOsintQuery] = useState("");
  const [darkWebQuery, setDarkWebQuery] = useState("");
  const [osintResults, setOsintResults] = useState<any[]>([]);
  const [darkWebResults, setDarkWebResults] = useState<any[]>([]);
  const [expandedRows, setExpandedRows] = useState<Record<string, boolean>>({});
  const [loadingOsint, setLoadingOsint] = useState(false);
  const [loadingDarkWeb, setLoadingDarkWeb] = useState(false);

  const toggleRow = (index: number) => {
    setExpandedRows((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const fetchOSINTData = async () => {
    if (!osintQuery) return;
    setLoadingOsint(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/osint`, {
        params: { ip: osintQuery },
      });
      setOsintResults(response.data.results);
    } catch (error) {
      console.error("Error fetching OSINT data:", error);
    }
    setLoadingOsint(false);
  };

  const fetchDarkWebData = async () => {
    if (!darkWebQuery) return;
    setLoadingDarkWeb(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/darkweb`, {
        params: { keyword: darkWebQuery },
      });
      setDarkWebResults(response.data.results);
    } catch (error) {
      console.error("Error fetching Dark Web data:", error);
    }
    setLoadingDarkWeb(false);
  };

  return (
    <div className="container mx-auto px-6 py-8">
      {/* 🔹 OSINT Search Section */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>🔍 OSINT Threat Intelligence Search</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4 mb-4">
            <Input
              placeholder="Enter IP, URL, or email..."
              value={osintQuery}
              onChange={(e) => setOsintQuery(e.target.value)}
            />
            <Button onClick={fetchOSINTData} disabled={loadingOsint}>
              {loadingOsint ? "Searching..." : "Search"}
            </Button>
          </div>

          {osintResults.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Source</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead>Details</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {osintResults.map((result, idx) => (
                  <>
                    <TableRow
                      key={idx}
                      onClick={() => toggleRow(idx)}
                      className="cursor-pointer hover:bg-gray-100"
                    >
                      <TableCell>{result.source}</TableCell>
                      <TableCell>
                        <span
                          className={`badge ${result.risk_category.toLowerCase()}`}
                        >
                          {result.risk_category}
                        </span>
                      </TableCell>
                      <TableCell>
                        {result.data && Object.keys(result.data).length > 0 ? (
                          <span className="text-blue-500 underline">
                            Click to view details
                          </span>
                        ) : (
                          "N/A"
                        )}
                      </TableCell>
                    </TableRow>
                    {expandedRows[idx] && result.data && (
                      <TableRow>
                        <TableCell colSpan={3} className="bg-gray-50 p-4">
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
          )}
        </CardContent>
      </Card>

      {/* 🔹 Dark Web Search Section */}
      <Card>
        <CardHeader>
          <CardTitle>🌑 Dark Web Threat Search</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4 mb-4">
            <Input
              placeholder="Enter keyword for dark web search..."
              value={darkWebQuery}
              onChange={(e) => setDarkWebQuery(e.target.value)}
            />
            <Button onClick={fetchDarkWebData} disabled={loadingDarkWeb}>
              {loadingDarkWeb ? "Searching..." : "Search"}
            </Button>
          </div>

          {darkWebResults.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Source</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead>Preview</TableHead>
                  <TableHead>Onion Links</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {darkWebResults.map((result, idx) => (
                  <>
                    <TableRow
                      key={idx}
                      onClick={() => toggleRow(idx + 100)}
                      className="cursor-pointer hover:bg-gray-100"
                    >
                      <TableCell>{result.source}</TableCell>
                      <TableCell>
                        <span
                          className={`badge ${result.risk_category.toLowerCase()}`}
                        >
                          {result.risk_category}
                        </span>
                      </TableCell>
                      <TableCell>
                        {result.data.preview ? (
                          <Tooltip>
                            <TooltipTrigger className="truncate block max-w-[250px]">
                              {result.data.preview.length > 50
                                ? `${result.data.preview.substring(0, 50)}...`
                                : result.data.preview}
                            </TooltipTrigger>
                            <TooltipContent>
                              {result.data.preview}
                            </TooltipContent>
                          </Tooltip>
                        ) : (
                          "N/A"
                        )}
                      </TableCell>
                      <TableCell>
                        {result.data.onion_links?.map(
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
                        ) || "N/A"}
                      </TableCell>
                    </TableRow>
                    {expandedRows[idx + 100] && result.data && (
                      <TableRow>
                        <TableCell colSpan={4} className="bg-gray-50 p-4">
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
          )}
        </CardContent>
      </Card>
    </div>
  );
}
