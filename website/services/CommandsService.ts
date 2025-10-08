import { Command } from "@/types";

const getAllCommands = async (): Promise<Command[]> => {
  const response = await fetch("/commands.txt");
  const text = await response.text();

  const commands = text
    .trim()
    .split("\n")
    .map((line) => {
      const [name, description] = line.split(":").map((p) => p.trim());
      return { name, description } as Command;
    });

  return commands;
};

const CommandsService = () => ({
  getAllCommands,
});

export default CommandsService();
