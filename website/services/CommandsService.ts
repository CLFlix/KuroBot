import { Command } from "@/types";

const getAllCommands = async (): Promise<Command[]> => {
  const basePath = process.env.NODE_ENV === "production" ? "/KuroBot" : "";
  const response = await fetch(`${basePath}/commands.txt`);
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
