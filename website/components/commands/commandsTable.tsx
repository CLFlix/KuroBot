"use client";

import { Command } from "@/types";

type Props = {
  commandsList: Command[];
};

const CommandsTable: React.FC<Props> = ({ commandsList }: Props) => {
  const processedCommands = commandsList.map((command) => ({
    ...command,
    description: command.description.includes("Alias")
      ? command.description.replace("Alias", "\nAlias")
      : command.description,
  }));

  return (
    <>
      <div className="flex justify-center mb-5">
        {processedCommands && (
          <table className="commandsTable">
            <thead>
              <tr>
                <th>Command</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {processedCommands.map((command, index) => (
                <tr key={index}>
                  <td>
                    <code>!{command.name}</code>
                  </td>
                  <td>{command.description}</td>
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
