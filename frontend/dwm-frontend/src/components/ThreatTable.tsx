import { Table, TableHead, TableRow, TableCell, TableBody } from "@/components/ui/table";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Threat } from "../services/api";

interface ThreatTableProps {
  data: Threat[];
}

const ThreatTable: React.FC<ThreatTableProps> = ({ data }) => {
  return (
    <div className="overflow-x-auto rounded-lg border border-gray-700 shadow-lg">

      <Table className="w-full table-fixed border-collapse">
        <TableHead>
          <TableRow className="bg-gray-800 text-white uppercase text-sm tracking-wider">
            <TableCell className="p-4 text-lg font-bold w-1/6">Source</TableCell>
            <TableCell className="p-4 text-lg font-bold w-3/6">Threat URL</TableCell>
            <TableCell className="p-4 text-lg font-bold w-2/6">Description</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {data.map((item, index) => (
            <TableRow key={index} className="border-b border-gray-700">
              <TableCell className="p-4 w-1/6 truncate">{item.site}</TableCell>

              <TableCell className="p-4 w-3/6 truncate">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 inline-block truncate hover:underline"
                    >
                      {item.url}
                    </a>
                  </TooltipTrigger>
                  <TooltipContent className="break-words max-w-xs">{item.url}</TooltipContent>
                </Tooltip>
              </TableCell>

              <TableCell className="p-4 w-2/6 truncate">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <span className="block truncate hover:whitespace-normal">
                      {item.context}
                    </span>
                  </TooltipTrigger>
                  <TooltipContent className="break-words max-w-xs">{item.context}</TooltipContent>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};

export default ThreatTable;