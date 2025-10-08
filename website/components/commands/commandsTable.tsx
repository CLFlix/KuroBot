"use client";

import { Command } from "@/types";

type Props = {
  commandsList: Command[];
};

const CommandsTable: React.FC<Props> = ({ commandsList }: Props) => {
  return (
    <>
      {commandsList && (
        <table className="min-w-full border border-gray-300 text-left">
          <thead className="bg-blue-900 text-white">
            <tr>
              <th className="p-2 w-1/6">Command</th>
              <th className="p-2 max-w-[400px] truncate">Description</th>
            </tr>
          </thead>
          <tbody>
            {commandsList.map((command, index) => (
              <tr key={index} className="border-t border-gray-300">
                <td className="p-2 font-mono">{command.name}</td>
                <td className="p-2 max-w-[400px] whitespace-normal break-words">
                  {command.description}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

export default CommandsTable;
