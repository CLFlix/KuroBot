"use client";

import { Command } from "@/types";

type Props = {
  commandsList: Command[];
};

const CommandsTable: React.FC<Props> = ({ commandsList }: Props) => {
  commandsList.map((command) => {
    if (command.description.includes("Alias")) {
      command.description = command.description.replace("Alias", "\nAlias");
    }
  });

  return (
    <>
      <div className="flex justify-center mb-5">
        {commandsList && (
          <table className="text-left">
            <thead className="table-header-gradient text-white">
              <tr>
                <th className="p-2 w-1/6 text-center">Command</th>
                <th className="p-2 max-w-[200px] truncate text-center">
                  Description
                </th>
              </tr>
            </thead>
            <tbody>
              {commandsList.map((command, index) => (
                <tr
                  key={index}
                  className="border border-gray-900 hover:scale-102 duration-300 table-command-gradient"
                >
                  <td className="p-2 text-center">
                    <code>!{command.name}</code>
                  </td>
                  <td className="p-2 max-w-[700px] whitespace-pre-wrap break-words">
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
