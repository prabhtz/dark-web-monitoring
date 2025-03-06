import { Table, TableHead, TableRow, TableCell, TableBody } from "@/components/ui/table";
import { Threat } from "../services/api";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface ThreatTableProps {
  data: Threat[];
}

const ThreatTable: React.FC<ThreatTableProps> = ({ data }) => {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-700">
      <Table className="w-full">
        <TableHead>
          <TableRow className="bg-gray-800 text-white">
            <TableCell className="p-3 text-lg font-semibold">Source</TableCell>
            <TableCell className="p-3 text-lg font-semibold">Threat URL</TableCell>
            <TableCell className="p-3 text-lg font-semibold">Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((item, index) => (
            <TableRow key={index} className="border-b border-gray-700">
              <TableCell className="p-3">{item.site}</TableCell>

              {/* ✅ Truncate long URLs but show full on hover */}
              <TableCell className="p-3 max-w-[250px] overflow-hidden text-ellipsis whitespace-nowrap">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-400 truncate">
                        {item.url.length > 50 ? `${item.url.slice(0, 50)}...` : item.url}
                      </a>
                    </TooltipTrigger>
                    <TooltipContent>{item.url}</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </TableCell>

              {/* ✅ Limit description text to prevent overflow */}
              <TableCell className="p-3 max-w-[250px] overflow-hidden text-ellipsis whitespace-nowrap">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <span className="truncate">
                        {item.context.length > 50 ? `${item.context.slice(0, 50)}...` : item.context}
                      </span>
                    </TooltipTrigger>
                    <TooltipContent>{item.context}</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ThreatTable;