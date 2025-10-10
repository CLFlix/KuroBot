"use client";

import { Command } from "@/types";

type Props = {
  commandsList: Command[];
};

const CommandsTable: React.FC<Props> = ({ commandsList }: Props) => {
  return (
    <>
      <div className="flex justify-center mb-5">
        {commandsList && (
          <table className="text-left">
            <thead className="bg-purple-600 text-white">
              <tr>
                <th className="p-2 w-1/6 text-center">Command</th>
                <th className="p-2 max-w-[200px] truncate text-center">
                  Description
                </th>
              </tr>
            </thead>
            <tbody>
              {commandsList.map((command, index) => (
                <tr key={index} className="border border-gray-800 odd:bg-gray-800 even:bg-gray-700 hover:bg-gray-900">
                  <td className="p-2 font-mono text-center bg-gray-900">{command.name}</td>
                  <td className="p-2 font-sans max-w-[700px] whitespace-normal break-words">
                    {command.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
};

export default CommandsTable;
