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
          <table className="commandsTable">
            <thead>
              <tr>
                <th>Command</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {commandsList.map((command, index) => (
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
