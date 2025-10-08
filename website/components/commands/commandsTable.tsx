"use client";

import { Command } from "@/types";

type Props = {
  commandsList: Command[];
};

const CommandsTable: React.FC<Props> = ({ commandsList }: Props) => {
  return (
    <>
      {commandsList && (
        <table className="font-sans m-auto border-separate">
          <thead>
            <tr>
              <th scope="col">Command</th>
              <th scope="col">Description</th>
            </tr>
          </thead>
          <tbody>
            {commandsList.map((command, index) => (
              <tr key={index}>
                <td>{command.name}</td>
                <td>{command.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </>
  );
};

export default CommandsTable;
