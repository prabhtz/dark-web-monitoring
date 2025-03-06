import { Table, TableHead, TableRow, TableCell, TableBody } from "@/components/ui/table";
import { Threat } from "../services/api";

interface ThreatTableProps {
  data: Threat[];
}

const ThreatTable: React.FC<ThreatTableProps> = ({ data }) => {
  return (
    <Table className="mt-6">
      <TableHead>
        <TableRow className="bg-gray-800">
          <TableCell>Source</TableCell>
          <TableCell>Threat URL</TableCell>
          <TableCell>Description</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {data.map((item, index) => (
          <TableRow key={index} className="border-b border-gray-700">
            <TableCell>{item.site}</TableCell>
            <TableCell>
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-blue-400">
                {item.url}
              </a>
            </TableCell>
            <TableCell>{item.context}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default ThreatTable;