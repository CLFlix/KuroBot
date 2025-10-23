import { Command } from "@/types";

const getAllCommands = async (): Promise<Command[]> => {
  const response = await fetch(
    `https://raw.githubusercontent.com/CLFlix/KuroBot/dev/website/public/commands.txt` +
      Date.now()
  );
  const text = await response.text();

  const commands = text
    .trim()
    .split("\n")
    .map((line) => {
      const [name, description, category] = line
        .split(" - ")
        .map((p) => p.trim());

      return {
        name,
        description,
        category: (category || "/") as Command["category"],
      };
    });

  return commands;
};

const CommandsService = { getAllCommands };
export default CommandsService;
